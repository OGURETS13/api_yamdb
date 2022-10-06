from rest_framework import serializers

from reviews.models import User


class UserSerializer(serializers.ModelSerializer):
    confirmation_code = serializers.HiddenField(
        default=''
    )
    role = serializers.CharField(
        read_only=True, default='user'
    )
    password = serializers.CharField(required=False, allow_null=True)

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
