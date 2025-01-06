from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    username = models.CharField(max_length=255)  # Add a full name field
    email = models.EmailField(unique=True)

    # Set email as the username field for login
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ["username"]  # Make full name a required field

    def __str__(self) -> str:
        return self.email