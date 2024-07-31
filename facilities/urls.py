from django.urls import path
from . import views

urlpatterns = [
    path('', views.Facilities.as_view(), name='facilities'),
]