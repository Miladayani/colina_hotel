from django.urls import path
from . import views

urlpatterns = [
    path('', views.ContactPageView.as_view(), name='contact'),
]