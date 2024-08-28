from django.db import models
from django.shortcuts import reverse
from django.contrib.auth import get_user_model


class Room(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    price_per_night = models.PositiveIntegerField()
    image = models.ImageField(upload_to='room/room_cover', blank=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('room_detail', args={self.pk})


class Booking(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.PROTECT)
    room = models.ForeignKey(Room, on_delete=models.PROTECT)
    arrival_date = models.DateField()
    departure_date = models.DateField()

    # guests = models.PositiveIntegerField()
    adults = models.PositiveIntegerField(default=0)
    children = models.PositiveIntegerField(default=0)
    infants = models.PositiveIntegerField(default=0)

    date_created = models.DateTimeField(auto_now_add=True, )

    def __str__(self):
        return f'{self.room.name} booked by {self.user} from {self.arrival_date} to {self.departure_date}'


class ActiveCommentManager(models.Manager):
    def get_queryset(self):
        return super(ActiveCommentManager, self).get_queryset().filter(active=True)


class Comment(models.Model):
    rooms = models.ForeignKey(Room, on_delete=models.CASCADE)
    author = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name='comments',
    )
    body = models.TextField()
    date_created = models.DateField(auto_now_add=True,)
    date_modified = models.DateField(auto_now=True)
    active = models.BooleanField(default=True,)

    objects = models.Manager()
    active_comments_manager = ActiveCommentManager()
