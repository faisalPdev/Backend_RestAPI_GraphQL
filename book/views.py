from django.http import Http404
from django.shortcuts import render
from .models import *
from .serializer import *
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework import generics
from rest_framework import status
# Create your views here.


class AuthorListCreateAPIView(APIView):
    permission_classes=[AllowAny]

    def get(self, request,*args, **kwargs):
        authors=Author.objects.all()
        serializer=AuthorSerializer(authors, many=True)
        return Response(serializer.data)
    
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'name': openapi.Schema(type=openapi.TYPE_STRING, description='The name of the author'),
                'bio': openapi.Schema(type=openapi.TYPE_STRING,description='bio'),
                # Add other fields as needed
            },
            required=['name']  # Specify required fields here
        ),
        responses={
            201: openapi.Response(
                description='Author created',
                schema=AuthorSerializer()
            ),
            400: openapi.Response(
                description='Bad request'
            ),
        }
    )

    def post(self, request,*args,**kwargs):
        serializer=AuthorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)    
    
class AuthorDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset=Author.objects.all()
    serializer_class=AuthorSerializer

class AuthorBooksListAPIView(generics.ListAPIView):
    serializer_class=BookSerializer

    def get_queryset(self,*args, **kwargs):
        author_id=self.kwargs.get('id')
        return Book.objects.filter(author_id=author_id)

class CategoryListCreateAPIView(generics.ListCreateAPIView):
    queryset=Category.objects.all()
    serializer_class=CategorySerializer

class CategoryDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset=Category.objects.all()
    serializer_class=CategorySerializer



class CategoryBookListAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        category_id = self.kwargs.get('id')
        books = Book.objects.filter(category_id=category_id)
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)


class BookListCreateAPIView(generics.ListCreateAPIView):
    queryset=Book.objects.all()
    serializer_class=BookSerializer

    def create(self, request, *args, **kwargs):
        title=request.data.get('title')
        author_id=request.data.get('author')
        category_id=request.data.get('category')    
        try:
         author=Author.objects.get(id=author_id) 
        except Author.DoesNotExist:
            return Response({'error':'Author not found'}, status=status.HTTP_404_NOT_FOUND)
        
        try:
         category=Category.objects.get(id=category_id)
        except Category.DoesNotExist:
            return Response({'error':'Category not found'}, status=status.HTTP_404_NOT_FOUND)   
        
        book=Book.objects.filter(title=title,author_id=author_id,category_id=category_id).first()

        if book:
            return Response({'error':'Book already exists'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            book=Book.objects.create(title=title, author=author, category=category)
            return Response(BookSerializer(book).data, status=status.HTTP_201_CREATED)

class BookDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset=Book.objects.all()
    serializer_class=BookSerializer 

    def update(self, request, *args, **kwargs):
        
        title=request.data.get('title')
        author_id=request.data.get('author')
        category_id=request.data.get('category')    
        
        try:
         author=Author.objects.get(id=author_id) 
        except Author.DoesNotExist:
            return Response({'error':'Author not found'}, status=status.HTTP_404_NOT_FOUND)
        
        try:
         category=Category.objects.get(id=category_id)
        except Category.DoesNotExist:
            return Response({'error':'Category not found'}, status=status.HTTP_404_NOT_FOUND)   

        
        try:
            book = self.get_object()
        except Http404:
            return Response({'error': 'Book not found'}, status=status.HTTP_404_NOT_FOUND)

        
        book.title = title
        book.author = author
        book.category = category
        book.save()

        return Response(BookSerializer(book).data, status=status.HTTP_200_OK)
        
        
            

    

        
    
        
    


    
    

    

   
    
