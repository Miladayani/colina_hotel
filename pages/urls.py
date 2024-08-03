from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.HomePageView.as_view(), name='home'),
    path('home2', views.HomePageView2.as_view(), name='home2'),
    path('home3', views.HomePageView3.as_view(), name='home3'),
    path('aboutus/', views.AboutUsPageView.as_view(), name='aboutus'),
    path('category', views.RoomsCategoryPageView.as_view(), name='category'),
    # path('overview', views.RoomOverviewPageView.as_view(), name='overview'),
    path('404', views.NotFound.as_view(), name='404'),
]