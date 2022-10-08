from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import (
    CategoryViewSet,
    GenreViewSet,
    GetTokenView,
    MeViewSet,
    SendConfirmationCodeView,
    TitleViewSet,
    UserViewSet,
)

router = SimpleRouter()
router.register('categories', CategoryViewSet)
router.register('genres', GenreViewSet)
router.register('titles', TitleViewSet)
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
    path('', include(router.urls))
]
