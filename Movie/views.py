from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q
from django.views.generic import CreateView, DetailView, ListView, UpdateView, DeleteView
from django.urls import reverse
from .models import Movie, Rating, RatingFeedback, RatingReport
from .forms import RatingForm
from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

# Create your views here.
class MovieListView(ListView):
    model = Movie
    context_object_name = 'all_movies'
    template_name = 'Movies_list.html'

    def get_queryset(self):
        query = self.request.GET.get('q', '')
        fsk = self.request.GET.get('fsk', '')
        genre = self.request.GET.get('genre', '')

        movies = Movie.objects.all()

        if query:
            movies = movies.filter(
                Q(title__contains=query) |
                Q(director__contains=query) |
                Q(actors__contains=query)
            )

        if fsk:
            movies = movies.filter(fsk=int(fsk))

        if genre:
            movies = movies.filter(genre=genre)

        return movies



    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q', '')
        context['selected_fsk'] = self.request.GET.get('fsk', '')
        context['selected_genre'] = self.request.GET.get('genre', '')
        return context

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
            return redirect('movie_detail', pk=self.object.pk)

        if form.is_valid():
            rating = form.save(commit=False)
            rating.user = request.user
            rating.movie = self.object
            rating.save()

            return redirect('movie_detail', pk=self.object.pk)

@login_required
@require_POST
def vote_rating(request, rating_pk, vote_value):
    rating = get_object_or_404(Rating, pk=rating_pk)

    # Nutzer kann eigene Bewertung nicht voten
    if rating.user == request.user:
        messages.error(request, 'Du kannst deine eigene Bewertung nicht bewerten.')
        return redirect('movie_detail', pk=rating.movie.pk)

    feedback, created = RatingFeedback.objects.get_or_create(
        user=request.user,
        rating=rating,
        defaults={'vote': vote_value}
    )

    if not created:
        # Vote schon vorhanden -> aktualisieren (z.B. von Upvote auf Downvote wechseln)
        feedback.vote = vote_value
        feedback.save()

    return redirect('movie_detail', pk=rating.movie.pk)

class RatingUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Rating
    form_class = RatingForm
    template_name = 'Rating_edit_form.html'

    def test_func(self):
        # Stellt sicher, dass nur der Ersteller die Bewertung bearbeiten kann
        rating = self.get_object()
        return rating.user == self.request.user

    def handle_no_permission(self):
        messages.error(self.request, 'Du kannst nur deine eigenen Bewertungen bearbeiten.')
        return redirect('movie_detail', pk=self.get_object().movie.pk)

    def get_success_url(self):
        return reverse('movie_detail', kwargs={'pk': self.object.movie.pk})


class RatingDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Rating
    template_name = 'Rating_confirm_delete.html'

    def test_func(self):
        rating = self.get_object()
        return rating.user == self.request.user

    def handle_no_permission(self):
        messages.error(self.request, 'Du kannst nur deine eigenen Bewertungen löschen.')
        return redirect('movie_detail', pk=self.get_object().movie.pk)

    def get_success_url(self):
        return reverse('movie_detail', kwargs={'pk': self.object.movie.pk})


@login_required
@require_POST
def report_rating(request, rating_pk):
    rating = get_object_or_404(Rating, pk=rating_pk)

    # Eigene Bewertung kann man nicht melden
    if rating.user == request.user:
        messages.error(request, 'Du kannst deine eigene Bewertung nicht melden.')
        return redirect('movie_detail', pk=rating.movie.pk)

    # Prüfen ob schon gemeldet
    if RatingReport.objects.filter(user=request.user, rating=rating).exists():
        messages.error(request, 'Du hast diese Bewertung bereits gemeldet.')
        return redirect('movie_detail', pk=rating.movie.pk)

    reason = request.POST.get('reason', '')
    RatingReport.objects.create(
        user=request.user,
        rating=rating,
        reason=reason,
    )
    messages.success(request, 'Bewertung wurde gemeldet.')
    return redirect('movie_detail', pk=rating.movie.pk)