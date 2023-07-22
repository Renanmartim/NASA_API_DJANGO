from django.contrib import admin
from django.urls import path
from app1 import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.login1, name='login'),
    path('cadastro', views.cadastro, name='cadastro'),
    path('home', views.home, name='home'),
    path('sair', views.sair, name='sair'),
]
