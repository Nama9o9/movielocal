from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from Movie.models import Movie
from .forms import MovieForm


@login_required
def cs_movie_list(request):
    """Übersicht aller Filme für den Kundenservice"""
    if not (request.user.role == 'S' or request.user.is_superuser):
        raise PermissionDenied

    all_movies = Movie.objects.all()
    return render(request, 'customerservice/movie_list.html', {'all_movies': all_movies})


@login_required
def cs_movie_create(request):
    """View zum Hinzufügen eines neuen Films"""
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
    """Kombinierte View zum Bearbeiten und Löschen eines Films"""
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