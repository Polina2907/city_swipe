from django.db import models
from django.contrib.auth.models import User

class Card(models.Model):
    title = models.CharField(max_length=255, default='')
    about = models.CharField(max_length=255, default='')
    photo = models.ImageField()
    avg_mark = models.IntegerField(default=0)
    latitude = models.FloatField(default=50.908407)#широта
    longitude = models.FloatField(default=34.795837)#долгота

# class AppUser(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     seenCards = models.JSONField()