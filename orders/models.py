from django.db import models
from django.conf import settings

from rooms.models import Room


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    is_paid = models.BooleanField(default=False)

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    address = models.CharField(max_length=500)
    order_note = models.CharField(max_length=500, blank=True)

    datetime_created = models.DateTimeField('Created', auto_now_add=True, blank=True)
    datetime_modified = models.DateTimeField('Modified', auto_now=True)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='item')
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='order_item')
    price_per_night = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f'OrderItem {self.id} or order {self.order.id}'