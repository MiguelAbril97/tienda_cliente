from django.urls import path,re_path
from .import views

    
urlpatterns = [

    path('',views.productos_listar_api),
    
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