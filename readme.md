# Running Your Django Project with Docker

Follow these steps to run this Django project using Docker. Docker allow us to create a containerized environment for your application, making it portable and easy to manage.

## Prerequisites

- [Docker](https://www.docker.com/products/docker-desktop) installed on your system.

## Step 1: Clone Your Project
### Navigate to the directory where this Django project is located.
`cd /path/to/your/project/directory`

## Step 2: Build the Docker Image
### Build a Docker image for this Django project using the provided Dockerfile.
`docker build -t book-writer-app .`

## Step 3: Run the Docker Container
### Run a Docker container using the built image.
`docker run -d --name book-writer-container -p 8000:8000 book-writer-app`

## Step 4: Access Your Django Application
### Your Django application should now be running inside a Docker container.
### You can access it by opening a web browser and going to:
### http://localhost:8000/
### This assumes that your Django application is configured to run on port 8000.

## Step 5: Stop and Remove the Container
### To stop and remove the Docker container when you're done.
`docker stop book-writer-container`
`docker rm book-writer-container`

## Step 6: Clean Up (Optional)
### If you want to remove the Docker image as well.
`docker rmi book-writer-app`

# Django Model Schemas

## Book

Represents books in the system.

| Field         | Type          | Description                                      |
|---------------|---------------|--------------------------------------------------|
| `title`       | CharField     | The title of the book.                          |
| `author`      | ForeignKey    | The author of the book (linked to User model).  |
| `collaborators`| ManyToManyField | Collaborators on the book (linked to User model). |

## Section

Represents sections within a book. Sections can be nested within other sections.

| Field             | Type          | Description                                         |
|-------------------|---------------|-----------------------------------------------------|
| `title`           | CharField     | The title of the section.                           |
| `book`            | ForeignKey    | The book to which the section belongs (linked to Book model). |


## Subsection

Represents subsections within a section.

| Field      | Type          | Description                                         |
|------------|---------------|-----------------------------------------------------|
| `title`    | CharField     | The title of the subsection.                       |
| `section`  | ForeignKey    | The section to which the subsection belongs (linked to Section model). |
| `parent_subsection`  | ForeignKey    | Parent sub section to which this sub section is nested (self-referential). |

# API DOCUMENTATION

# User Registration

## Endpoint: `/api/registration/`

**Method:** `POST`

**Authentication:** Not required

**Description:** Register a new user.

**Request Body:**
- `username` (string, required): The username of the new user.
- `email` (string, required): The email address of the new user.
- `password` (string, required): The password of the new user.

**Response:**
- `201 Created`: If the user is successfully registered.
- `400 Bad Request`: If the request data is invalid.

# User Login

## Endpoint: `/api/login/`

**Method:** `POST`

**Authentication:** Not required

**Description:** Log in as an existing user.

**Request Body:**
- `username` (string, required): The username of the user.
- `password` (string, required): The password of the user.

**Response:**
- `200 OK`: If the user is successfully logged in.
  - Response includes tokens for authentication:
    - `refresh`: Refresh token.
    - `access`: Access token.
- `401 Unauthorized`: If the provided credentials are invalid.

# Book List

## Endpoint: `/api/books/`

**Method:** `GET`

**Authentication:** Required

**Permissions:** Authenticated users can access.

**Description:** Get a list of all books.

**Response:**
- `200 OK`: Successful response with a list of books.
- `401 Unauthorized`: If the user is not authenticated.

# Create Book

## Endpoint: `/api/books/`

**Method:** `POST`

**Authentication:** Required

**Description:** Create a new book.

**Request Body:**
- `title` (string, required): The title of the new book.

**Response:**
- `201 Created`: If the book is successfully created.
- `400 Bad Request`: If the request data is invalid.

# Book Detail

## Endpoint: `/api/books/{book_id}/`

**Method:** `GET`

**Authentication:** Required

**Permissions:** Only the author or collaborator can access.

**Description:** Get details of a specific book.

**Response:**
- `200 OK`: Successful response with book details.
- `404 Not Found`: If the book with the specified ID does not exist.
- `403 Forbidden`: If the user does not have permission.

# Update Book

## Endpoint: `/api/books/{book_id}/`

**Method:** `PUT`

**Authentication:** Required

**Permissions:** Only the author or collaborator can access.

**Description:** Update details of a specific book.

**Request Body:**
- `title` (string, required): The updated title of the book.

**Response:**
- `200 OK`: If the book is successfully updated.
- `400 Bad Request`: If the request data is invalid.
- `404 Not Found`: If the book with the specified ID does not exist.
- `403 Forbidden`: If the user does not have permission.

# Delete Book

## Endpoint: `/api/books/{book_id}/`

**Method:** `DELETE`

**Authentication:** Required

**Permissions:** Only the author can access.

**Description:** Delete a specific book.

**Response:**
- `204 No Content`: If the book is successfully deleted.
- `404 Not Found`: If the book with the specified ID does not exist.
- `403 Forbidden`: If the user does not have permission.

# Create Section

## Endpoint: `/api/sections/`

**Method:** `POST`

**Authentication:** Required

**Permissions:** Only the author can create sections for a book.

**Description:** Create a new section.

**Request Body:**
- `book` (integer, required): The ID of the book to which the section belongs.
- `title` (string, required): The title of the new section.

**Response:**
- `201 Created`: If the section is successfully created.
- `400 Bad Request`: If the request data is invalid.

# Section Detail

## Endpoint: `/api/sections/{section_id}/`

**Method:** `GET`

**Authentication:** Required

**Permissions:** Only the author or collaborator can access.

**Description:** Get details of a specific section.

**Response:**
- `200 OK`: Successful response with section details.
- `404 Not Found`: If the section with the specified ID does not exist.
- `403 Forbidden`: If the user does not have permission.

# Update Section

## Endpoint: `/api/sections/{section_id}/`

**Method:** `PUT`

**Authentication:** Required

**Permissions:** Only the author or collaborator can access.

**Description:** Update details of a specific section.

**Request Body:**
- `title` (string, required): The updated title of the section.

**Response:**
- `200 OK`: If the section is successfully updated.
- `400 Bad Request`: If the request data is invalid.
- `404 Not Found`: If the section with the specified ID does not exist.
- `403 Forbidden`: If the user does not have permission.

# Delete Section

## Endpoint: `/api/sections/{section_id}/`

**Method:** `DELETE`

**Authentication:** Required

**Permissions:** Only the author can access.

**Description:** Delete a specific section.

**Response:**
- `204 No Content`: If the section is successfully deleted.
- `404 Not Found`: If the section with the specified ID does not exist.
- `403 Forbidden`: If the user does not have permission.

# Create Subsection

## Endpoint: `/api/subsections/`

**Method:** `POST`

**Authentication:** Required

**Permissions:** Only the author can create subsections for a section in a book.

**Description:** Create a new subsection.

**Request Body:**
- `section` (integer, required): The ID of the section to which the subsection belongs.
- `title` (string, required): The title of the new subsection.

**Response:**
- `201 Created`: If the subsection is successfully created.
- `400 Bad Request`: If the request data is invalid.

# Subsection Detail

## Endpoint: `/api/subsections/{subsection_id}/`

**Method:** `GET`

**Authentication:** Required

**Permissions:** Only the author or collaborator can access.

**Description:** Get details of a specific subsection.

**Response:**
- `200 OK`: Successful response with subsection details.
- `404 Not Found`: If the subsection with the specified ID does not exist.
- `403 Forbidden`: If the user does not have permission.

# Update Subsection

## Endpoint: `/api/subsections/{subsection_id}/`

**Method:** `PUT`

**Authentication:** Required

**Permissions:** Only the author or collaborator can access.

**Description:** Update details of a specific subsection.

**Request Body:**
- `title` (string, required): The updated title of the subsection.

**Response:**
- `200 OK`: If the subsection is successfully updated.
- `400 Bad Request`: If the request data is invalid.
- `404 Not Found`: If the subsection with the specified ID does not exist.
- `403 Forbidden`: If the user does not have permission.

# Delete Subsection

## Endpoint: `/api/subsections/{subsection_id}/`

**Method:** `DELETE`

**Authentication:** Required

**Permissions:** Only the author can access.

**Description:** Delete a specific subsection.

**Response:**
- `204 No Content`: If the subsection is successfully deleted.
- `404 Not Found`: If the subsection with the specified ID does not exist.
- `403 Forbidden`: If the user does not have permission.

# Add Collaborator

## Endpoint: `/api/books/{book_id}/collaborators/{user_id}/add/`

**Method:** `POST`

**Authentication:** Required

**Permissions:** Only the author can add collaborators to a book.

**Description:** Add a collaborator to a book.

**Response:**
- `200 OK`: If the collaborator is successfully added.
- `403 Forbidden`: If the user does not have permission.

# Remove Collaborator

## Endpoint: `/api/books/{book_id}/collaborators/{user_id}/remove/`

**Method:** `POST`

**Authentication:** Required

**Permissions:** Only the author can remove collaborators from a book.

**Description:** Remove a collaborator from a book.

**Response:**
- `200 OK`: If the collaborator is successfully removed.
- `403 Forbidden`: If the user does not have permission.