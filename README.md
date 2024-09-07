# Social Media App

## Overview

This project is a Django-based social media application that is containerized using Docker.

## Getting Started

To get started with the project, follow these instructions:

### Build and Run the Docker Containers

Run the following command to build and start the Docker containers:

```bash
docker compose up --build
```

### Superuser Credentials
A superuser is automatically created with the following credentials:

- **Username:** admin
- **Password:** adminpassword


## API Documentation

The project documentation is implemented with Swagger. You can view it by accessing:

[http://0.0.0.0:8000/api/docs/](http://0.0.0.0:8000/api/docs/)

## Authentication

Endpoints require authentication using an admin user. To obtain a token, use the endpoint:

[http://0.0.0.0:8000/api/token/](http://0.0.0.0:8000/api/token/)

with the following body:

```json
{
  "username": "admin2",
  "password": "adminpassword"
}
```

Use the token returned in the **access** field to include in the headers with **Bearer {{token}}**.

## Endpoints

- **GET /users/**: Retrieve a list of all users.
- **GET /users/{id}/**: Retrieve details of a specific user, including the number of total posts, comments, followers, and following.
- **POST /users/{id}/follow/{id}**: Set the user with the first `id` as a follower of the user with the second `id`.
- **POST /users/**: Create a new user.
- **GET /posts/**: Retrieve a list of all posts ordered from newest to oldest from all users, with pagination and filters. Filters: `author_id`, `from_date`, `to_date` (none are compulsory). Pagination parameters: `page_size` (default = 20), `page_number` (default = 1).
- **GET /posts/{id}/**: Retrieve details of a specific post with its last three comments and creator information.
- **POST /posts/**: Create a new post.
- **GET /posts/{id}/comments/**: Retrieve all comments for a specific post.
- **POST /posts/{id}/comments/**: Add a new comment to a post.


## Insomnia Collection

An Insomnia collection is provided to facilitate endpoint testing.

## Running Tests

To run tests, follow these steps:

```bash
$ docker compose exec app sh
$ cd app/app
$ pytest
```

