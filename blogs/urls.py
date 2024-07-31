from django.urls import path, include
from . import views

urlpatterns = [
    path('categories', views.BlogCategoryPageView.as_view(), name='blog_category'),
    path('items', views.BlogItemPageView.as_view(), name='blog_item')
]