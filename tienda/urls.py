from django.urls import path,re_path
from .import views

    
urlpatterns = [
    path('',views.index),
    path('productos/',views.productos_listar_api,name='lista_basica'),
    path('productos-mejorado/',views.productos_listar_mejorado_api,name='lista_mejorada'),
    path('productos/buscar_simple/',views.producto_buscar_simple,name='productos_buscar_simple'),
    path('productos/buscar_avanzada/',views.producto_buscar,name='productos_buscar'),
    path('productos/crear/',views.producto_crear,name='productos_crear'),
    path('calzados/',views.calzado_listar,name='calzados'),
    path('calzados_crear/',views.calzado_crear,name='calzados_crear'),
    path('calzados/buscar/',views.calzado_buscar,name='calzados_buscar'),
    path('consolas/',views.consolas_listar,name='consolas'),
    path('consolas/buscar/',views.consola_buscar,name='consolas_buscar'),
    path('consolas_crear/',views.consola_crear,name='consolas_crear'),
    path('muebles/',views.muebles_listar,name='muebles'),
    path('muebles/buscar/',views.mueble_buscar,name='muebles_buscar'),
    path('muebles_crear/',views.mueble_crear,name='muebles_crear'),
    
    #CRUD calzado
    # path('calzado/crear', views.calzado_crear, name='calzado_crear'),
    # path('calzado/buscar', views.calzado_buscar, name='calzado_buscar'),
    # path('calzado/actualizar/<int:calzado_id>/', views.calzado_editar, name='calzado_editar'),
    # path('calzado/eliminar/<int:calzado_id>/', views.calzado_eliminar, name='calzado_eliminar'),
    
    
    #CRUD mueble
    #CRUD mueble
    # path('mueble/crear', views.mueble_crear, name='mueble_crear'),
    # path('mueble/buscar', views.mueble_buscar, name='mueble_buscar'),
    # path('mueble/actualizar/<int:mueble_id>/', views.mueble_editar, name='mueble_editar'),
    # path('mueble/eliminar/<int:mueble_id>/', views.mueble_eliminar, name='mueble_eliminar'),
        
        #CRUD consola
    #CRUD consola
    # path('consola/crear', views.consola_crear,name='consola_crear'),
    # path('consola/buscar', views.consola_buscar,name='consola_buscar'),
    # path('consola/actualizar/<int:consola_id>/', views.consola_editar, name='consola_editar'),
    # path('consola/eliminar/<int:consola_id>/', views.consola_eliminar, name='consola_eliminar'),

]