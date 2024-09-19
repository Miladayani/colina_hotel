from django.urls import path

from .views import payment_process, payment_callback, payment_process_sandbox, payment_callback_sandbox

urlpatterns = [
    path('process/', payment_process, name='payment_process'),
    path('callback/',  payment_callback, name='payment_callback'),
]