from random import randint

from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import status, mixins, viewsets, filters, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django_filters.rest_framework import DjangoFilterBackend

from reviews.models import User, Category, Genre, Title
from .permissions import IsAdminOrReadOnly
from .serializers import (
    UserSerializer,
    CategorySerializer,
    GenreSerializer,
    TitleReadDelSerializer,
    TitleCreateUpdateSerializer,
    UserSerializer
)


class SendConfirmationCodeView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        username = request.data['username']

        if User.objects.filter(username=username).exists():
            instance = User.objects.get(username=username)
            serializer = UserSerializer(
                instance=instance,
                data=request.data
            )

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
    # TODO: пагинация
    permission_classes = (IsAdminOrReadOnly,)
    # permission_classes = (permissions.AllowAny,)
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'slug'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class GenreViewSet(CreateListDestroyViewSet):
    # TODO: пагинация
    permission_classes = (IsAdminOrReadOnly,)
    # permission_classes = (permissions.AllowAny,)
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    lookup_field = 'slug'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class TitleViewSet(viewsets.ModelViewSet):
    # TODO: пагинация
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    # permission_classes = (permissions.AllowAny,)
    queryset = Title.objects.all()
    filterset_fields = ('category__slug', 'genre__slug', 'name', 'year')

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve', 'destroy'):
            return TitleReadDelSerializer
        if self.action in ('create', 'update'):
            return TitleCreateUpdateSerializer



class MeViewSet(viewsets.ViewSet):
    def retrieve(self, request, pk=None):
        queryset = User.objects.all()
        me = get_object_or_404(queryset, pk=request.user.pk)
        serializer = UserSerializer(me)
        return Response(serializer.data)

    def partial_update(self, request, pk=None):
        queryset = User.objects.all()
        me = get_object_or_404(queryset, pk=request.user.pk)
        serializer = UserSerializer(me, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAdminOrReadOnly,)
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)

    def perform_create(self, serializer):
        if 'role' in self.request.data:
            serializer.save(role=self.request.data['role'])
        serializer.save()
