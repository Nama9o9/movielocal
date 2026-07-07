from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from Movie.models import Movie, RatingReport
from .forms import MovieForm
from Movie.models import Rating
from .forms import MovieForm, ShopForm
from Shop.models import Shop
from Movie.models import Rating, RatingReport
from django.db import IntegrityError
from .forms import MovieForm, ShopForm, ShopMovieAvailabilityForm
from Shop.models import Shop, ShopMovieAvailability

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
def cs_toggle_rating(request, rating_id):

    if not (request.user.role == 'S' or request.user.is_superuser):
        raise PermissionDenied

    rating = get_object_or_404(Rating, pk=rating_id)
    movie_id = rating.movie.id

    if request.method == 'POST':
        rating.is_active = not rating.is_active
        rating.save()

    return redirect('movie_detail', pk=movie_id)

@login_required
@login_required
def cs_reported_ratings(request):

    if not (request.user.role == 'S' or request.user.is_superuser):
        raise PermissionDenied

    reports = RatingReport.objects.select_related('rating', 'rating__movie', 'rating__user', 'user').order_by('-timestamp')

    return render(request, 'customerservice/reported_ratings.html', {'reports': reports})


@login_required
def cs_dismiss_report(request, report_id):

    if not (request.user.role == 'S' or request.user.is_superuser):
        raise PermissionDenied

    report = get_object_or_404(RatingReport, pk=report_id)

    if request.method == 'POST':
        report.delete()

    return redirect('cs_reported_ratings')

@login_required
def cs_shop_list(request):

    if not (request.user.role == 'S' or request.user.is_superuser):
        raise PermissionDenied

    all_shops = Shop.objects.all()
    return render(request, 'customerservice/shop_list.html', {'all_shops': all_shops})


@login_required
def cs_shop_create(request):

    if not (request.user.role == 'S' or request.user.is_superuser):
        raise PermissionDenied

    if request.method == 'POST':
        form = ShopForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('cs_shop_list')
    else:
        form = ShopForm()

    return render(request, 'customerservice/shop_edit_delete.html', {
        'form': form,
        'can_edit_delete': True,
        'is_create': True
    })


@login_required
def cs_shop_edit_delete(request, pk):

    can_edit_delete = (request.user.role == 'S' or request.user.is_superuser)

    if not can_edit_delete:
        raise PermissionDenied

    shop = get_object_or_404(Shop, pk=pk)

    if request.method == 'POST':
        if 'edit' in request.POST:
            form = ShopForm(request.POST, instance=shop)
            if form.is_valid():
                form.save()
                return redirect('cs_shop_list')
        elif 'delete' in request.POST:
            shop.delete()
            return redirect('cs_shop_list')
    else:
        form = ShopForm(instance=shop)

    context = {
        'form': form,
        'shop': shop,
        'can_edit_delete': can_edit_delete,
        'is_create': False
    }
    return render(request, 'customerservice/shop_edit_delete.html', context)

@login_required
def cs_shop_list(request):

    if not (request.user.role == 'S' or request.user.is_superuser):
        raise PermissionDenied

    if request.method == 'POST' and 'add_availability' in request.POST:
        shop_id = request.POST.get('shop_id')
        shop = get_object_or_404(Shop, pk=shop_id)
        form = ShopMovieAvailabilityForm(request.POST)
        if form.is_valid():
            availability = form.save(commit=False)
            availability.shop = shop
            try:
                availability.save()
            except IntegrityError:
                pass
        return redirect('cs_shop_list')

    elif request.method == 'POST' and 'delete_availability' in request.POST:
        availability_id = request.POST.get('availability_id')
        availability = get_object_or_404(ShopMovieAvailability, pk=availability_id)
        availability.delete()
        return redirect('cs_shop_list')

    all_shops = Shop.objects.all().prefetch_related('shopmovieavailability_set__movie')
    empty_form = ShopMovieAvailabilityForm()

    return render(request, 'customerservice/shop_list.html', {
        'all_shops': all_shops,
        'availability_form': empty_form,
    })