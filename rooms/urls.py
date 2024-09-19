from django.urls import path
from .views import RoomsDetailView, CommentCreateView

from . import views


urlpatterns = [
    path('', views.RoomsListView.as_view(), name='rooms_list'),
    path('<int:pk>/', RoomsDetailView.as_view(), name='room_detail'),
    path('comment/<int:room_id>/', CommentCreateView.as_view(), name='comment_create'),
]