from django.contrib import admin
from reviews.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    pass