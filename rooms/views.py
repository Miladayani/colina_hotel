from django.shortcuts import render, get_object_or_404, reverse, redirect
from django.views.generic import ListView, DetailView, CreateView

from .models import Room, Comment
from .forms import CommentForm
from cart.forms import AddToCartRoomForm


class RoomsListView(ListView):
    model = Room
    queryset = Room.objects.all()
    template_name = 'rooms/room_list.html'
    context_object_name = 'rooms'


class RoomsDetailView(DetailView):
    model = Room
    template_name = 'rooms/room_detail.html'
    context_object_name = 'room'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['add_to_cart_form'] = AddToCartRoomForm()
        return context


# def add_comment(request, room_id):
#     room = get_object_or_404(Room, id=room_id)
#     if request.method == 'POST':
#         form = CommentForm(request.POST)
#         if form.is_valid():
#             parent_id = request.POST.get('parent_id')
#             print(f"Parent ID: {parent_id}")
#             parent_comment = None
#             if parent_id:
#                 try:
#                     parent_comment = Comment.objects.get(id=parent_id)
#                 except Comment.DoesNotExist:
#                     parent_comment = None
#             comment = Comment(
#                 rooms=room,
#                 author=request.user,
#                 content=form.cleaned_data['content'],
#                 parent=parent_comment
#             )
#             comment.save()
#     return redirect('room_detail', pk=room.id)


class CommentCreateView(CreateView):
    model = Comment
    form_class = CommentForm

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.author = self.request.user

        room_id = int(self.kwargs['room_id'])
        room = get_object_or_404(Room, id=room_id)
        obj.rooms = room

        return super().form_valid(form)
