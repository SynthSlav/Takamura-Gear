from django.contrib import admin
from .models import UserProfile

# Register your models here.


class UserProfileAdmin(admin.ModelAdmin):
    """
    Admin interface for UserProfile model
    """

    list_display = (
        "user",
        "default_phone_number",
        "default_town_or_city",
        "default_country",
    )

    ordering = ("user",)


admin.site.register(UserProfile, UserProfileAdmin)
