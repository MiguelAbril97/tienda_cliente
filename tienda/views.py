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

def peticion_v1(direccion):
    return 'https://mabrala.pythonanywhere.com/api/v1/'+direccion

def respuesta (objeto):
    return objeto.json()

def productos_listar_api(request):
    #El :9090 es el puerto que he usado
    headers = {'Authorization':'Bearer '+env('ADMIN')}
    response = requests.get(peticion_v1('productos'),headers=headers)
    productos = respuesta(response)
    return render(request, 'productos/lista_basica.html',{'productos':productos})

def productos_listar_mejorado_api(request):
    #Usando el token del admin
    headers = {'Authorization':'Bearer '+env('ADMIN')}
    response = requests.get(peticion_v1('productos-mejorado'),headers=headers)
    productos = respuesta(response)
    return render(request, 'productos/lista.html',{'productos':productos})

def calzado_listar(request):
    #Usando token para un cliente
    headers = {'Authorization':'Bearer '+env("CLIENTE")}
    response = requests.get(peticion_v1('calzados'),headers=headers)
    calzados = respuesta(response)
    return render(request, 'calzados/lista.html',{'calzados':calzados})

def consolas_listar(request):
    #Usando token para un vendedor
    headers = {'Authorization':'Bearer '+env('VENDEDOR')}
    response = requests.get(peticion_v1('consolas'),headers=headers)
    consolas = respuesta(response)
    return render(request, 'consolas/lista.html',{'consolas':consolas})
