from django.contrib import admin

from .models import Card
from .models import UserLocation

admin.site.register(Card)
admin.site.register(UserLocation)
