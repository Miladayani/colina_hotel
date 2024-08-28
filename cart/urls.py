from django.urls import path
from .views import cart_detail_view, add_to_cart_view, remove_from_cart, cart_clear


app_name = 'cart'
urlpatterns = [
    path('', cart_detail_view, name='cart_detail'),
    path('add/<int:room_id>/', add_to_cart_view, name='cart_add'),
    path('remove/<int:room_id>/', remove_from_cart, name='remove_to_cart'),
    path('clear', cart_clear, name='cart_clear'),
]