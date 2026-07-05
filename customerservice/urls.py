from django.urls import path
from . import views

urlpatterns = [
    path('movies/', views.cs_movie_list, name='cs_movie_list'),
    path('movies/add/', views.cs_movie_create, name='cs_movie_create'),
    path('movies/<int:pk>/manage/', views.cs_movie_edit_delete, name='cs_movie_edit_delete'),
    path('rating/<int:rating_id>/delete/', views.cs_delete_rating, name='cs_delete_rating'),
]