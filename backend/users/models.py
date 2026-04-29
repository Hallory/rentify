from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    class Roles(models.TextChoices):
        TENANT = 'tenant', 'Tenant'
        LANDLORD = 'landlord', 'Landlord'

    email = models.EmailField(unique=True)
    image = models.ImageField(upload_to='user_images/', blank=True)

    role = models.CharField(max_length=20, choices=Roles.choices, default=Roles.TENANT)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ["username"]
    def __str__(self):
        return self.email
    
    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ['date_joined']