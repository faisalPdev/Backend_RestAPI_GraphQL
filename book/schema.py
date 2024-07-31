import graphene
from graphene_django.types import DjangoObjectType
from .models import *

class AuthorType(DjangoObjectType):
    class Meta:
        model=Author

class BookType(DjangoObjectType):
    class Meta:
        model=Book

class CategoryType(DjangoObjectType):
    class Meta:
        model=Category
        


class Query(graphene.ObjectType):
    hello = graphene.String(default_value="Hi!")
    all_authors = graphene.List(AuthorType)
    author=graphene.Field(AuthorType, id=graphene.Int(required=True))

    all_categories=graphene.List(CategoryType)
    category=graphene.Field(CategoryType,id=graphene.Int(required=True))
    category_books=graphene.List(BookType,category_id=graphene.Int(required=True))

    all_books=graphene.List(BookType)
    book=graphene.Field(BookType, id=graphene.Int(required=True))


    def resolve_all_authors(root,info):
        return Author.objects.all()
    
    def resolve_author(root,info,id):
        return Author.objects.get(pk=id)
    
    def resolve_all_categories(root,info):
        return Category.objects.all()
    
    def resolve_category(root,info,id):
        return Category.objects.get(pk=id)
    
    def resolve_category_books(root,info,category_id):
        category = Category.objects.get(pk=category_id)
        return Book.objects.filter(category=category) 
    
    def resolve_all_books(root,info):
        return Book.objects.all()
    
    def resolve_book(root,info,id):
        return Book.objects.get(pk=id)
    



class CreateAuthor(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        bio = graphene.String(required=True)
        

    author = graphene.Field(AuthorType)

    def mutate(self, info, name, bio):
        author = Author.objects.create(name=name,bio=bio)
        return CreateAuthor(author=author)
    
class UpdateAuthor(graphene.Mutation):
    class Arguments:
        id=graphene.Int(required=True)
        name = graphene.String(required=True)
        bio = graphene.String(required=True)
    
    author=graphene.Field(AuthorType)

    def mutate(self,info,id,name,bio):
        author = Author.objects.get(pk=id)
        author.name=name
        author.bio=bio
        author.save()
        return UpdateAuthor(author=author)
    
class DeleteAuthor(graphene.Mutation):
    class Arguments:    
        id=graphene.Int(required=True)  

    success=graphene.Boolean()

    def mutate(self,info,id):
        author = Author.objects.get(pk=id)
        author.delete()
        return DeleteAuthor(success=True)
    
class AuthorBooks(graphene.Mutation):
    class Arguments:
        author_id=graphene.Int(required=True)

    author=graphene.Field(AuthorType)
    books=graphene.List(BookType)
    
    def mutate(self, info, author_id):
        author = Author.objects.get(pk=author_id)
        books = Book.objects.filter(author=author)
        return AuthorBooks(author=author, books=books)
    
class CreateCategory(graphene.Mutation):
    class Arguments:
        title=graphene.String(required=True)
    
    category=graphene.Field(CategoryType)
    message=graphene.String()
    
    def mutate(self, info, title):
        category=Category.objects.filter(title=title).first()

        if category:
            return CreateCategory(category=None,message="Category Already Exists")
        else:
            category = Category.objects.create(title=title)
            return CreateCategory(category=category,message="Category Created")
        
class UpdateCategory(graphene.Mutation):
    class Arguments:
        id=graphene.Int(required=True)
        title=graphene.String(required=True)
    
    category=graphene.Field(CategoryType)
    message=graphene.String()

    def mutate(self,info,id,title):
        try:
            category = Category.objects.get(pk=id)
            category.title=title
            category.save()
            return UpdateCategory(category=category,message="Category Updated Successfully")
        except Category.DoesNotExist:
            return UpdateCategory(category=None,message="Category Does Not Exists")
        
class DeleteCategory(graphene.Mutation):
    class Arguments:
        id=graphene.Int(required=True)
    
    success=graphene.Boolean()
    
    def mutate(self, info, id):
        try:
            category = Category.objects.get(pk=id)
            category.delete()
            return DeleteCategory(success=True)
        except Category.DoesNotExist:
            return DeleteCategory(success=False)

class CreateBook(graphene.Mutation):
    class Arguments:
        title=graphene.String(required=True)
        author_id=graphene.Int(required=True)
        category_id=graphene.Int(required=True)

    book=graphene.Field(BookType)
    message=graphene.String()

    def mutate(self,info,title,author_id,category_id):
        try:
            author=Author.objects.get(id=author_id)
        except Author.DoesNotExist:
            return CreateBook(book=None,message="author is not exists")
        
        try:
            category=Category.objects.get(id=category_id)
        except Category.DoesNotExist:
            return CreateBook(book=None,message="category is not exists")
        
        if author and category:
            book=Book.objects.filter(title=title,author=author,category=category).first()

            if book:
                return CreateBook(book=None,message="Book already exists")
            else:
                book = Book.objects.create(title=title, author=author, category=category)
                return CreateBook(book=book, message="Book Created")
            
class UpdateBook(graphene.Mutation):
    class Arguments:
        id=graphene.Int(required=True)
        title=graphene.String(required=True)
        author_id=graphene.Int(required=True)
        category_id=graphene.Int(required=True)

    book=graphene.Field(BookType)
    message=graphene.String()

    def mutate(self, info, id, title, author_id, category_id):
        try:
            author=Author.objects.get(id=author_id)
        except Author.DoesNotExist:
            return UpdateBook(book=None,message="author is not exists")
        
        try:
            category=Category.objects.get(id=category_id)
        except Category.DoesNotExist:
            return UpdateBook(book=None,message="category is not exists")
        
        
        
        if author and category:

            book=Book.objects.filter(pk=id).first()
            if book:    
                book.title=title
                book.author=author
                book.category=category
                book.save()
                return UpdateBook(book=book, message="Book is Updated Successfully")
            else:
                return UpdateBook(book=None,message="Book does not exist")  
            

class DeleteBook(graphene.Mutation):
    class Arguments:
        id=graphene.Int(required=True)
    
    success=graphene.Boolean()
    
    def mutate(self, info, id):
        try:
            book = Book.objects.get(pk=id)
            book.delete()
            return DeleteBook(success=True)
        except Book.DoesNotExist:
            return DeleteBook(success=False)
            
        


        


class Mutation(graphene.ObjectType):
    create_author = CreateAuthor.Field()
    update_author = UpdateAuthor.Field()
    delete_author = DeleteAuthor.Field()
    author_books = AuthorBooks.Field()

    create_category=CreateCategory.Field()
    update_category=UpdateCategory.Field()
    delete_category=DeleteCategory.Field()

    create_book=CreateBook.Field()
    update_book=UpdateBook.Field()
    delete_book=DeleteBook.Field()

schema = graphene.Schema(query=Query,mutation=Mutation)