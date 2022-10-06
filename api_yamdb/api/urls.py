from django.urls import path
from rest_framework.routers import SimpleRouter

from .views import (GetTokenView, SendConfirmationCodeView, CommentViewSet,
                    ReviewViewSet)

router = SimpleRouter()
router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='reviews'
)
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments'
)

urlpatterns = [
    path('auth/signup/', SendConfirmationCodeView.as_view()),
    path('', include(router.urls)),
    path(
        'auth/token/',
        GetTokenView.as_view(),
        name='token_obtain'
    ),
]
