from django import forms
from Movie.models import Movie
from Shop.models import Shop, ShopMovieAvailability

class MovieForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = [
            'title', 'description', 'fsk', 'genre', 'year',
            'director', 'time', 'actors', 'price', 'rental_price',
            'details_pdf', 'movie_pic'
        ]


class ShopForm(forms.ModelForm):
    class Meta:
        model = Shop
        fields = ['name', 'adress']


class ShopMovieAvailabilityForm(forms.ModelForm):
    class Meta:
        model = ShopMovieAvailability
        fields = ['movie', 'purchase_stock', 'rental_stock']