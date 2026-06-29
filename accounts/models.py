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

    @property #damit das ohne Klammern aufgerufen werden kann
    def shopping_cart_item_count(self):
        from shoppingcart.models import ShoppingCart  # Import hier drin, um zirkuläre Imports zu vermeiden
        cart = ShoppingCart.objects.filter(myuser=self).first()
        return cart.get_number_of_items() if cart else 0