import datetime
from django.shortcuts import render, redirect
import requests
import environ
import os
from pathlib import Path
from .forms import *
import json
from requests.exceptions import HTTPError

BASE_DIR = Path(__file__).resolve().parent.parent

environ.Env.read_env(os.path.join(BASE_DIR, '.env'), True)
env = environ.Env()

# Create your views here.
def index(request):
    return render(request, 'index.html')

def crear_cabecera():
    return {
        'Authorization': 'Bearer ' + env('TOKEN_ACCESO'),
        "Content-Type": "application/json"
    }

def peticion_v1(direccion):
    return 'http://127.0.0.1:8000/api/v1/' + direccion+'/'

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

#CRUD ManyToMany con tabla intermedia
def producto_crear(request):
    if (request.method == 'POST'):
        try:
            formulario = ProductoForm(request.POST)
            headers = crear_cabecera()
            datos = formulario.data.copy()
            datos['categorias'] = request.POST.getlist('categorias')          
            
            #Creo una copia de la fecha para poder convertirla al mismo formato que el timezone
            fecha_copia = datos['fecha_de_publicacion']
            
            #Convierto la fecha a un formato datetime
            #https://docs.python.org/3/library/datetime.html#datetime.datetime.strptime
            fecha = datetime.datetime.strptime(fecha_copia, '%Y-%m-%dT%H:%M')
            
            #Uso el timezone.mae_aware para convertir la fecha a un formato que pueda ser enviado
            #https://docs.djangoproject.com/en/5.0/ref/utils/#django.utils.timezone.make_aware
            fecha_aware = timezone.make_aware(fecha)
            
            #Paso la fecha a datos
            #https://docs.python.org/3/library/datetime.html#datetime.datetime.strftime
            datos['fecha_de_publicacion'] = fecha_aware.strftime('%Y-%m-%d %H:%M:%S')
            
            response = requests.post(
                                    peticion_v1('productos/crear'),
                                    headers=headers,
                                    data=json.dumps(datos)
                                    )
            if(response.status_code == requests.codes.ok):
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
                               'fecha_de_publicacion': datetime.datetime.strptime(
                                   producto['fecha_de_publicacion'], '%Y-%m-%d %H:%M:%S'),
                                'vendedor': producto['vendedor']['id'],
                                'categorias': [categoria['id'] for categoria in producto['categorias']]
                              }
                            )
    if request.method == 'POST':
        formulario = ProductoForm(request.POST)
        datos = formulario.data.copy()
        datos['categorias'] = request.POST.getlist('categorias')
        
        fecha_copia = request.POST['fecha_de_publicacion']
        fecha = datetime.strptime(fecha_copia, '%Y-%m-%dT%H:%M')
        fecha_aware = timezone.make_aware(fecha)
        datos['fecha_de_publicacion'] = fecha_aware.strftime('%Y-%m-%d %H:%M:%S')
        
        response = requests.put(
                                peticion_v1('productos/editar/'+str(producto_id)),
                                headers=crear_cabecera(),
                                data=json.dumps(datos)
                                )
        if(response.status_code == requests.codes.ok):
            return redirect("lista_mejorada")
        else:
            if(response.status_code == 400):
                errores = response.json()
                for error in errores:
                    formulario.add_error(error,errores[error])
                return render(request, 
                            'productos/crear.html',
                            {"formulario":formulario})
            else:
                return mi_error_500(request)
    return render(request, 'productos/crear.html', {"formulario":formulario})

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
            response = requests.put(peticion_v1('productos/actualizar/'+str(producto_id)), 
                                    headers=headers, 
                                    data=json.dumps(formulario.data))
            if response.status_code == requests.codes.ok:
                return redirect("lista_mejorada")
            else:
                print(response.status_code)
                response.raise_for_status()
        else:
            print(formulario.errors)
    return render(request, 'productos/actualizar_nombre.html', {"formulario":formulario})

