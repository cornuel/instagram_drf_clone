# First Commit
## Dependancies
Installed `django`, `djangorestframework`, `django-extensions`, `djangorestframework-simplejwt`, `python-decouple`
## Git
- -Setup the `.gitignore` kick venv, .env and ,pyc files
## Django setup
- Created the blog project with django
# Second Commit
## Blog
- Added `permissions.py` with the new permissions `IsAccountOwnerOrAdmin`
## Core app
- Created class `TimestampedModel`
## Auth app
- Created `view` `MyTokenObtainPairView` based on `TokenObtainPairView` from the simplejwt package
- Created `serializers.py` `MyTokenObtainPairSerializer` based on `TokenObtainPairSerializer`
- Created `urls.py`
## Users app
- In `models.py` added a receiver to create a `Profile` whenever a User is created
- Created `serializers.py` -> validate the password
- Created `urls.py` -> login and refresh the token
## Profiles app
- Added the `Profile` model
- Added the view `ProfileModelViewSet`
- Added the serializers `ProfileListSerializer` and `ProfileDetailSerializer`
- Added `urls.py`
## Tags app
### Added the `Tag` model
- override `save` method to save the *slugified* name and the name *titled*
### Added the view `TagModelViewSet`
override `create` method to check if the `slug` already exists

- Added the serializers `TagSerializer`
- Added `urls.py`
## Posts app
- Added the `Post` and `Comment` model
- Added the view `PostViewSet`
- Added `urls.py`
### Added the serializers `PostListSerializer`, `PostDetailSerializer` and `CommentSerializer`
#### PostDetailSerializer
- override `create`
    - save the slugified `title`
    - With the `TagListField`
        - override the `to_internal_value` to `get` or `create` a tag by its `name`
    - add the tags in the newly created instance and update the `post_count` in them
- override `update`
    - add or remove `tags` and the `post_count` in them
    - delete the tag if its `post_count` is 0
- override `delete`
    - update the `post_count` in the post tags
    - delete the tag if its `post_count` is 0
## Blog url
- Modified the blog `urls.py` to have the routes for every apps
- Modified `settings.py` to add all the new apps and library, `simplejwt` config
## Migrations
- `makemigrations` and `migrate` to render our initial db
# Third commit - 10/10/23
- Changed `IsAccountOwnerOrAdmin()` permissions to check the post Profile instead of User
## Profiles app
### Serializers
- Created `PublicProfileSerializer`
### Views
- Modified `get_serializer_class()`, to use `PublicProfileSerializer` by default and `ProfileDetailSerializer` if user is owner of the profile
## Posts app
### Models
- Changed user `model` into `profile`
### Serializers
- Changed list serializer to use `profile = PublicProfileSerializer()`, 
- Changed detail serializer to use `profile = serializers.StringRelatedField(read_only=True)`, 
### Views
- Modified `perform_create()` to save the `profile` instead of `user`
## Tags app
### Views
- Added a `delete_all()` method (for debug purpose)
# Forth commit 11/10/23
## Posts app
### Views
- Added `toggle_feature()` with no more than 3 featured posts active
# Fifth commit 11/10/23
## Posts app
### Views
- Fixed bug for `toggle_feature()`, no more than 3 featured posts active *per user*!
# Sixth commit 11/10/23
## Profiles app
### Models
- Added `favorite_posts`
## Posts app
### Views
- Added `toggle_favorite()`
# Seventh commit 11/10/23
## Posts app
### Views
- Modified `toggle_favorite()` to increment/decrement the `upvote_count` of the post
# Eighth commit 11/10/23
## Profiles app
### Views
- Added POST `follow()`, GET `following()` and GET `followers()`
### Serializers
- Added `SimpleProfileSerializer` to simply serialize the following/followers profile list
- Added manually calculated `following_count` and `followers_count`
### Models
- Renamed `image` with `profile_pic_url`
- Added `full_name` char field
# Ninth commit 12/10/23
- Renamed app name from `blog` to `app`
# Tenth commit 12/10/23
## Posts app
### Models
- Added `likes`, a manytomany rel with `Profile`
### Views
- Added the action `like`
### Serializers
- Added manually calculated `like_count`
# Commit 11 - 12/10/23
## Posts app
### Models
- Added reverse relation for `profile` to gain access to the posts of a profile
### Views
- Strongely typed every views
- Removed `reset_upvote_count()`
- Renamed `toggle_favorite()` -> `favorite()`
- Renamed `toggle_featured()` -> `feature()`
### Serializers
- Added `is_liked` and `is_favorited`
## Profiles app
### Views
- Strongley typed every views
- Added `posts()` to see every posts per user