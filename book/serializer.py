from rest_framework.serializers import ModelSerializer
from .models import Category,Book,Author



class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class AuthorSerializer(ModelSerializer):
    class Meta:
        model = Author
        fields = '__all__'


class BookSerializer(ModelSerializer):
    category = CategorySerializer()
    author = AuthorSerializer()
    
    class Meta:
        model = Book
        fields = '__all__'


