from django.urls import path
from . import views

urlpatterns = [
    path('movies/', views.cs_movie_list, name='cs_movie_list'),
    path('movies/add/', views.cs_movie_create, name='cs_movie_create'),
    path('movies/<int:pk>/manage/', views.cs_movie_edit_delete, name='cs_movie_edit_delete'),
    path('rating/<int:rating_id>/delete/', views.cs_delete_rating, name='cs_delete_rating'),
    path('rating/<int:rating_id>/toggle/', views.cs_toggle_rating, name='cs_toggle_rating'),
path('reported-ratings/', views.cs_reported_ratings, name='cs_reported_ratings'),
    path('reported-ratings/<int:report_id>/dismiss/', views.cs_dismiss_report, name='cs_dismiss_report'),
    path('shops/', views.cs_shop_list, name='cs_shop_list'),
    path('shops/add/', views.cs_shop_create, name='cs_shop_create'),
    path('shops/<int:pk>/manage/', views.cs_shop_edit_delete, name='cs_shop_edit_delete'),
]