from django.urls import path

from . import views


urlpatterns = [
    path('', views.RoomsListView.as_view(), name='rooms_list'),
    path('<int:pk>/', views.RoomsDetailView.as_view(), name='room_detail'),
    path('comment/<int:rooms_id>/', views.CommentCreateView.as_view(), name='comment_create'),
]