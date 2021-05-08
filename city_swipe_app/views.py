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
        user_id = request.user.id
        non_viewed_cards = Card.objects.exclude(users__id=user_id) #получаем все карточки, которые не видел пользователь
        user = User.objects.get(id=user_id) #получаем айди юзера get=select

        if len(non_viewed_cards) >= 1:
          card = dict(id = non_viewed_cards[0].id, name = non_viewed_cards[0].title, about = non_viewed_cards[0].about, latitude = non_viewed_cards[0].latitude, longitude = non_viewed_cards[0].longitude, photo = non_viewed_cards[0].photo.url)
          non_viewed_cards[0].users.add(user) #добавление юзера к карточке
          return HttpResponse(json.dumps(card), content_type='application/json')
        else:
            return HttpResponse('404', content_type='application/json')

    else:
        return redirect('/city_swipe_app/')

def submit(request):
    if request.user.is_authenticated:
        card_id = request.POST['card_id']
        answer = request.POST['answer']

