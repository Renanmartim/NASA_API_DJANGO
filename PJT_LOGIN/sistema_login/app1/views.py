from django.shortcuts import render
from django.http import HttpResponse
from django.contrib import messages
from django.shortcuts import redirect, reverse
from django.contrib.sessions.models import Session
from django.utils import timezone
import json
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
from datetime import datetime
import requests
import json
import webbrowser


def login1(request):
    
    if request.method == 'POST':
        
        username = request.POST["email1"]
        password = request.POST["password1"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            mensagem_erro = "Usuário ou e-mail não existem!"
            return render(request, 'login.html', {'content_erro': mensagem_erro})
        
    return render(request, 'login.html')


def cadastro(request):
    
    if request.method == 'POST':
        
        if User.objects.get(username=request.POST.get('email')):
            mensagem_erro = "Usuário já existe!"
            return render(request, 'cadastro.html', {'content_erro': mensagem_erro})
        
        if request.POST.get('email') or request.POST.get('passwd') is None:
            return redirect('cadastro.html')
        
        else:
            username = request.POST.get("email")
            passwd = request.POST.get("passwd")
            
            user = User.objects.create_user(username=username, password=passwd)
            user.save()
    
    return render(request, 'cadastro.html')


@login_required
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def home(request):
    
    print(request.session.session_key)
    
    if request.method == 'POST':
        
        data = request.POST.get('input')
        
        
    if request.method == 'GET':
        
        data = datetime.today().strftime('%Y-%m-%d')

    
    key = "MSxpmu692i4sF9YkqIdZckYFQBhHosDIB9CGsig2"

    url = "https://api.nasa.gov/planetary/apod"

    parameters = {
            'api_key': key,
            'hd': 'True',
            'date': data
    }

    response = requests.get(url, params=parameters)

    json_data = json.loads(response.text)
    
    try:

        imagem = json_data['hdurl']
        
        sobre = json_data['explanation']
        
    except KeyError:
        
        key = "MSxpmu692i4sF9YkqIdZckYFQBhHosDIB9CGsig2"

        url = "https://api.nasa.gov/planetary/apod"

        parameters = {
                'api_key': key,
                'hd': 'True',
                'date': '2023-01-10'
        }

        response = requests.get(url, params=parameters)

        json_data = json.loads(response.text)
        
        imagem = imagem = json_data['hdurl']
        
        sobre = json_data['explanation']
        
    content = {
        'imagem' : imagem,
        'sobre' : sobre
    }
    
    return render(request, 'home.html', content)


def sair(request):
    
    user = request.session.session_key
    
    session = Session.objects.get(session_key=user)
    session.delete()
    
    return redirect('login')