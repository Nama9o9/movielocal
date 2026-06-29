
from decimal import Decimal
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.shortcuts import redirect, render, get_object_or_404
from django.views import generic
from django.views.decorators.http import require_POST
from Movie.models import Movie
from Shop.models import Shop, ShopMovieAvailability
# from .forms import PaymentForm
from .models import ShoppingCart, ShoppingCartItem
from datetime import timedelta
from django.utils import timezone
from django.contrib import messages

RENT_PERIOD = 7

def show_shopping_cart(request):
    if request.method == 'POST':
        #damit wenn man ein Item doch nicht kauft, der Stock wieder angepasst wird
        if 'empty' in request.POST:
            shopping_cart = ShoppingCart.objects.get(myuser=request.user)
            items = ShoppingCartItem.objects.filter(shopping_cart=shopping_cart)

            for item in items:
                if item.shop:
                    availability = ShopMovieAvailability.objects.filter(
                        movie_id=item.product_id, shop=item.shop
                    ).first()

                    if availability:
                        if item.transaction_type == 'Purchase':
                            availability.purchase_stock += item.quantity
                        else:
                            availability.rental_stock += item.quantity
                        availability.save()

            shopping_cart.delete()

            context = {'shopping_cart_is_empty': True,
                       'shopping_cart_items': None,
                       'amount': 0.0}
            return render(request, 'shopping_cart.html', context)

        elif 'checkout' in request.POST:
            shopping_cart = ShoppingCart.objects.filter(myuser=request.user).first()

            if shopping_cart:
                total = shopping_cart.get_total()
                items = ShoppingCartItem.objects.filter(shopping_cart=shopping_cart)

                # Daten für die Bestätigungsseite in der Session sichern
                request.session['checkout_total'] = str(total)
                request.session['checkout_items'] = [
                    {
                        'product_name': item.product_name,
                        'shop_name': item.shop.name if item.shop else '-',
                        'transaction_type': item.get_transaction_type_display(),
                        'transaction_type_display': item.get_transaction_type_display(),
                        'price': str(item.price),
                        'due_date': item.due_date.strftime('%d.%m.%Y') if item.due_date else None,

                    }
                    for item in items
                ]

                shopping_cart.delete()

            return redirect('checkout_confirmation')

    else:  # request.method == 'GET'
        shopping_cart_is_empty = True
        shopping_cart_items = None
        total = Decimal(0.0)

        myuser = request.user
        if myuser.is_authenticated:
            shopping_carts = ShoppingCart.objects.filter(myuser=myuser)
            if shopping_carts:
                shopping_cart = shopping_carts.first()
                shopping_cart_is_empty = False
                shopping_cart_items = ShoppingCartItem.objects.filter(shopping_cart=shopping_cart)
                total = shopping_cart.get_total()

        context = {'shopping_cart_is_empty': shopping_cart_is_empty,
                   'shopping_cart_items': shopping_cart_items,
                   'total': total}
        return render(request, 'shopping_cart.html', context)


# @login_required(login_url='/accounts/login/')
# def pay(request):
#     shopping_cart_is_empty = True
#     paid = False
#     form = None
#
#     if request.method == 'POST':
#         myuser = request.user
#         form = PaymentForm(request.POST)
#         form.instance.myuser = myuser
#         if form.is_valid():
#             form.save()
#             paid = True
#
#             # Empty the shopping cart
#             ShoppingCart.objects.get(myuser=myuser).delete()
#         else:
#             print(form.errors)
#
#     else:  # request.method == 'GET'
#         shopping_carts = ShoppingCart.objects.filter(myuser=request.user)
#         if shopping_carts:
#             shopping_cart = shopping_carts.first()
#             shopping_cart_is_empty = False
#             form = PaymentForm(initial={'amount': shopping_cart.get_total()})
#
#     context = {'shopping_cart_is_empty': shopping_cart_is_empty,
#                'payment_form': form,
#                'paid': paid,}
#     return render(request, 'pay.html', context)

@login_required
@require_POST
def add_to_cart(request, movie_pk, shop_pk, transaction_type):
    movie = get_object_or_404(Movie, pk=movie_pk)
    shop = get_object_or_404(Shop, pk=shop_pk)

    with transaction.atomic():
        availability = get_object_or_404(ShopMovieAvailability, movie=movie, shop=shop)

        if transaction_type == 'Purchase':
            item_price = movie.price
            if availability.purchase_stock < 1:
                messages.error(request, 'Dieser Film ist bei diesem Shop nicht mehr zum Kauf verfügbar.')
                return redirect('select_shop', movie_pk=movie.pk, transaction_type=transaction_type)
            availability.purchase_stock -= 1
        else:
            item_price = movie.rental_price
            if availability.rental_stock < 1:
                messages.error(request, 'Dieser Film ist bei diesem Shop nicht mehr zum Ausleihen verfügbar.')
                return redirect('select_shop', movie_pk=movie.pk, transaction_type=transaction_type)
            availability.rental_stock -= 1

        availability.save()

        shopping_carts = ShoppingCart.objects.filter(myuser=request.user)
        shopping_cart = shopping_carts.first() if shopping_carts else ShoppingCart.objects.create(myuser=request.user)

        product_name = f'{movie.title} [{movie.get_fsk_display()}] - [{movie.get_genre_display()}] ({movie.year})'

        due_date = None
        if transaction_type == 'Rental':
            due_date = timezone.now().date() + timedelta(days=RENT_PERIOD)

        ShoppingCartItem.objects.create(
            product_id=movie.id,
            product_name=product_name,
            price=item_price,
            quantity=1,
            shopping_cart=shopping_cart,
            shop=shop,
            transaction_type=transaction_type,
            due_date=due_date,
        )

    return redirect('shopping_cart_show')


class CheckoutConfirmationView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'checkout_confirmation.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total'] = self.request.session.get('checkout_total')
        context['items'] = self.request.session.get('checkout_items', [])
        return context