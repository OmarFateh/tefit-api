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
