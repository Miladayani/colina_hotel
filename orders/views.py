from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages

from cart.cart import Cart
from .forms import OrderForm
from .models import OrderItem


@login_required()
def order_create_view(request):
    order_form = OrderForm()
    cart = Cart(request)

    if len(cart) == 0:
        messages.warning(request, 'There are no orders in your cart.')
        return redirect('rooms_list')

    if request.method == 'POST':
        order_form = OrderForm(request.POST)

        if order_form.is_valid():
            order_obj = order_form.save(commit=False)
            order_obj.user = request.user
            order_obj.save()

            for item in cart:
                room = item['room_obj']
                OrderItem.objects.create(
                    order=order_obj,
                    room=room,
                    price_per_night=room.price_per_night,
                )

            cart.clear()

            request.user.first_name = order_obj.first_name
            request.user.last_name = order_obj.last_name
            request.user.save()

    return render(request, 'orders/order_create.html', {
        'form': order_form,
    })
