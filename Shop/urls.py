from django.urls import path
from . import views

urlpatterns = [
    path('select-shop/<int:movie_pk>/<str:transaction_type>/', views.SelectShopView.as_view(), name='select_shop'),
]