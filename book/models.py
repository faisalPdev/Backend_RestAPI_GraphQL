from django.db import models

# Create your models here.

class Category(models.Model):
    title=models.CharField(max_length=100)

    def __str__(self):
        return self.title
    

class Author(models.Model):
    name=models.CharField(max_length=100)
    bio=models.CharField(max_length=100)

    def __str__(self):
        return self.name
    

class Book(models.Model):
    title=models.CharField(max_length=100)
    category=models.ForeignKey(Category, on_delete=models.CASCADE)
    author=models.ForeignKey(Author, on_delete=models.CASCADE)
    
    def __str__(self):  
        return self.title