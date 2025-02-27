import os
from pathlib import Path
import environ
import requests

BASE_DIR = Path(__file__).resolve().parent.parent

environ.Env.read_env(os.path.join(BASE_DIR, '.env'), True)
env = environ.Env()

class helper:
    
    def obtener_token_session(usuario, password):
        token_url = 'http://127.0.0.1:8000/oauth2/token/'
        data = {
            'grant_type': 'password',
            'username': usuario,
            'password': password,
            'client_id': env('CLIENT_ID'),
            'client_secret': env('CLIENT_SECRET'),
        }

        response = requests.post(token_url, data=data)
        respuesta = response.json()
        if response.status_code == 200:
            return respuesta.get('access_token')
        else:
            raise Exception(respuesta.get("error_description"))

    # OBTENER LISTAS #
    def obtener_categorias():
        headers = {'Authorization': 'Bearer ' + env('TOKEN_ACCESO')}
        response = requests.get('http://127.0.0.1:8000/api/v1/categorias/', headers=headers)
        categorias = response.json()

        lista_categorias = [("", "Ninguna")]
        for categoria in categorias:
            lista_categorias.append((categoria['id'], categoria['nombre']))
        return lista_categorias

    def obtener_vendedores():
        headers = {'Authorization': 'Bearer ' + env('TOKEN_ACCESO')}
        response = requests.get('http://127.0.0.1:8000/api/v1/vendedores/listar/', headers=headers)
        vendedores = response.json()

        lista_vendedores = [("", "Ninguno")]
        for vendedor in vendedores:
            lista_vendedores.append((vendedor['id'], vendedor['usuario']['username']))
        return lista_vendedores

    def obtener_compradores():
        headers = {'Authorization': 'Bearer ' + env('TOKEN_ACCESO')}
        response = requests.get('http://127.0.0.1:8000/api/v1/compradores/listar/', headers=headers)
        compradores = response.json()

        lista_compradores = [("", "Ninguno")]
        for comprador in compradores:
            lista_compradores.append((comprador['id'], comprador['usuario']['username']))
        return lista_compradores

    def obtener_productos():
        headers = {'Authorization': 'Bearer ' + env('TOKEN_ACCESO')}
        response = requests.get('http://127.0.0.1:8000/api/v1/productos-mejorado/', headers=headers)
        productos = response.json()

        lista_productos = [("", "Ninguno")]
        for producto in productos:
            lista_productos.append((producto['id'], producto['nombre']))
        return lista_productos

    def obtener_compras():
        headers = {'Authorization': 'Bearer ' + env('TOKEN_ACCESO')}
        response = requests.get('http://127.0.0.1:8000/api/v1/compras/listar/', headers=headers)
        compras = response.json()

        lista_compras = [("", "Ninguna")]
        for compra in compras:
            nombres_productos = ", ".join([producto['nombre'] for producto in compra['producto']])
            lista_compras.append((compra['id'], f"Compra {compra['id']} - {nombres_productos}"))
        return lista_compras

    # OBTENER UN SOLO ELEMENTO #
    def obtener_producto(id):
        headers = {'Authorization': 'Bearer ' + env('TOKEN_ACCESO')}
        response = requests.get(f'http://127.0.0.1:8000/api/v1/productos/'+str(id)+'/', headers=headers)
        producto = response.json()
        return producto

    def obtener_compra(id):
        headers = {'Authorization': 'Bearer ' + env('TOKEN_ACCESO')}
        response = requests.get(f'http://127.0.0.1:8000/api/v1/compras/'+str(id)+'/', headers=headers)
        compra = response.json()
        return compra

    def obtener_valoracion(id):
        headers = {'Authorization': 'Bearer ' + env('TOKEN_ACCESO')}
        response = requests.get(f'http://127.0.0.1:8000/api/v1/valoraciones/'+str(id)+'/', headers=headers)
        valoracion = response.json()
        return valoracion

