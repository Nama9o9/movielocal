from django.urls import path
from . import views

urlpatterns = [
    path('list', views.MovieListView.as_view(), name='movie_list'),
    path('detail/<int:pk>', views.MovieDetailView.as_view(), name='movie_detail'),
    path('rating/<int:rating_pk>/vote/<int:vote_value>/', views.vote_rating, name='vote_rating'),

]