from .views import *
class helper :
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
        response = requests.get(peticion_v1('vendedores'), headers=headers)
        vendedores = respuesta(response)
        
        lista_vendedores = [("","Ninguno")]
        for vendedor in vendedores:
            lista_vendedores.append((vendedor['id'], vendedor['username']))
        return lista_vendedores