def producto_eliminar(request, producto_id):
    try:
        headers = crear_cabecera()
        response = requests.delete(peticion_v1('productos/eliminar/'+str(producto_id)), 
                                headers=headers)
        if( response.status_code == requests.codes.ok):
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
            fecha_copia = datos['fecha_compra']
            fecha = datetime.datetime.strptime(fecha_copia, '%Y-%m-%dT%H:%M')
            fecha_aware = timezone.make_aware(fecha)
            datos['fecha_compra'] = fecha_aware.strftime('%Y-%m-%d %H:%M:%S')
            
            response = requests.post(
                                    peticion_v1('compras/crear'),
                                    headers=headers,
                                    data=json.dumps(datos)
                                    )
            if(response.status_code == requests.codes.ok):
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
                                'fecha_compra': datetime.datetime.strptime(
                                    compra['fecha_compra'], '%Y-%m-%d %H:%M:%S'),
                                'total': compra['total'],
                                'garantia': compra['garantia'],
                                'comprador': compra['comprador']['id'],
                                'producto': [producto['id'] for producto in compra['producto']]
                            }
                        )
    if request.method == 'POST':
        formulario = CompraForm(request.POST)
        datos = formulario.data.copy()
        
        fecha_copia = request.POST['fecha_compra']
        fecha = datetime.strptime(fecha_copia, '%Y-%m-%dT%H:%M')
        fecha_aware = timezone.make_aware(fecha)
        datos['fecha_compra'] = fecha_aware.strftime('%Y-%m-%d %H:%M:%S')
        
        response = requests.put(
                                peticion_v1('compras/editar/'+str(compra_id)),
                                headers=crear_cabecera(),
                                data=json.dumps(datos)
                                )
        if(response.status_code == requests.codes.ok):
            return redirect("lista_mejorada")
        else:
            if(response.status_code == 400):
                errores = response.json()
                for error in errores:
                    formulario.add_error(error,errores[error])
                return render(request, 
                            'compras/crear.html',
                            {"formulario":formulario})
            else:
                return mi_error_500(request)
    return render(request, 'compras/crear.html', {"formulario":formulario})

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
            response = requests.put(peticion_v1('compras/actualizar/'+str(compra_id)), 
                                    headers=headers, 
                                    data=json.dumps(formulario.data))
            if response.status_code == requests.codes.ok:
                return redirect("lista_mejorada")
            else:
                print(response.status_code)
                response.raise_for_status()
        else:
            print(formulario.errors)
    return render(request, 'compras/actualizar_garantia.html', {"formulario":formulario})


def compra_eliminar(request, compra_id):
    try:
        headers = crear_cabecera()
        response = requests.delete(peticion_v1('compras/eliminar/'+str(compra_id)), 
                                headers=headers)
        if( response.status_code == requests.codes.ok):
            return redirect("lista_mejorada")
        else:
            print(response.status_code)
            response.raise_for_status()
    except Exception as err:
        print(f'Ocurrió un error: {err}')
        return mi_error_500(request)
    return redirect("lista_mejorada")
   
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
                                        'fecha_valoracion': datetime.datetime.strptime(
                                            valoracion['fecha_valoracion'], '%Y-%m-%d %H:%M:%S'),
                                        'usuario': valoracion['usuario']['id'],
                                        'compra': valoracion['compra']['id']
                                    }
                                )
    if request.method == 'POST':
        formulario = ValoracionForm(request.POST)
        datos = formulario.data.copy()
        
        fecha_copia = request.POST['fecha_valoracion']
        fecha = datetime.strptime(fecha_copia, '%Y-%m-%dT%H:%M')
        fecha_aware = timezone.make_aware(fecha)
        datos['fecha_valoracion'] = fecha_aware.strftime('%Y-%m-%d %H:%M:%S')
        
        response = requests.put(
                                peticion_v1('valoraciones/editar/'+str(valoracion_id)),
                                headers=crear_cabecera(),
                                data=json.dumps(datos)
                                )
        if(response.status_code == requests.codes.ok):
            return redirect("lista_mejorada")
        else:
            if(response.status_code == 400):
                errores = response.json()
                for error in errores:
                    formulario.add_error(error,errores[error])
                return render(request, 
                            'valoraciones/crear.html',
                            {"formulario":formulario})
            else:
                return mi_error_500(request)
    return render(request, 'valoraciones/crear.html', {"formulario":formulario})


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
            response = requests.put(peticion_v1('valoraciones/actualizar/'+str(valoracion_id)), 
                                    headers=headers, 
                                    data=json.dumps(formulario.data))
            if response.status_code == requests.codes.ok:
                return redirect("lista_mejorada")
            else:
                print(response.status_code)
                response.raise_for_status()
        else:
            print(formulario.errors)
    return render(request, 'valoraciones/actualizar_puntuacion.html', {"formulario":formulario})

