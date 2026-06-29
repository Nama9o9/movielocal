from django.urls import path
from . import views

urlpatterns = [
    #
    path('show/', views.show_shopping_cart, name='shopping_cart_show'),


    # path('pay/', views.pay, name='shopping_cart_pay'),

path('add_to_cart/<int:movie_pk>/<int:shop_pk>/<str:transaction_type>/', views.add_to_cart, name='add_to_cart'),
path('checkout/confirmation/', views.CheckoutConfirmationView.as_view(), name='checkout_confirmation'),]