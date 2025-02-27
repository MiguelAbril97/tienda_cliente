from django.urls import path,re_path
from .import views

    
urlpatterns = [
    path('',views.index, name='index'),
    
    path('registrar',views.registrar_usuario,name='registrar_usuario'),
    path('login',views.login,name='login'),
    path('logout',views.logout,name='logout'),
    
    path('productos/',views.productos_listar_api,name='lista_basica'),
    path('productos-mejorado/',views.productos_listar_mejorado_api,name='lista_mejorada'),
    path('productos/buscar_simple/',views.producto_buscar_simple,name='productos_buscar_simple'),
    path('productos/buscar_avanzada/',views.producto_buscar,name='productos_buscar'),
    
    ### PRODUCTOS CRUD
    path('productos/crear/',views.producto_crear,name='productos_crear'),
    path('productos/editar/<int:producto_id>/',views.producto_editar,name='productos_editar'),
    path('productos/actualizar/<int:producto_id>/',views.producto_actualizar_nombre,name='productos_actualizar'),
    path('productos/eliminar/<int:producto_id>/',views.producto_eliminar,name='productos_eliminar'),
    
    ####CRUD COMPRA
    path('compras/listar/',views.compras_listar,name='compras_listar'),
    path('compras/crear/',views.compra_crear,name='compras_crear'),
    path('compras/editar/<int:compra_id>/',views.compra_editar,name='compras_editar'),
    path('compras/actualizar/<int:compra_id>/',views.compra_actualizar_garantia,name='compras_actualizar_garantia'),
    path('compras/eliminar/<int:compra_id>/',views.compra_eliminar,name='compras_eliminar'),
    
    ### crud valoraciones
    path('valoraciones/listar/',views.valoraciones_listar,name='valoraciones_listar'),
    path('valoraciones/crear/',views.valoracion_crear,name='valoraciones_crear'),
    path('valoraciones/editar/<int:valoracion_id>/',views.valoracion_editar,name='valoraciones_editar'),
    path('valoraciones/actualizar/<int:valoracion_id>/',views.valoracion_actualizar_puntuacion,name='valoraciones_actualizar_puntuacion'),
    path('valoraciones/eliminar/<int:valoracion_id>/',views.valoracion_eliminar,name='valoraciones_eliminar'),
    
    
]