from django.urls import path,include
from .views import *
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
   openapi.Info(
      title="BOOK API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   
)




urlpatterns = [
   #author
   path('author/',AuthorListCreateAPIView.as_view()),
   path('author/detail/<int:pk>/',AuthorDetailAPIView.as_view()),
   path('author/books/<id>/',AuthorBooksListAPIView.as_view()),

   #category
   path('category/',CategoryListCreateAPIView.as_view()),
   path('category/detail/<int:pk>/',CategoryDetailAPIView.as_view()),
   path('category/books/<id>',CategoryBookListAPIView.as_view()),

   #books
   path('book/',BookListCreateAPIView.as_view()),
   path('book/detail/<int:pk>/',BookDetailAPIView.as_view()),
   

   

   



   path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
   

    
]
