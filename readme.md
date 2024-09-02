# Backend Using RestAPI and GraphQL








## Packages Used

- Django
- Django Rest Framework
- Graphene-django
- drf-yasg for restapi documentation


## Database

- sqlite3
## Features

- CRUD operations for Author, Category, and Book
- Category wise Books
- Author wise Books
- Containerised using Docker


## Run Locally

Clone the project

```bash
  git clone https://github.com/faisalPdev/Backend_RestAPI_GraphQL.git
```

Go to the project directory

```bash
  cd Backend_RestAPI_GraphQL
```

Docker compose up and build

```bash
  docker compose up --build
```

To test restapi

```bash
  http://localhost:8000/api/swagger/
```
To test GraphQl

```bash
  http://localhost:8000/graphql 
```

