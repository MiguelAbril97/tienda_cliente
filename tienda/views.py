from django.shortcuts import render
import requests
from django.core import serializers
import environ
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

environ.Env.read_env(os.path.join(BASE_DIR, '.env'),True)
env = environ.Env()

# Create your views here.
def index(request):
    return render(request,'index.html')

def productos_listar_api(request):
    #El :9090 es el puerto que he usado
    headers = {'Authorization':'Bearer '+env('ADMIN')}
    response = requests.get('http://127.0.0.1:9090/api/v1/productos',headers=headers)
    productos = response.json()
    return render(request, 'productos/lista_basica.html',{'productos':productos})

def productos_listar_mejorado_api(request):
    #Usando el token del admin
    headers = {'Authorization':'Bearer '+env('ADMIN')}
    response = requests.get('http://127.0.0.1:9090/api/v1/productos-mejorado',headers=headers)
    productos = response.json()
    return render(request, 'productos/lista.html',{'productos':productos})

def calzado_listar(request):
    #Usando token para un cliente
    headers = {'Authorization':'Bearer '+env("CLIENTE")}
    response = requests.get('http://127.0.0.1:9090/api/v1/calzados',headers=headers)
    calzados = response.json()
    return render(request, 'calzados/lista.html',{'calzados':calzados})

def consolas_listar(request):
    #Usando token para un vendedor
    headers = {'Authorization':'Bearer '+env('VENDEDOR')}
    response = requests.get('http://127.0.0.1:9090/api/v1/consolas',headers=headers)
    consolas = response.json()
    return render(request, 'consolas/lista.html',{'consolas':consolas})
