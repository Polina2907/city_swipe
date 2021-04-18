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
        for card in Card.objects.raw('SELECT * FROM Card'): #ЗАПРОС
            return HttpResponse(card.title)
    else:
        return redirect('/city_swipe_app/')
