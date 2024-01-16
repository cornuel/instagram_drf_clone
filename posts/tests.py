from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User


class PostViewSetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='Demo', password='rootroot')
        refresh = RefreshToken.for_user(self.user)
        self.access_token = str(refresh.access_token)

    def test_get_posts(self):
        response = self.client.get('/api/posts/')
        self.assertEqual(response.status_code, 200)

    def test_create_post(self):
        data = {
            'title': 'Test Post',
            'body': 'This is a test post.',
            "upvote_count": 8,
            "view_count": 0,
            "is_featured": False
        }
        headers = {'Authorization': f'Bearer {self.access_token}'}
        response = self.client.post('/api/posts/', data, headers=headers)
        self.assertEqual(response.status_code, 201)

    def test_update_post(self):
        create_data = {
            'title': 'Test Post',
            'body': 'This is a test post.',
            "upvote_count": 8,
            "view_count": 0,
            "is_featured": False
        }
        create_headers = {'Authorization': f'Bearer {self.access_token}'}
        create_response = self.client.post(
            '/api/posts/', create_data, headers=create_headers)
        self.assertEqual(create_response.status_code, 201)

        # Get the slug of the created post
        post_id = create_response.data['slug']

        # Update the post with new data
        update_data = {
            'title': 'Updated Test Post',
            'body': 'This is an updated test post.',
        }
        update_headers = {'Authorization': f'Bearer {self.access_token}'}
        update_response = self.client.put(
            f'/api/posts/{post_id}/', update_data, headers=update_headers)
        self.assertEqual(update_response.status_code, 200)

    def test_delete_post(self):
        create_data = {
            'title': 'Test Post',
            'body': 'This is a test post.',
            "upvote_count": 8,
            "view_count": 0,
            "is_featured": False
        }
        create_headers = {'Authorization': f'Bearer {self.access_token}'}
        create_response = self.client.post(
            '/api/posts/', create_data, headers=create_headers)
        self.assertEqual(create_response.status_code, 201)

        # Get the slug of the created post
        post_id = create_response.data['slug']

        update_headers = {'Authorization': f'Bearer {self.access_token}'}
        update_response = self.client.delete(
            f'/api/posts/{post_id}/', headers=update_headers)
        self.assertEqual(update_response.status_code, 204)

    def test_update_delete_wrong_user(self):
        create_data = {
            'title': 'Test Post',
            'body': 'This is a test post.',
            "upvote_count": 8,
            "view_count": 0,
            "is_featured": False
        }
        create_headers = {
            'Authorization': f'Bearer {self.access_token}'
        }
        create_response = self.client.post(
            '/api/posts/', create_data, headers=create_headers)
        self.assertEqual(create_response.status_code, 201)

        # Get the slug of the created post
        post_id = create_response.data['slug']

        update_headers = {'Authorization': f'Bearer 123456'}
        update_response = self.client.delete(
            f'/api/posts/{post_id}/', headers=update_headers)
        self.assertEqual(update_response.status_code, 401)
