from django.shortcuts import render, redirect
import requests
import environ
import os
from pathlib import Path
from .forms import *
from .helper import helper

import json
from requests.exceptions import HTTPError
from django.contrib import messages

BASE_DIR = Path(__file__).resolve().parent.parent

environ.Env.read_env(os.path.join(BASE_DIR, '.env'), True)
env = environ.Env()


def crear_cabecera():
    return {
        'Authorization': 'Bearer ' + env('TOKEN_ACCESO'),
        "Content-Type": "application/json"
    }

def peticion_v1(direccion):
    return 'http://127.0.0.1:8000/api/v1/' + direccion+'/'

def respuesta(objeto):
    return objeto.json()

def index(request):
    return render(request, 'index.html')

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

def valoraciones_listar(request):
    headers = crear_cabecera()
    response = requests.get(peticion_v1('valoraciones/listar'), headers=headers)
    valoraciones = respuesta(response)
    return render(request, 'valoraciones/lista.html', {'valoraciones':valoraciones})

def compras_listar(request):
    headers = crear_cabecera()
    response = requests.get(peticion_v1('compras/listar'), headers=headers)
    compras = respuesta(response)
    return render(request, 'compras/lista.html', {'compras':compras})

#### VIEWS DE USUARIOS ####

def registrar_usuario(request):
    if (request.method == "POST"):
        try:
            formulario = RegistroForm(request.POST)
            if(formulario.is_valid()):
                headers =  {
                            "Content-Type": "application/json" 
                        }
                response = requests.post(
                    'http://127.0.0.1:8000/api/v1/registrar/usuario',
                    headers=headers,
                    data=json.dumps(formulario.cleaned_data)
                )
                
                if(response.status_code == requests.codes.ok):
                    usuario = response.json()
                    token_acceso = helper.obtener_token_session(
                            formulario.cleaned_data.get("username"),
                            formulario.cleaned_data.get("password1")
                            )
                    request.session["usuario"]=usuario
                    request.session["token"] = token_acceso
                    redirect("index")
                else:
                    print(response.status_code)
                    response.raise_for_status()
        except HTTPError as http_err:
            print(f'Hubo un error en la petición: {http_err}')
            if(response.status_code == 400):
                errores = response.json()
                for error in errores:
                    formulario.add_error(error,errores[error])
                return render(request, 
                            'registration/signup.html',
                            {"formulario":formulario})
            else:
                return mi_error_500(request)
        except Exception as err:
            print(f'Ocurrió un error: {err}')
            return mi_error_500(request)
            
    else:
        formulario = RegistroForm()
    return render(request, 'registration/signup.html', {'formulario': formulario})


def login(request):
    if (request.method == "POST"):
        formulario = LoginForm(request.POST)
        try:
            token_acceso = helper.obtener_token_session(
                                formulario.data.get("usuario"),
                                formulario.data.get("password")
                                )
            request.session["token"] = token_acceso
            
          
            headers = {'Authorization': 'Bearer '+token_acceso} 
            response = requests.get('http://127.0.0.1:8000/api/v1/usuario/token/'+token_acceso,headers=headers)
            usuario = response.json()
            request.session["usuario"] = usuario
            
            return  redirect("index")
        except Exception as excepcion:
            print(f'Hubo un error en la petición: {excepcion}')
            formulario.add_error("usuario",excepcion)
            formulario.add_error("password",excepcion)
            return render(request, 
                            'registration/login.html',
                            {"form":formulario})
    else:  
        formulario = LoginForm()
    return render(request, 'registration/login.html', {'form': formulario})

def logout(request):
    del request.session['token']
    return redirect('index')

####otras views####

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

