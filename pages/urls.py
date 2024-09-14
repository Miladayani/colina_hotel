from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.HomePageView.as_view(), name='home'),
    path('home2', views.HomePageView2.as_view(), name='home2'),
    path('aboutus/', views.AboutUsPageView.as_view(), name='aboutus'),
    path('404', views.NotFound.as_view(), name='404'),
]