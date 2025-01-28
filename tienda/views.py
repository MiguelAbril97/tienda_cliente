from django.shortcuts import render
import requests
from django.core import serializers
# Create your views here.

def productos_listar_api(request):
    #El :9090 es el puerto que he usado
    headers = {'Authorization':'Bearer mMekgbftV5GURD3dZNtRSouNWGn9eA'}
    response = requests.get('http://127.0.0.1:9090/api/v1/productos',headers=headers)
    productos = response.json()
    return render(request, 'productos/lista_basica.html',{'productos':productos})

def productos_listar_mejorado_api(request):
    #El :9090 es el puerto que he usado
    headers = {'Authorization':'Bearer mMekgbftV5GURD3dZNtRSouNWGn9eA'}
    response = requests.get('http://127.0.0.1:9090/api/v1/productos-mejorado',headers=headers)
    productos = response.json()
    return render(request, 'productos/lista.html',{'productos':productos})

def calzado_listar(request):
    headers = {'Authorization':'Bearer mMekgbftV5GURD3dZNtRSouNWGn9eA'}
    response = requests.get('http://127.0.0.1:9090/api/v1/calzados',headers=headers)
    calzados = response.json()
    return render(request, 'calzados/lista.html',{'calzados':calzados})

def consolas_listar(request):
    headers = {'Authorization':'Bearer mMekgbftV5GURD3dZNtRSouNWGn9eA'}
    response = requests.get('http://127.0.0.1:9090/api/v1/consolas',headers=headers)
    consolas = response.json()
    return render(request, 'consolas/lista.html',{'consolas':consolas})