def valoracion_eliminar(request, valoracion_id):
    try:
        headers = crear_cabecera()
        response = requests.delete(peticion_v1('valoraciones/eliminar/'+str(valoracion_id)), 
                                headers=headers)
        if(response.status_code == requests.codes.ok):
            return redirect("lista_mejorada")
        else:
            print(response.status_code)
            response.raise_for_status()
    except Exception as err:
        print(f'Ocurrió un error: {err}')
        return mi_error_500(request)
    return redirect("lista_mejorada")

################################################
################################################
##########  OTRAS VIEWS  #######################

################################################
################################################
         
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
                return render(request, 'calzados_lista.html', {'calzados':calzados})
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

def calzado_crear(request):
    if (request.method == 'POST'):
        try:
            formulario = CalzadoForm(request.POST)
            headers = crear_cabecera()
            response = requests.post(
                                    peticion_v1('calzados/crear'),
                                    headers=headers,
                                    data=json.dumps(formulario.data)
            )
            if(response.status_code == requests.codes.ok):
                return redirect("calzado_listar")
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
                            'calzados/crear.html',
                            {"formulario":formulario})
            else:
                return mi_error_500(request)
        except Exception as err:
            return mi_error_500(request)
    else:
        formulario = CalzadoForm(None)
    return render(request, 'calzados/crear.html', {"formulario":formulario})
    

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

def consola_crear(request):
    if (request.method == 'POST'):
        try:
            formulario = ConsolaForm(request.POST)
            headers = crear_cabecera()
            response = requests.post(
                                    peticion_v1('consolas/crear'),
                                    headers=headers,
                                    data=json.dumps(formulario.data)
            )
            if(response.status_code == requests.codes.ok):
                return redirect("consolas_listar")
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
                            'consolas/crear.html',
                            {"formulario":formulario})
            else:
                return mi_error_500(request)
        except Exception as err:
            return mi_error_500(request)
    else:
        formulario = ConsolaForm(None)
    return render(request, 'consolas/crear.html', {"formulario":formulario})

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

def mueble_crear(request):
    if (request.method == 'POST'):
        try:
            formulario = MuebleForm(request.POST)
            headers = crear_cabecera()
            response = requests.post(
                                    peticion_v1('muebles/crear'),
                                    headers=headers,
                                    data=json.dumps(formulario.data)
            )
            if(response.status_code == requests.codes.ok):
                return redirect("muebles_listar")
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
                            'muebles/crear.html',
                            {"formulario":formulario})
            else:
                return mi_error_500(request)
        except Exception as err:
            return mi_error_500(request)
    else:
        formulario = MuebleForm(None)
    return render(request, 'muebles/crear.html', {"formulario":formulario})

def mi_error_400(request, exception=None):
    return render(request, 'errores/400.html', None, None, 400)

def mi_error_403(request, exception=None):
    return render(request, 'errores/403.html', None, None, 403)

def mi_error_404(request, exception=None):
    return render(request, 'errores/404.html', None, None, 404)

def mi_error_500(request):
    return render(request, 'errores/500.html', None, None, 500)
