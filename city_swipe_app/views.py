from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import Card

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
        for card in Card.objects.raw('select c.id_card from Card c join usercard uc on (c.id_card != uc.id_card) join users u on (u.id_user = uc.id_user and uc.id_user = 2);'):
            return HttpResponse(card.title)
    else:
        return redirect('/city_swipe_app/')
