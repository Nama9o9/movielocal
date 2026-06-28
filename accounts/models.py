from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class MyUser(AbstractUser):
    ROLE_CHOICES = ([
        ('C', 'Customer'),
        ('S', 'Staff')
    ])
    profile_pic = models.ImageField(upload_to='profile_pics', null=True, blank=True)
    role = models.CharField(max_length=1, choices=ROLE_CHOICES, default='C')