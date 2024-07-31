from django.urls import path

from .views import RoomsListView, CommentCreateView

urlpatterns = [
    path('', RoomsListView.as_view(), name='rooms_list'),
    # path('room/<int:pk>/', RoomsDetailView.as_view(), name='room_detail'),
    path('comment/<int:rooms_id>/', CommentCreateView.as_view(), name='comment_create'),
]