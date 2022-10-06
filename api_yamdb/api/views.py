from random import randint

from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .permissions import AdminModeratorAuthorPermission
from reviews.models import Review, User
from .serializers import CommentSerializer, ReviewSerializer, UserSerializer


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


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (AdminModeratorAuthorPermission,)

    def get_queryset(self):
        review = get_object_or_404(
            Review,
            id=self.kwargs.get('review_id'))
        return review.comments.all()

    def perform_create(self, serializer):
        review = get_object_or_404(
            Review,
            id=self.kwargs.get('review_id'))
        serializer.save(author=self.request.user, review=review)


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (AdminModeratorAuthorPermission,)

    def get_queryset(self):
        title = get_object_or_404(
            Title,
            id=self.kwargs.get('title_id'))
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(
            Title,
            id=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)
