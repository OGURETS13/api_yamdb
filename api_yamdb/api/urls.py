from django.urls import path, include
from rest_framework.routers import SimpleRouter

from .views import (
    GetTokenView,
    SendConfirmationCodeView,
    CategoryViewSet,
    GenreViewSet,
    TitleViewSet
)

router = SimpleRouter()
router.register('categories', CategoryViewSet)
router.register('genres', GenreViewSet)
router.register('titles', TitleViewSet)

urlpatterns = [
    path('auth/signup/', SendConfirmationCodeView.as_view()),
    path(
        'auth/token/',
        GetTokenView.as_view(),
        name='token_obtain'
    ),
    path('', include(router.urls))
]
