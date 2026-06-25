from django.contrib import admin
from .models import Movie, Rating, RatingFeedback, RatingReport

admin.site.register(Movie)
admin.site.register(Rating)
admin.site.register(RatingFeedback)
admin.site.register(RatingReport)