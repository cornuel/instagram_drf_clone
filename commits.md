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