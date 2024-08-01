Backend Using RestAPI and GraphQL

Packages used
- Django
- Django Rest Framework
- Graphene-django
- drf-yasg for restapi documentation

DataBase
- sqlite3

Models
- Author
- Category
- Book

Features
- CRUD operations for Author, Category, and Book
- Category wise Books
- Author wise Books
- Containerised using Docker

Run
- clone the repo
- docker compose up --build
- http://localhost:8000/api/swagger/               #for  restapi
- http://localhost:8000/graphql                    #for  graphql
