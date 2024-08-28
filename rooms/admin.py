from django.contrib import admin

from .models import Room, Comment, Booking


class CommentsInline(admin.TabularInline):
    model = Comment
    fields = ('body', 'author', 'active')
    extra = 1


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('name', 'price_per_night', 'active')

    inlines = [
        CommentsInline,
    ]


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'room', 'arrival_date', 'departure_date']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('rooms', 'body', 'author', 'active')

