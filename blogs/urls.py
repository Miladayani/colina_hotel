from django.urls import path, include
from . import views

urlpatterns = [
    path('items', views.BlogItemPageView.as_view(), name='blog_item')
]