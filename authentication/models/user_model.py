from django.contrib.gis.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
)
from authentication.models.user_manager import UserManager


USER_TYPE = [
    ("MEDICAL STORE", "MEDICAL STORE"),
    ("AMBULANCE", "AMBULANCE"),
    ("BLOOD BANK", "BLOOD BANK"),
    ("USER", "USER"),
]


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=255, blank=True)
    email = models.EmailField(max_length=255, db_index=True, unique=True)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    user_type = models.CharField(max_length=15, choices=USER_TYPE)

    class Meta:
        unique_together = ("email", "user_type")
        app_label = "authentication"

    USERNAME_FIELD = "email"

    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email
