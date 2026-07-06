from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from Movie.models import Movie, RatingReport
from .forms import MovieForm
from Movie.models import Rating

@login_required
def cs_movie_list(request):

    if not (request.user.role == 'S' or request.user.is_superuser):
        raise PermissionDenied

    all_movies = Movie.objects.all()
    return render(request, 'customerservice/movie_list.html', {'all_movies': all_movies})


@login_required
def cs_movie_create(request):

    if not (request.user.role == 'S' or request.user.is_superuser):
        raise PermissionDenied

    if request.method == 'POST':
        form = MovieForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('cs_movie_list')
    else:
        form = MovieForm()

    return render(request, 'customerservice/movie_edit_delete.html', {
        'form': form,
        'can_edit_delete': True,
        'is_create': True
    })


@login_required
def cs_movie_edit_delete(request, pk):

    can_edit_delete = (request.user.role == 'S' or request.user.is_superuser)

    if not can_edit_delete:
        raise PermissionDenied

    movie = get_object_or_404(Movie, pk=pk)

    if request.method == 'POST':
        if 'edit' in request.POST:
            form = MovieForm(request.POST, request.FILES, instance=movie)
            if form.is_valid():
                form.save()
                return redirect('cs_movie_list')
        elif 'delete' in request.POST:
            movie.delete()
            return redirect('cs_movie_list')
    else:
        form = MovieForm(instance=movie)

    context = {
        'form': form,
        'movie': movie,
        'can_edit_delete': can_edit_delete,
        'is_create': False
    }
    return render(request, 'customerservice/movie_edit_delete.html', context)


@login_required
def cs_delete_rating(request, rating_id):

    if not (request.user.role == 'S' or request.user.is_superuser):
        raise PermissionDenied

    rating = get_object_or_404(Rating, pk=rating_id)
    movie_id = rating.movie.id

    if request.method == 'POST':
        rating.delete()


    return redirect('movie_detail', pk=movie_id)

@login_required
def cs_reported_ratings(request):
    if not (request.user.role == 'S' or request.user.is_superuser):
        raise PermissionDenied

    reports = RatingReport.objects.select_related('rating', 'rating__user', 'rating__movie', 'user').all()

    return render(request, 'customerservice/reported_ratings.html', {'reports': reports})