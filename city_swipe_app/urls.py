from django.conf.urls import url
from django.urls import path
from . import views
from .views import getCard

app_name = 'city_swipe_app'

urlpatterns = [
    url(r'^$', views.index, name='index'), #r-regexp, name-название представления, views.index - место где определили урл
    path('instruction/', views.instruction, name='instruction'),
    path('mainPage/', views.mainPage, name='mainPage'),
    path('getCard/', views.getCard, name='getCard'),
]
