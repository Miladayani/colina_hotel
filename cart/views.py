from datetime import datetime

from django.views.decorators.http import require_POST
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages

# from django.utils.translation import gettext as _

from rooms.models import Room
from .cart import Cart
from .forms import AddToCartRoomForm, BookingForm


def cart_detail_view(request):
    cart = Cart(request)

    for item in cart:
        item['room_update_quantity_form'] = AddToCartRoomForm(initial={
            'quantity': item['quantity'],
            'inplace': True,
        })

    return render(request, 'cart/cart_detail.html', context={'cart': cart})


@require_POST
def add_to_cart_view(request, room_id):
    cart = Cart(request)
    room = get_object_or_404(Room, id=room_id)

    arrival_date = request.POST.get('arrival_date')
    departure_date = request.POST.get('departure_date')
    adults = request.POST.get('adults', 0)
    children = request.POST.get('children', 0)
    infants = request.POST.get('infants', 0)

    # تبدیل تاریخ به رشته
    if arrival_date:
        arrival_date = str(arrival_date)
    if departure_date:
        departure_date = str(departure_date)

    # افزودن به سبد خرید
    cart.add(
        room=room,
        arrival_date=arrival_date,
        departure_date=departure_date,
        adults=adults,
        children=children,
        infants=infants
    )

    return redirect('cart:cart_detail')

# @require_POST
# def add_to_cart_view(request, room_id):
#     cart = Cart(request)
#
#     room = get_object_or_404(Room, id=room_id)
#     form = AddToCartRoomForm(request.POST)
#
#     arrival_date = request.POST.get('arrival_date')
#     departure_date = request.POST.get('departure_date')
#     adults = request.POST.get('adults')
#     children = request.POST.get('children', 0)
#     infants = request.POST.get('infants', 0)
#
#     cart.add(room=room)
#
#     if form.is_valid():
#         cleaned_data = form.cleaned_data
#         # quantity = cleaned_data['quantity']
#         cart.add(room, replace_current_quantity=cleaned_data['inplace'])
#
#     cart.add(room=room, arrival_date=arrival_date, departure_date=departure_date,
#              adults=adults, children=children, infants=infants)
#
#     return redirect('cart:cart_detail')


def remove_from_cart(request, room_id):
    cart = Cart(request)

    room = get_object_or_404(Room, id=room_id)

    cart.remove(room)

    return redirect('cart:cart_detail')


@require_POST
def cart_clear(request):
    cart = Cart(request)

    if len(cart):
        cart.clear()
        messages.success(request, 'Cart cleared')
    else:
        messages.error(request, 'your cart is already empty')

    return redirect('room_list')
