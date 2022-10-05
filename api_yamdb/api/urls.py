from django.urls import path

from .views import GetTokenView, SendConfirmationCodeView


urlpatterns = [
    path('auth/signup/', SendConfirmationCodeView.as_view()),
    path(
        'auth/token/',
        GetTokenView.as_view(),
        name='token_obtain'
    ),
]
