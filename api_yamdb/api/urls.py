from django.urls import path, include
from rest_framework.routers import SimpleRouter

from .views import (
    GetTokenView,
    SendConfirmationCodeView,
    CategoryViewSet,
    GenreViewSet
)

router = SimpleRouter()
router.register('categories', CategoryViewSet)
router.register('genres', GenreViewSet)

urlpatterns = [
    path('auth/signup/', SendConfirmationCodeView.as_view()),
    path(
        'auth/token/',
        GetTokenView.as_view(),
        name='token_obtain'
    ),
    path('', include(router.urls))
]