#CRUD ManyToMany con tabla intermedia
def producto_crear(request):
    if (request.method == 'POST'):
        try:
            formulario = ProductoForm(request.POST)
            headers = crear_cabecera()
            datos = formulario.data.copy()
            datos['categorias'] = request.POST.getlist('categorias')          
            response = requests.post(
                                    peticion_v1('productos/crear'),
                                    headers=headers,
                                    data=json.dumps(datos)
                                    )
            if(response.status_code == requests.codes.ok):
                messages.success(request, 'Producto creado exitosamente.')
                return redirect("lista_mejorada")
            else:
                print(response.status_code)
                response.raise_for_status()
        except HTTPError as http_err:
            print(f'Hubo un error en la petición: {http_err}')
            if(response.status_code == 400):
                errores = response.json()
                for error in errores:
                    formulario.add_error(error,errores[error])
                return render(request, 
                            'productos/crear.html',
                            {"formulario":formulario})
            else:
                return mi_error_500(request)
        except Exception as err:
            print(f'Ocurrió un error: {err}')
            return mi_error_500(request)
    else:
        formulario = ProductoForm(None)
    return render(request, 'productos/crear.html', {"formulario":formulario})

def producto_editar(request, producto_id):

    datosFormulario = None
    
    if request.method == "POST":
        datosFormulario = request.POST
    
    producto = helper.obtener_producto(producto_id)
    formulario = ProductoForm(datosFormulario,
                              initial={
                               'nombre': producto['nombre'],
                               'descripcion': producto['descripcion'],
                               'precio': producto['precio'],
                               'estado': producto['estado'],
                                'vendedor': producto['vendedor']['id'],
                                'categorias': [categoria['id'] for categoria in producto['categorias']]
                              }
                            )
    if request.method == 'POST':
        formulario = ProductoForm(request.POST)
        datos = formulario.data.copy()
        datos['categorias'] = request.POST.getlist('categorias')
          
        response = requests.put(
                                peticion_v1('productos/editar/'+str(producto_id)),
                                headers=crear_cabecera(),
                                data=json.dumps(datos)
                                )
        if(response.status_code == requests.codes.ok):
            messages.success(request, 'Producto editado exitosamente.')
            return redirect("lista_mejorada")
        else:
            if(response.status_code == 400):
                errores = response.json()
                for error in errores:
                    formulario.add_error(error,errores[error])
                return render(request, 
                            'productos/editar.html',
                            {"formulario":formulario})
            else:
                return mi_error_500(request)
    return render(request, 'productos/editar.html', {"formulario":formulario, "producto":producto})

def producto_actualizar_nombre(request, producto_id):
    
    datosFormulario = None
    
    if request.method == "POST":
        datosFormulario = request.POST
        
    producto = helper.obtener_producto(producto_id)
    formulario = ProductoActualizarNombreForm(datosFormulario,
                                                  initial={'nombre': producto['nombre']})
        
    if (request.method == 'POST'):
        formulario = ProductoActualizarNombreForm(request.POST)
        if formulario.is_valid():
            headers = crear_cabecera()
            response = requests.patch(peticion_v1('productos/actualizar/'+str(producto_id)), 
                                    headers=headers, 
                                    data=json.dumps(formulario.data))
            if response.status_code == requests.codes.ok:
                messages.success(request, 'Nombre del producto actualizado exitosamente.')
                return redirect("lista_mejorada")
            else:
                print(response.status_code)
                response.raise_for_status()
        else:
            print(formulario.errors)
    return render(request, 'productos/actualizar_nombre.html', {"formulario":formulario, "producto":producto})

def producto_eliminar(request, producto_id):
    try:
        headers = crear_cabecera()
        response = requests.delete(peticion_v1('productos/eliminar/'+str(producto_id)), 
                                headers=headers)
        if( response.status_code == requests.codes.ok):
            messages.success(request, 'Producto eliminado exitosamente.')
            return redirect("lista_mejorada")
        else:
            print(response.status_code)
            response.raise_for_status()
    except Exception as err:
        print(f'Ocurrió un error: {err}')
        return mi_error_500(request)
    return redirect("lista_mejorada")
            

