from django.shortcuts import render, redirect
import requests
from django.core import serializers
import environ
import os
from pathlib import Path
from .forms import *
from requests.exceptions import HTTPError

BASE_DIR = Path(__file__).resolve().parent.parent

environ.Env.read_env(os.path.join(BASE_DIR, '.env'), True)
env = environ.Env()

# Create your views here.
def index(request):
    return render(request, 'index.html')

def crear_cabecera():
    return {
        'Authorization': 'Bearer ' + env('TOKEN_ACCESO')
    }

def peticion_v1(direccion):
    return 'https://mabrala.pythonanywhere.com/api/v1/' + direccion+'/'

def respuesta(objeto):
    return objeto.json()

def productos_listar_api(request):
    headers = crear_cabecera()
    response = requests.get(peticion_v1('productos'), headers=headers)
    productos = respuesta(response)
    return render(request, 'productos/lista_basica.html', {'productos':productos})

def productos_listar_mejorado_api(request):
    headers = crear_cabecera()
    response = requests.get(peticion_v1('productos-mejorado'), headers=headers)
    productos = respuesta(response)
    return render(request, 'productos/lista.html', {'productos':productos})

def producto_buscar_simple(request):
    formulario = BusquedaProductoSimple(request.GET)
    
    if formulario.is_valid():
        headers = crear_cabecera()
        response = requests.get(peticion_v1('productos/buscar_simple'), 
                                headers=headers, 
                                params={'textoBusqueda':formulario.data.get("textoBusqueda")})
        productos = respuesta(response)
        return render(request, 'productos/lista.html', {'productos':productos})
    
    if "HTTP_REFERER" in request.META:
        return redirect(request.META["HTTP_REFERER"])
    else:
        return redirect("index")

def producto_buscar(request):
    if len(request.GET) > 0:
        formulario = BuscarProducto(request.GET)
        try:
            headers = crear_cabecera()
            response = requests.get(peticion_v1('productos/buscar_avanzada'), 
                                    headers=headers, 
                                    params=formulario.data)
            if response.status_code == requests.codes.ok:
                productos = respuesta(response)
                return render(request, 'productos/lista.html', {'productos':productos})
            else:
                print(response.status_code)
                response.raise_for_status()
        except HTTPError as http_err:
            print(f'Hubo un error en la petición: {http_err}')
            if response and response.status_code == 400:
                errores = response.json()
                for error in errores:
                    formulario.add_error(error, errores[error])
                return render(request, 'productos/buscar.html', 
                              {"formulario":formulario, "errores":errores})
            else:
                return mi_error_500(request)
        except Exception as err:
            print(f'Ocurrió un error: {err}')
            return mi_error_500(request)
    else:
        formulario = BuscarProducto(None)
    return render(request, 'productos/buscar.html', {"formulario":formulario})
                
def calzado_listar(request):
    headers = crear_cabecera()
    response = requests.get(peticion_v1('calzados'), headers=headers)
    calzados = respuesta(response)
    return render(request, 'calzados/lista.html', {'calzados':calzados})

def calzado_buscar(request):
    if len(request.GET) > 0:
        formulario = BuscarCalzado(request.GET)
        try:
            headers = crear_cabecera()
            response = requests.get(peticion_v1('calzados/buscar'), 
                                    headers=headers, 
                                    params=formulario.data)
            if response.status_code == requests.codes.ok:
                calzados = respuesta(response)
                return render(request, 'calzados/lista.html', {'calzados':calzados})
            else:
                print(response.status_code)
                response.raise_for_status()
        except HTTPError as http_err:
            print(f'Hubo un error en la petición: {http_err}')
            if response and response.status_code == 400:
                errores = response.json()
                for error in errores:
                    formulario.add_error(error, errores[error])
                return render(request, 'calzados/buscar.html',
                              {"formulario":formulario, "errores":errores})
            else:
                return mi_error_500(request)
        except Exception as err:
            print(f'Ocurrió un error: {err}')
            return mi_error_500(request)
    else:
        formulario = BuscarCalzado(None)
    return render(request, 'calzados/buscar.html', {"formulario":formulario})

def consolas_listar(request):
    headers = crear_cabecera()
    response = requests.get(peticion_v1('consolas'), headers=headers)
    consolas = respuesta(response)
    return render(request, 'consolas/lista.html', {'consolas':consolas})

def consola_buscar(request):
    if len(request.GET) > 0:
        formulario = BuscarConsola(request.GET)
        try:
            headers = crear_cabecera()
            response = requests.get(peticion_v1('consolas/buscar'), 
                                    headers=headers, 
                                    params=formulario.data)
            if response.status_code == requests.codes.ok:
                consolas = respuesta(response)
                return render(request, 'consolas/lista.html', {'consolas':consolas})
            else:
                print(response.status_code)
                response.raise_for_status()
        except HTTPError as http_err:
            print(f'Hubo un error en la petición: {http_err}')
            if response and response.status_code == 400:
                errores = response.json()
                for error in errores:
                    formulario.add_error(error, errores[error])
                return render(request, 'consolas/buscar.html', 
                              {"formulario":formulario, "errores":errores})
            else:
                return mi_error_500(request)
        except Exception as err:
            print(f'Ocurrió un error: {err}')
            return mi_error_500(request)
    else:
        formulario = BuscarConsola(None)
    return render(request, 'consolas/buscar.html', {"formulario":formulario})

def muebles_listar(request):
    headers = crear_cabecera()
    response = requests.get(peticion_v1('muebles'), headers=headers)
    muebles = respuesta(response)
    return render(request, 'muebles/lista.html', {'muebles':muebles})

def mueble_buscar(request):
    if len(request.GET) > 0:
        formulario = BuscarMueble(request.GET)
        try:
            headers = crear_cabecera()
            response = requests.get(peticion_v1('muebles/buscar'), 
                                    headers=headers, 
                                    params=formulario.data)
            if response.status_code == requests.codes.ok:
                muebles = respuesta(response)
                return render(request, 'muebles/lista.html', {'muebles':muebles})
            else:
                print(response.status_code)
                response.raise_for_status()
        except HTTPError as http_err:
            print(f'Hubo un error en la petición: {http_err}')
            if response and response.status_code == 400:
                errores = response.json()
                for error in errores:
                    formulario.add_error(error, errores[error])
                return render(request, 'muebles/buscar.html', 
                              {"formulario":formulario, "errores":errores})
            else:
                return mi_error_500(request)
        except Exception as err:
            print(f'Ocurrió un error: {err}')
            return mi_error_500(request)
    else:
        formulario = BuscarMueble(None)
    return render(request, 'muebles/buscar.html', {"formulario":formulario})

def mi_error_400(request, exception=None):
    return render(request, 'errores/400.html', None, None, 400)

def mi_error_403(request, exception=None):
    return render(request, 'errores/403.html', None, None, 403)

def mi_error_404(request, exception=None):
    return render(request, 'errores/404.html', None, None, 404)

def mi_error_500(request):
    return render(request, 'errores/500.html', None, None, 500)
