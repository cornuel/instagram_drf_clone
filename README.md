# Instagram DRF Clone

This Instagram DRF Clone is a full-fledged social media platform built using Django Rest Framework.
It provides a range of functionalities similar to the original Instagram platform, including user authentication, profile management, post creation, commenting, tagging, searching, and more.

## Features

### Authentication

- **Token Generation**:
    - `/token`: Endpoint to obtain refresh and access tokens.
    - `/token/refresh`: Endpoint to obtain a new refresh token.
    - `/token/verify`: Endpoint to verify a token.

### Profiles

- **CRUD Operations**:
    - `/profiles/:profile_name`: CRUD endpoints for managing user profiles.
- **Actions**:
    - `/follow`: Action to follow or unfollow a profile.
    - `/following`: Get a list of profiles that the user is following.
    - `/followers`: Get a list of profiles that follow the user.
    - `/isFollowing`: Check if the authenticated user is following a profile.

### Posts

- **CRUD Operations**:
    - `/posts`: CRUD endpoints for managing posts.
- **Actions**:
    - `/favorited`: Get a list of favorited posts by the requesting user.
    - `:post_slug/tags`: Get all tags associated with a post.
    - `:post_slug/feature`: Mark a post as featured/unfeatured (can only be done by the post owner).
    - `:post_slug/favorite`: Mark a post as favorite/unfavorite.
    - `:post_slug/like`: Like/unlike a post.
    - `:post_slug/likes`: Get a list of profiles that like the post.
    - `:post_slug/publish`: Publish/unpublish a post (can only be done by the post owner).
    - `:post_slug/download`: Download a zip containing all original images in the post.
    - `:post_slug/comments`: Get a list of root comments to the post.
    - `:post_slug/comment/:comment_id`: Get a list of replies to a specific comment.

### Comments

- **CRUD Operations**:
    - `/comments`: CRUD endpoints for managing comments.
- **Actions**:
    - `:comment_id/like`: Like/unlike a comment.
    - `:comment_id/likes`: Get a list of profiles that like the comment.

### Tags

- **CRUD Operations**:
    - `/tags`: CRUD endpoints for managing tags.

### Search

- **List Endpoint**:
    - `/search`: Endpoint for searching profiles, posts, or tags.
- **Parameters**:
    - `?query`: The search query.
    - `?type`: Type of search (profile, post, or tag).
    - `?page`: The page number for paginated results.

### Hosting

- **Platform**: Hosted on [PythonAnywhere](https://www.pythonanywhere.com/).
- **Database**: MySQL database hosted on [PythonAnywhere](https://www.pythonanywhere.com/).
- **Storage**: Assets stored inside an Amazon S3 bucket using Django Storages.

## Getting Started

To get started with this Instagram clone app, follow these steps:

1. Clone the repository to your local machine.
2. Install the required dependencies listed in `requirements.txt`.
3. Set up a MySQL database.
4. Modify DATABASES in settings.py
5. Run migrations to create necessary database tables.
6. Start the Django server with .
7. Explore the API endpoints using tools like Postman or cURL.

## License

This project is licensed under the MIT License.

## Acknowledgments

- Thanks to Django Rest Framework and all the open-source libraries used in this project.
- Inspired by the functionality of Instagram.
