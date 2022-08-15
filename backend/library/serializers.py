from rest_framework.exceptions import ValidationError
from rest_framework.serializers import ModelSerializer, Serializer, CharField, IntegerField, StringRelatedField, HyperlinkedModelSerializer
from .models import Author, Book


class AuthorSerializer(Serializer):
    first_name = CharField(max_length=64)
    last_name = CharField(max_length=64)
    birthday_year = IntegerField()

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.birthday_year = validated_data.get('birthday_year', instance.birthday_year)
        instance.save()
        return instance

    def create(self, validated_data):
        author = Author(**validated_data)
        author.save()
        return author

    def validate_birthday_year(self, value):
        if value > 2004:
            raise ValidationError('18+')
        return value

    def validate(self, attrs):
        if attrs.get('last_name') == 'Бредбери' and attrs.get('birthday_year') != 1920:
            raise ValidationError('birthday_year must be 1920')
        return attrs


class BookSerializer(Serializer):
    title = CharField(max_length=64)
    authors = AuthorSerializer(many=True)


class AuthorModelSerializer(ModelSerializer):
    class Meta:
        model = Author
        # fields = ['first_name', 'last_name']
        fields = '__all__'


class BookModelSerializer(ModelSerializer):
    # authors = StringRelatedField(many=True)

    class Meta:
        model = Book
        # fields = ['first_name', 'last_name']
        fields = '__all__'
