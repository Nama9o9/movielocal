from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, DetailView, ListView
from .models import Movie, Rating
from .forms import RatingForm
from django.contrib import messages
from django.shortcuts import redirect
# Create your views here.
class MovieListView(ListView):
    model = Movie
    context_object_name = 'all_movies'
    template_name = 'Movies_list.html'

class MovieDetailView(LoginRequiredMixin, DetailView):
    model = Movie
    context_object_name = 'one_movie'
    template_name = 'Movie_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ratings'] = self.object.rating_set.all()
        context['rating_form'] = RatingForm()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = RatingForm(request.POST)

        # Prüfen, ob der User diesen Movie schon bewertet hat
        if Rating.objects.filter(user=request.user, movie=self.object).exists():
            messages.error(request, 'Du hast diesen Movie bereits bewertet.')
            return redirect('movie-detail', pk=self.object.pk)

        if form.is_valid():
            rating = form.save(commit=False)
            rating.user = request.user
            rating.movie = self.object
            rating.save()
            return redirect('movie-detail', pk=self.object.pk)