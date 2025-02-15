
import os
from pathlib import Path
import environ
import requests


BASE_DIR = Path(__file__).resolve().parent.parent

environ.Env.read_env(os.path.join(BASE_DIR, '.env'), True)
env = environ.Env()

def crear_cabecera():
    return {
        'Authorization': 'Bearer ' + env('TOKEN_ACCESO')
    }
def peticion_v1(direccion): 
    return 'http://127.0.0.1:8000/api/v1/' + direccion+'/'
def respuesta(objeto):
    return objeto.json()

class helper :
    
    ################################################
    # OBTENER LISTAS #
    def obtener_categorias():
        headers = crear_cabecera()
        response = requests.get(peticion_v1('categorias'), headers=headers)
        categorias = respuesta(response)
        
        lista_categorias = [("","Ninguna")]
        for categoria in categorias:
            lista_categorias.append((categoria['id'], categoria['nombre']))
        return lista_categorias
    
    def obtener_vendedores():
        headers = crear_cabecera()
        response = requests.get(peticion_v1('vendedores/listar'), headers=headers)
        vendedores = respuesta(response)
        
        lista_vendedores = [("","Ninguno")]
        for vendedor in vendedores:
            lista_vendedores.append((vendedor['id'], vendedor['usuario']['username']))
        return lista_vendedores
    
    def obtener_compradores():
        headers = crear_cabecera()
        response = requests.get(peticion_v1('compradores/listar'), headers=headers)
        compradores = respuesta(response)
        
        lista_compradores = [("","Ninguno")]
        for comprador in compradores:
            lista_compradores.append((comprador['id'], comprador['usuario']['username']))
        return lista_compradores
    
    def obtener_productos():
        headers = crear_cabecera()
        response = requests.get(peticion_v1('productos-mejorado'), headers=headers)
        productos = respuesta(response)
        
        lista_productos = [("","Ninguno")]
        for producto in productos:
            lista_productos.append((producto['id'], producto['nombre']))
        return lista_productos
    
    def obtener_compras():
        headers = crear_cabecera()
        response = requests.get(peticion_v1('compras/listar'), headers=headers)
        compras = respuesta(response)
        
        lista_compras = [("","Ninguna")]
        for compra in compras:
            lista_compras.append((compra['id'], compra['producto']['nombre']))
        return lista_compras
    
    ################################################
    # OBTENER UN SOLO ELEMENTO #
    
    def obtener_producto(id):
        headers = crear_cabecera()
        response = requests.get(peticion_v1('productos/'+str(id)), headers=headers)
        producto = respuesta(response)
        return producto
    
    def obtener_compra(id):
        headers = crear_cabecera()
        response = requests.get(peticion_v1('compras/'+str(id)), headers=headers)
        compra = respuesta(response)
        return compra
    
    def obtener_valoracion(id):
        headers = crear_cabecera()
        response = requests.get(peticion_v1('valoraciones/'+str(id)), headers=headers)
        valoracion = respuesta(response)
        return valoracion