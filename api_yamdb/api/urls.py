from django.urls import include, path
from rest_framework import routers

from api.views import (
    GetTokenView,
    MeViewSet,
    SendConfirmationCodeView,
    UserViewSet)

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

router = routers.DefaultRouter()
router.register(r'users', UserViewSet, basename='user')

urlpatterns = [
    path('users/me/', MeViewSet.as_view({'get': 'retrieve',
                                         'patch': 'partial_update'})),
    path('', include(router.urls)),
    path('auth/signup/', SendConfirmationCodeView.as_view()),
    path('', include(router.urls)),
    path(
        'auth/token/',
        GetTokenView.as_view(),
        name='token_obtain'
    ),
]
