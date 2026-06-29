from django.shortcuts import render

# Create your views here.
from django.views import generic
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Movie, ShopMovieAvailability


class SelectShopView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'Shop_Choice.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        movie = get_object_or_404(Movie, pk=self.kwargs['movie_pk'])
        transaction_type = self.kwargs['transaction_type']

        if transaction_type == 'Purchase':
            availabilities = ShopMovieAvailability.objects.filter(movie=movie, purchase_stock__gt=0)
        else:
            availabilities = ShopMovieAvailability.objects.filter(movie=movie, rental_stock__gt=0)

        context['movie'] = movie
        context['transaction_type'] = transaction_type
        context['availabilities'] = availabilities
        return context