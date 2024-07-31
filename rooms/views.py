from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView

from .models import Room, Comment
from .forms import CommentForm


class RoomsListView(ListView):
    model = Room
    queryset = Room.objects.all()
    template_name = 'rooms/room_list.html'
    context_object_name = 'rooms'

#
# class RoomsDetailView(DetailView):
#     model = Room
#     template_name = 'rooms/room_detail.html'
#     context_object_name = 'room'


class CommentCreateView(CreateView):
    model = Comment
    form_class = CommentForm

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.author = self.request.user

        rooms_id = int(self.kwargs['rooms_id'])
        product = get_object_or_404(Room, id=rooms_id)
        obj.product = product

        return super().form_valid(form)
