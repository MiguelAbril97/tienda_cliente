from django.shortcuts import render
import requests
from django.core import serializers
# Create your views here.

def productos_listar_api(request):
    #El :9090 es el puerto que he usado
    headers = {'Authorization':'Bearer xRL3Yd0UHwlUR88EdlwkCocsqOZy23'}
    response = requests.get('http://127.0.0.1:9090/api/v1/productos',headers=headers)
    productos = response.json
    return render(request, 'productos/lista.html',{'productos':productos})