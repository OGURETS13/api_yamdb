from rest_framework import serializers
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404

from reviews.models import (
    Category,
    # Comment,
    Genre,
    GenreTitle,
    # Review,
    Title,
    User)


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


class TitleReadDelSerializer(serializers.ModelSerializer):

    genre = GenreSerializer(many=True, read_only=True)
    category = CategorySerializer(many=False, read_only=True)

    class Meta:
        model = Title
        fields = (
            'id',
            'name',
            'year',
            # 'rating',
            # TODO: сделать вычисляемое поле когда появится модель с оценками
            'description',
            'genre',
            'category'
        )


class TitleCreateUpdateSerializer(serializers.ModelSerializer):

    genre = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Genre.objects.all(),
        many=True
    )
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all()
    )

    class Meta:
        model = Title
        fields = (
            'id',
            'name',
            'year',
            'description',
            'genre',
            'category'
        )

    def create(self, validated_data):
        genres = validated_data.pop('genre')
        category = validated_data.pop('category')
        title = Title.objects.create(
            **validated_data,
            category=category
        )
        for genre in genres:
            GenreTitle.objects.create(
                genre=genre,
                title=title
            )
        return title

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.year = validated_data.get('year', instance.year)
        instance.description = validated_data.get(
            'description',
            instance.description
        )
        instance.category = validated_data.get(
            'category',
            instance.category
        )
        genres = validated_data.pop('genre')
        for genre in genres:
            GenreTitle.objects.get_or_create(
                genre=genre,
                title=instance
            )
        instance.save()
        return instance

    def to_representation(self, instance):
        return TitleReadDelSerializer().to_representation(instance)
