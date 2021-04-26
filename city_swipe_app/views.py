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
        id_user = request.user.id
        #all_cards = ""
        user_card = Card.objects.raw('select u.id from auth_user u join users_cards uc on (u.id = uc.id);')
        all_cards = Card.objects.raw('select c.id from Card c join users_cards uc on (c.id != uc.id) join auth_user u on (u.id = uc.id and uc.id = '+ str(id_user) +');')
        # for card in Card.objects.raw('select c.id from Card c join users_cards uc on (c.id != uc.id) join auth_user u on (u.id = uc.id and uc.id = '+ str(id_user) +');'):
        #     all_cards += card.title + ", "
        return HttpResponse(len(user_card))
    else:
        return redirect('/city_swipe_app/')
