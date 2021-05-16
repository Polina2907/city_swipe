from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Card
from .models import UserLocation
from django.contrib.auth.models import User
from geopy.distance import geodesic

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

def endPage(request):
    if request.user.is_authenticated:
        return render(request, "end.html")
    else:
        return render(request, "index.html")

def mapPage(request):
    if request.user.is_authenticated:
        return render(request, "mapPage.html")
    else:
        return render(request, "index.html")

def getCard(request):
    if request.user.is_authenticated:
        user_lat = request.GET['latitude']
        user_lng = request.GET['longtitude']
        user_id = request.user.id
        non_view_cards = Card.objects.exclude(users__id=user_id)
        user = User.objects.get(id=user_id)

        revalant_cards = []
        for card in non_view_cards:
            if getDistance(user_lat, user_lng, card.latitude, card.longitude) <= 1.5:
                revalant_cards.append(card)

        if len(revalant_cards) >= 1:
            card = dict(id = revalant_cards[0].id, title = revalant_cards[0].title, about = revalant_cards[0].about, latitude = revalant_cards[0].latitude, longitude = revalant_cards[0].longitude, photo = revalant_cards[0].photo.url)
            revalant_cards[0].users.add(user)
            return HttpResponse(json.dumps(card), content_type='application/json')
        else:
            return HttpResponse('404', content_type='application/json')
    else:
        return redirect('/city_swipe_app/')

def getUser(request):
    if request.user.is_authenticated:
        user_id = request.user.id
        user_location = UserLocation.objects.filter(user_id=user_id)
        if user_location:
            result = dict(username=request.user.username, longitude = user_location[0].longitude, latitude = user_location[0].latitude)
            return HttpResponse(json.dumps(result), content_type='application/json')
        else:
            return HttpResponse('404', content_type='application/json')
    else:
        return redirect('/city_swipe_app/')

@csrf_exempt
def setUserLocation(request):
    if request.user.is_authenticated:
        user = request.user
        if request.method == 'GET':
            return HttpResponseBadRequest('This is POST method')
        elif request.method == 'POST':
            lat = request.POST['latitude']
            lng = request.POST['longtitude']
            location = UserLocation(user=user, latitude=lat, longitude=lng)
            location.save()
            return HttpResponse('ok', content_type='application/json')
    else:
        return redirect('/city_swipe_app/')

def resetUserLocation(request):
    if request.user.is_authenticated:
        user = request.user
        UserLocation.objects.get(user=user).delete()
        return HttpResponse('ok', content_type='application/json')
    else:
        return redirect('/city_swipe_app/')

@csrf_exempt
def submitAnswer(request):
    if request.user.is_authenticated:
        if request.method == 'GET':
            return HttpResponseBadRequest('This is POST method')
        elif request.method == 'POST':
            card_id = request.POST['card']
            answer = request.POST['answer']

            card = Card.objects.get(id=card_id)

            if answer == 'no_btn':
                card.avg_mark = card.avg_mark - 1
            if answer == 'yes_btn':
                card.avg_mark = card.avg_mark + 1

            card.save()
            return HttpResponse('ok', content_type='application/json')
    else:
        return redirect('/city_swipe_app/')

def getAllCards(request):
    if request.user.is_authenticated:
        allCards = Card.objects.all()
        listOfCards = []
        for card in allCards:
            cardObject = dict(id = card.id, title = card.title, about = card.about, latitude = card.latitude, longitude = card.longitude, photo = card.photo.url, mark = card.avg_mark)
            listOfCards.append(cardObject)
        return HttpResponse(json.dumps(listOfCards), content_type='application/json')
    else:
        return redirect('/city_swipe_app/')

def getDistance(lat1, lng1, lat2, lng2):
    point1 = (lat1, lng1)
    point2 = (lat2, lng2)
    return geodesic(point1, point2).km
