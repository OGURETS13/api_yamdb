from random import randint

from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import status, mixins, viewsets, permissions, filters
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django_filters.rest_framework import DjangoFilterBackend

from reviews.models import User, Category, Genre, Title
from .serializers import (
    UserSerializer,
    CategorySerializer,
    GenreSerializer,
    TitleSerializer
)
from .permissions import IsAdminOrReadOnly


class SendConfirmationCodeView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)

        if serializer.is_valid():
            confirmation_code = str(randint(100000, 999999))
            email = request.data['email']

            send_mail(
                'YAMDB Confirmation code',
                str(request.data['username'] + '\n' + str(confirmation_code)),
                'from@example.com',
                [email],
                fail_silently=False,
            )

            serializer.save(confirmation_code=confirmation_code)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetTokenView(APIView):
    def post(self, request):
        username = request.data['username']
        confirmation_code = request.data['confirmation_code']
        user = get_object_or_404(User, username=username)

        if confirmation_code == user.confirmation_code:
            refresh = RefreshToken.for_user(user)
            return Response({
                'access': str(refresh.access_token),
            })


class CreateListDestroyViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    pass


class CategoryViewSet(CreateListDestroyViewSet):
    #TODO: пагинация
    permission_classes = (IsAdminOrReadOnly,)
    # permission_classes = (permissions.AllowAny,)
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'slug'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class GenreViewSet(CreateListDestroyViewSet):
    #TODO: пагинация
    permission_classes = (IsAdminOrReadOnly,)
    # permission_classes = (permissions.AllowAny,)
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    lookup_field = 'slug'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class TitleViewSet(viewsets.ModelViewSet):
    #TODO: пагинация
    # permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    permission_classes = (permissions.AllowAny,)
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    filterset_fields = ('category__slug', 'genre__slug', 'name', 'year')