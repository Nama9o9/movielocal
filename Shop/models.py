from django.db import models

from Movie.models import Movie


# Create your models here.
class Shop(models.Model):
    name = models.CharField(max_length=100)
    adress = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class ShopMovieAvailability(models.Model):
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    purchase_stock = models.PositiveIntegerField(default=0)
    rental_stock = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ('shop', 'movie')

    def __str__(self):
        return f'{self.movie.title} @ {self.shop.name}'