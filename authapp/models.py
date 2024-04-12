from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import CustomUserManager

class User(AbstractUser):
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'phone']

    objects = CustomUserManager()

    def __str__(self):
        return self.email

class UserDetails(models.Model):
    user = models.ForeignKey(User, related_name='details', on_delete=models.CASCADE)
    age = models.IntegerField()
    dob = models.DateField()
    profession = models.CharField(max_length=100)
    address = models.TextField()
    hobby = models.CharField(max_length=100)