#CRUD ManyToMany con tabla intermedia
def compra_crear(request):
    if (request.method == 'POST'):    
        try:
            formulario = CompraForm(request.POST)
            headers = crear_cabecera()
            datos = formulario.data.copy()
            
            datos['producto'] = request.POST.getlist('producto')

            response = requests.post(
                                    peticion_v1('compras/crear'),
                                    headers=headers,
                                    data=json.dumps(datos)
                                    )
            if(response.status_code == requests.codes.ok):
                messages.success(request, 'Compra creada exitosamente.')
                return redirect("compras_listar")
            else:
                print(response.status_code)
                response.raise_for_status()
        except HTTPError as http_err:
            print(f'Hubo un error en la petición: {http_err}')
            if(response.status_code == 400):
                errores = response.json()
                for error in errores:
                    formulario.add_error(error,errores[error])
                return render(request, 
                            'compras/crear.html',
                            {"formulario":formulario})
            else:
                return mi_error_500(request)
        except Exception as err:
            print(f'Ocurrió un error: {err}')
            return mi_error_500(request)
    else:
        formulario = CompraForm(None)
    return render(request, 'compras/crear.html', {"formulario":formulario})

def compra_editar(request, compra_id):
    
    datosFormulario = None
    
    if request.method == "POST":
        datosFormulario = request.POST
    
    compra = helper.obtener_compra(compra_id)
    formulario = CompraForm(datosFormulario,
                            initial={
                                'total': compra['total'],
                                'garantia': compra['garantia'],
                                'comprador': helper.obtener_compradores(), 
                                'producto': [producto['id'] for producto in compra['producto']]
                            }
                        )
    if request.method == 'POST':
        formulario = CompraForm(request.POST)
        datos = request.POST.copy()
        datos['producto'] = request.POST.getlist('producto')
        datos['comprador'] = request.POST.getlist('comprador')
        response = requests.put(
                                peticion_v1('compras/editar/'+str(compra_id)),
                                headers=crear_cabecera(),
                                data=json.dumps(datos)
                                )
        if(response.status_code == requests.codes.ok):
            messages.success(request, 'Compra editada exitosamente.')
            return redirect("compras_listar")
        else:
            if(response.status_code == 400):
                errores = response.json()
                for error in errores:
                    formulario.add_error(error,errores[error])
                return render(request, 
                            'compras/editar.html',
                            {"formulario":formulario})
            else:
                return mi_error_500(request)
    return render(request, 'compras/editar.html', {"formulario":formulario, "compra":compra})

def compra_actualizar_garantia(request, compra_id):
    
    datosFormulario = None
    
    if request.method == "POST":
        datosFormulario = request.POST
        
    compra = helper.obtener_compra(compra_id)
    formulario = CompraActualizarGarantiaForm(datosFormulario,
                                                 initial={'garantia': compra['garantia']})

    if (request.method == 'POST'):
        formulario = CompraActualizarGarantiaForm(request.POST)
        if formulario.is_valid():
            headers = crear_cabecera()
            response = requests.patch(peticion_v1('compras/actualizar/'+str(compra_id)), 
                                    headers=headers, 
                                    data=json.dumps(formulario.data))
            if response.status_code == requests.codes.ok:
                messages.success(request, 'Garantía de la compra actualizada exitosamente.')
                return redirect("compras_listar")
            else:
                print(response.status_code)
                response.raise_for_status()
        else:
            print(formulario.errors)
    return render(request, 'compras/actualizar_garantia.html', {"formulario":formulario, "compra":compra})


def compra_eliminar(request, compra_id):
    try:
        headers = crear_cabecera()
        response = requests.delete(peticion_v1('compras/eliminar/'+str(compra_id)), 
                                headers=headers)
        if(response.status_code == requests.codes.ok):
            messages.success(request, 'Compra eliminada exitosamente.')
            return redirect("compras_listar")
        else:
            print(response.status_code)
            response.raise_for_status()
    except Exception as err:
        print(f'Ocurrió un error: {err}')
        return mi_error_500(request)
    return redirect("compras_listar")
   
