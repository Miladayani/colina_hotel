from datetime import datetime
from bs4 import BeautifulSoup

from django.views.decorators.http import require_POST
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages

# from django.utils.translation import gettext as _

from rooms.models import Room
from .cart import Cart
from .forms import AddToCartRoomForm


def cart_detail_view(request):
    cart = Cart(request)

    for item in cart:
        item['room_update_quantity_form'] = AddToCartRoomForm(initial={
            'quantity': item['quantity'],
            'inplace': True,
        })

    total_sum = sum(item['totally_price'] for item in cart.cart.values())

    return render(request, 'cart/cart_detail.html', context={'cart': cart, 'total_sum': total_sum})


@require_POST
def add_to_cart_view(request, room_id):
    cart = Cart(request)
    room = get_object_or_404(Room, id=room_id)

    arrival_date = request.POST.get('arrival_date')
    departure_date = request.POST.get('departure_date')
    adults = request.POST.get('adults', 0)
    children = request.POST.get('children', 0)
    infants = request.POST.get('infants', 0)

    # تبدیل تاریخ‌ها به فرمت دلخواه
    arrival_date_str = request.POST.get('arrival_date')
    departure_date_str = request.POST.get('departure_date')

    soup_arrival = BeautifulSoup(arrival_date_str, 'html.parser')
    soup_departure = BeautifulSoup(departure_date_str, 'html.parser')

    day_arrival = soup_arrival.find('span', {'class': 'day'}).text
    month_arrival = soup_arrival.find('span', {'class': 'month'}).text
    year_arrival = soup_arrival.find('span', {'class': 'year'}).text

    day_departure = soup_departure.find('span', {'class': 'day'}).text
    month_departure = soup_departure.find('span', {'class': 'month'}).text
    year_departure = soup_departure.find('span', {'class': 'year'}).text

    arrival_date = f"{year_arrival}-{month_arrival}-{day_arrival}"
    departure_date = f"{year_departure}-{month_departure}-{day_departure}"

    arrival_date = datetime.strptime(arrival_date, "%Y-%b-%d")
    departure_date = datetime.strptime(departure_date, "%Y-%b-%d")

    # تبدیل به رشته برای سریال‌سازی در JSON
    arrival_date_str = arrival_date.strftime("%Y-%m-%d")
    departure_date_str = departure_date.strftime("%Y-%m-%d")

    # محاسبه تعداد شب‌ها
    nights = (departure_date - arrival_date).days

    # محاسبه قیمت کل
    totally_price = room.price_per_night * nights

    # افزودن به سبد خرید
    cart.add(
        room=room,
        arrival_date=arrival_date_str,
        departure_date=departure_date_str,
        adults=adults,
        children=children,
        infants=infants,
        totally_price=totally_price,
        nights=nights
    )
    return redirect('cart:cart_detail')


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
