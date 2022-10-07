from rest_framework import serializers

from reviews.models import User


class UserSerializer(serializers.ModelSerializer):
    confirmation_code = serializers.CharField(
        default=''
    )
    serializers.ChoiceField(
        read_only=True,
        choices=['user', 'moderator', 'admin'],
    )
    password = serializers.HiddenField(
        default='',
        required=False,
        allow_null=True
    )

    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'password',
            'confirmation_code',
            'role',
            'email',
            'bio',
        )
        lookup_field = 'username'
