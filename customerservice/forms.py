from django import forms
from Movie.models import Movie

class MovieForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = [
            'title', 'description', 'fsk', 'genre', 'year',
            'director', 'time', 'actors', 'price', 'rental_price',
            'details_pdf', 'movie_pic'
        ]