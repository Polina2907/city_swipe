from django.http import HttpResponse
from django.shortcuts import render, redirect
import json
from .models import Card
from django.contrib.auth.models import User

def index(request):
    if request.user.is_authenticated:
        return redirect('/city_swipe_app/instruction')
    else:
        return render(request, "index.html")

def instruction(request):
    return render(request, "instruction.html")

def mainPage(request):
    if request.user.is_authenticated:
        return render(request, "mainPage.html")
    else:
        return render(request, "index.html")

def getCard(request):
    if request.user.is_authenticated:
        cards = []
        user_id = request.user.id
        view_cards = Card.objects.exclude(users__id=user_id)
        user = User.objects.get(id=user_id)

        if len(view_cards) >= 1:
          card = dict(id = view_cards[0].id, name = view_cards[0].title, about = view_cards[0].about, latitude = view_cards[0].latitude, longitude = view_cards[0].longitude, photo = view_cards[0].photo.url)
          view_cards[0].users.add(user)
          return HttpResponse(json.dumps(card), content_type='application/json')
        else:
            return HttpResponse('404', content_type='application/json')

    else:
        return redirect('/city_swipe_app/')
