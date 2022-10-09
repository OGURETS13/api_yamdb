from random import randint

import django_filters
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import status, mixins, viewsets, filters, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django_filters.rest_framework import DjangoFilterBackend
from django_filters.rest_framework import filters as django_filters_filters

from reviews.models import User, Category, Genre, Title
from .permissions import IsAdmin, IsAdminOrReadOnly
from .serializers import (
    AuthSerializer,
    CategorySerializer,
    GenreSerializer,
    TitleReadDelSerializer,
    TitleCreateUpdateSerializer,
    UserSerializer,
)


class SendConfirmationCodeView(APIView):
    def post(self, request):
        serializer = AuthSerializer(data=request.data)
        username = request.data.get('username')

        if User.objects.filter(username=username).exists():
            instance = User.objects.get(username=username)
            serializer = UserSerializer(
                instance=instance,
                data=request.data
            )
            return Response(status=status.HTTP_400_BAD_REQUEST)

        if serializer.is_valid():
            confirmation_code = str(randint(100000, 999999))
            email = request.data.get('email')
            send_mail(
                'YAMDB Confirmation code',
                str(request.data['username'] + '\n' + str(confirmation_code)),
                'from@example.com',
                [email],
                fail_silently=False,
            )
            serializer.save(confirmation_code=confirmation_code)

            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetTokenView(APIView):
    def post(self, request):
        username = request.data.get('username')
        confirmation_code = request.data.get('confirmation_code')

        if username is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        try:
            user = get_object_or_404(User, username=username)
            print(user.username)
            if confirmation_code == user.confirmation_code:
                refresh = RefreshToken.for_user(user)
                return Response({
                    'access': str(refresh.access_token),
                })
            return Response(status=status.HTTP_400_BAD_REQUEST)
        except Exception:
            return Response(status=status.HTTP_404_NOT_FOUND)


class CreateListDestroyViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    pass


class CategoryViewSet(CreateListDestroyViewSet):
    permission_classes = (IsAdminOrReadOnly,)
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'slug'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class GenreViewSet(CreateListDestroyViewSet):
    permission_classes = (IsAdminOrReadOnly,)
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    lookup_field = 'slug'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class TitleFilter(django_filters.FilterSet):
    genre = django_filters_filters.CharFilter(field_name='genre__slug')
    category = django_filters_filters.CharFilter(field_name='category__slug')
    name = django_filters_filters.CharFilter(
        field_name='name',
        lookup_expr='icontains'
    )

    class Meta:
        model = Title
        fields = ['year', ]


class TitleViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    queryset = Title.objects.all()
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve', 'destroy'):
            return TitleReadDelSerializer
        return TitleCreateUpdateSerializer


class MeViewSet(viewsets.ViewSet):
    permission_classes = (permissions.IsAuthenticated,)

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
            if 'role' in request.data:
                if me.role == 'admin' or me.is_superuser:
                    serializer.validated_data['role'] \
                        = request.data.get('role')
                else:
                    serializer.validated_data['role'] = me.role
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAdmin,)
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)

    def perform_create(self, serializer):
        if 'role' in self.request.data:
            serializer.save(role=self.request.data['role'])
        serializer.save()
