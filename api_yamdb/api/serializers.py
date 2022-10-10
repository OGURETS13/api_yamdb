from rest_framework import serializers
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from rest_framework.validators import UniqueValidator

from reviews.models import (
    Category,
    Comment,
    Genre,
    GenreTitle,
    Review,
    Title,
    User
)


class AuthSerializer(serializers.ModelSerializer):
    confirmation_code = serializers.HiddenField(
        default=''
    )
    password = serializers.HiddenField(
        default='',
        required=False,
        allow_null=True
    )
    role = serializers.HiddenField(
        default='user'
    )

    class Meta:
        model = User
        fields = (
            'username',
            'password',
            'confirmation_code',
            'role',
            'email',
        )
        lookup_field = 'username'

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError("Username 'me' - под запретом!")
        return value


class UserSerializer(serializers.ModelSerializer):
    confirmation_code = serializers.HiddenField(
        default=''
    )
    password = serializers.HiddenField(
        default='',
        required=False,
        allow_null=True
    )
    role = serializers.ChoiceField(
        choices=['user', 'moderator', 'admin'],
        default='user',
    )

    class Meta:
        model = User
        fields = (
            'username',
            'password',
            'confirmation_code',
            'role',
            'email',
            'bio',
            'first_name',
            'last_name',

        )
        lookup_field = 'username'

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError("Username 'me' - под запретом!")
        return value


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
        genres = validated_data.get('genre', [])
        for genre in genres:
            GenreTitle.objects.get_or_create(
                genre=genre,
                title=instance
            )
        instance.save()
        return instance

    def to_representation(self, instance):
        return TitleReadDelSerializer().to_representation(instance)


class ReviewSerializer(serializers.ModelSerializer):
    title = serializers.SlugRelatedField(
        slug_field='name',
        read_only=True
    )
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    def validate_score(self, value):
        if 0 > value > 10:
            raise serializers.ValidationError('Оценка по 10-бальной шкале!')
        return value

    def validate(self, data):
        request = self.context['request']
        author = request.user
        title_id = self.context.get('view').kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        if (
            request.method == 'POST'
            and Review.objects.filter(title=title, author=author).exists()
        ):
            raise ValidationError('Может существовать только один отзыв!')
        return data

    class Meta:
        fields = '__all__'
        model = Review


class CommentSerializer(serializers.ModelSerializer):
    review = serializers.SlugRelatedField(
        slug_field='text',
        read_only=True
    )
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        fields = '__all__'
        model = Comment
