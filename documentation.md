# Tefit API #

This API allows you to write a blog with authentication.

The API is available at `http://127.0.0.1:8000/`

## Endpoints ##

### Categories List ###

GET `api/blog/categories/list/`

Returns a list of categories.

### Category Posts List ###

GET `api/blog/categories/:categorySlug/posts/list/`

Returns a list of posts of a category.

### Single Category ###

GET `api/blog/categories/:categorySlug/`

Retrieve detailed information about a category.

### Create Category ###

POST `api/blog/categories/create/`

Allows you to create a new category. Requires authentication.

Request Data:

 - `title` - String - maxLength: 50 - minLength: 1 - Required
 
### Update Category ###

PATCH `api/blog/categories/:categorySlug/`

Update an existing category. Requires authentication.

Request Data:

 - `title` - String - maxLength: 50 - minLength: 1 - Required

### Delete Category ###

DELETE `api/blog/categories/:categorySlug/`

Delete an existing category. Requires authentication.

The request body needs to be empty.

### Posts List ###

GET `api/blog/posts/list/`

Returns a list of posts.

### Single Post ###

GET `api/blog/posts/:postSlug/`

Retrieve detailed information about a post.

### Create Post ###

POST `api/blog/posts/create/`

Allows you to create a new post. Requires authentication.

Request Data:

 - `title` - String - maxLength: 200 - Required
 - `overview` - String - Required
 - `thumbnail` - imagefile - Required
 - `category` - Integer - categoryId - Required
 - `content` - String - Required
 - `status` - String - availableValues: draft, published - Required
 
### Update Post ###

PATCH `api/blog/posts/:postSlug/`

Update an existing post. Requires authentication.

Request Data:

 - `title` - String - maxLength: 200 - Required
 - `overview` - String - Required
 - `thumbnail` - imagefile - Required
 - `category` - Integer - categoryId - Required
 - `content` - String - Required
 - `status` - String - availableValues: draft, published - Required

### Delete Post ###

DELETE `api/blog/posts/:postSlug/`

Delete an existing post. Requires authentication.

## API Authentication ##

To create, update, or delete a category or post, you need to login your API client.

### Token ###

POST `/api/users/token/`

Return access and refresh tokens.

Request Data:

 - `username` - String - Required
 - `password` - String - Required

### Register ###

POST `/api/users/register/`

Allows you to create a new user. Requires authentication.

Request Data:

 - `username` - String - maxLength: 150 - 150 characters or fewer. Letters, digits and @/./+/-/_ only - Required
 - `first_name` - String - maxLength: 30 - Required
 - `last_name` - String - maxLength: 150 - Required
 - `email` - String - Required
 - `email2` - String - Required
 - `password` - String - maxLength: 128 - Required
 - `password2` - String - Required

### Change Password ###

PATCH `/api/users/password/change/`

Allows you to change a user's password. Requires authentication.

Request Data:

 - `old_password` - String - Required
 - `new_password1` - String - Required
 - `new_password2` - String - Required

### Reset Password Email ###

POST `/api/users/password/reset/`

Send email to user's email with reset password link.

Request Data:

 - `email` - String - Required

### Reset Password Token ###

GET `/api/users/password/reset/:uidb64/:token/`

Check if the reset password link is valid, and return uidb64 and token.

The response body will contain the uidb64 and token.

### Reset Password Form ###

PATCH `/api/users/password/reset/complete/`

Allows you to reset a user's password.

Request Data:

 - `new_password1` - String - Required
 - `new_password2` - String - Required
 - `token` - String - Required
 - `uidb64` - String - Required
