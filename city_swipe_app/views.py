from django.http import HttpResponse
from django.shortcuts import render
#from .models import Card

def index(request):
    context = {
        'cards': "WELCOME!"
        if request.user.is_authenticated else []
    }
    return render(request, "index.html")

def instruction(request):
    return render(request, "instruction.html")
