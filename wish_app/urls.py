from django.urls import path
from . import views

urlpatterns= [
    path('', views.index),
    path('register', views.register),
    path('login', views.login),
    path('wishes', views.dashboard),
    path('wishes/new', views.wishes_new),
    path('process_wish', views.process_wish),
    
]