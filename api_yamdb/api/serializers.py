from rest_framework import serializers
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404

from reviews.models import  Category, Comment, Genre, GenreTitle, Review, Title, User, 


class UserSerializer(serializers.ModelSerializer):
    confirmation_code = serializers.CharField(
        default=''
    )
    serializers.ChoiceField(
        read_only=True,
        choices=['user', 'moderator', 'admin'],
    )
    password = serializers.HiddenField(
        default='',
        required=False,
        allow_null=True
    )

    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'password',
            'confirmation_code',
            'role',
            'email',
            'bio',
        )
        lookup_field = 'username'


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = (
            'name',
            'slug'
        )


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = (
            'name',
            'slug'
        )


class TitleSerializer(serializers.ModelSerializer):

    genre = GenreSerializer(many=True)
    category = CategorySerializer(many=False)

    class Meta:
        model = Title
        fields = (
            'id',
            'name',
            'year',
            # 'rating', #TODO: сделать вычисляемое поле rating когда появится модель с оценками
            'description',
            'genre',
            'category'
        )

    def create(self, validated_data):
        genres = validated_data.pop('genre')
        category = validated_data.pop('category')
        current_category, status = Category.objects.get_or_create(**category)
        title = Title.objects.create(
            **validated_data,
            category=current_category
        )
        print(f'title: {title}')
        for genre in genres:
            current_genre, status = Genre.objects.get_or_create(**genre)
            GenreTitle.objects.create(
                genre=current_genre,
                title=title
            )
        return title

    def update(self, instance, validated_data):
        genres = validated_data.pop('genre')
        category = validated_data.pop('category')
        current_category, status = Category.objects.get_or_create(**category)

        instance.name = validated_data.get('name', instance.name)
        instance.year = validated_data.get('year', instance.year)
        instance.description = validated_data.get('description', instance.description)
        instance.category = current_category

        for genre in genres:
            current_genre, status = Genre.objects.get_or_create(**genre)
            GenreTitle.objects.get_or_create(
                genre=current_genre,
                title=instance
            )
        instance.save()
        return instance