#CRUD ManyToOne
def valoracion_crear(request):
    if(request.method == 'POST'):
        try:
            formulario = ValoracionForm(request.POST)
            headers = crear_cabecera()
            response = requests.post(
                                    peticion_v1('valoraciones/crear'),
                                    headers=headers,
                                    data=json.dumps(formulario.data)
                                    )
            if(response.status_code == requests.codes.ok):
                messages.success(request, 'Valoración creada exitosamente.')
                return redirect("valoraciones_listar")
            else:
                print(response.status_code)
                response.raise_for_status()
        except HTTPError as http_err:
            print(f'Hubo un error en la petición: {http_err}')
            if(response.status_code == 400):
                errores = response.json()
                for error in errores:
                    formulario.add_error(error,errores[error])
                return render(request, 
                            'valoraciones/crear.html',
                            {"formulario":formulario})
            else:
                return mi_error_500(request)
        except Exception as err:
            print(f'Ocurrió un error: {err}')
            return mi_error_500(request)
    else:
        formulario = ValoracionForm(None)
    return render(request, 'valoraciones/crear.html', {"formulario":formulario})
        

def valoracion_editar(request, valoracion_id):
    
    datosFormulario = None
    
    if request.method == "POST":
        datosFormulario = request.POST

    valoracion = helper.obtener_valoracion(valoracion_id)
    formulario = ValoracionForm(datosFormulario,
                                initial={
                                    'puntuacion': valoracion['puntuacion'],
                                    'comentario': valoracion['comentario'],
                                    'usuario': valoracion['usuario']['id'],
                                    'compra': valoracion['compra']['id']
                                }
                            )
    
    if request.method == 'POST':
        formulario = ValoracionForm(request.POST)
        datos = formulario.data.copy()
        response = requests.put(
                                peticion_v1('valoraciones/editar/'+str(valoracion_id)),
                                headers=crear_cabecera(),
                                data=json.dumps(datos)
                                )
        if(response.status_code == requests.codes.ok):
            messages.success(request, 'Valoración editada exitosamente.')
            return redirect("valoraciones_listar")
        else:
            if(response.status_code == 400):
                errores = response.json()
                for error in errores:
                    formulario.add_error(error,errores[error])
                return render(request, 
                            'valoraciones/editar.html',
                            {"formulario":formulario})
            else:
                return mi_error_500(request)
    return render(request, 'valoraciones/editar.html', {"formulario":formulario, "valoracion":valoracion})


def valoracion_actualizar_puntuacion(request, valoracion_id):
    
    datosFormulario = None
    
    if request.method == "POST":
        datosFormulario = request.POST
        
    valoracion = helper.obtener_valoracion(valoracion_id)
    formulario = ValoracionActualizarPuntuacionForm(datosFormulario,
                                                       initial={'puntuacion': valoracion['puntuacion']})

    if (request.method == 'POST'):
        formulario = ValoracionActualizarPuntuacionForm(request.POST)
        if formulario.is_valid():
            headers = crear_cabecera()
            response = requests.patch(peticion_v1('valoraciones/actualizar/'+str(valoracion_id)), 
                                    headers=headers, 
                                    data=json.dumps(formulario.data))
            if response.status_code == requests.codes.ok:
                messages.success(request, 'Puntuación de la valoración actualizada exitosamente.')
                return redirect("valoraciones_listar")
            else:
                print(response.status_code)
                response.raise_for_status()
        else:
            print(formulario.errors)
    return render(request, 'valoraciones/actualizar_puntuacion.html', {"formulario":formulario, "valoracion":valoracion})

def valoracion_eliminar(request, valoracion_id):
    try:
        headers = crear_cabecera()
        response = requests.delete(peticion_v1('valoraciones/eliminar/'+str(valoracion_id)), 
                                headers=headers)
        if(response.status_code == requests.codes.ok):
            messages.success(request, 'Valoración eliminada exitosamente.')
            return redirect("valoraciones_listar")
        else:
            print(response.status_code)
            response.raise_for_status()
    except Exception as err:
        print(f'Ocurrió un error: {err}')
        return mi_error_500(request)
    return redirect("valoraciones_listar")

def mi_error_400(request, exception=None):
    return render(request, 'errores/400.html', None, None, 400)

def mi_error_403(request, exception=None):
    return render(request, 'errores/403.html', None, None, 403)

def mi_error_404(request, exception=None):
    return render(request, 'errores/404.html', None, None, 404)

def mi_error_500(request):
    return render(request, 'errores/500.html', None, None, 500)
