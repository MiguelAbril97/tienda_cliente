Por cada petición que hemos hecho, se ha incluido siempre lo siguiente:http://127.0.0.1:8000/api/v1/libros/, que pasaría si en un futuro, la versión cambiar.¿Deberíamos cambiarlo en todos los sitios de la aplicación?¿Cómo podríamos mejorarlo?
-Es mejor utilizar un metodo ya que reduce los posibles errores al escribir la direccion y facilita el mantenimiento o actualizacion del codigo si hubiese que cambiar la version en el futuro

Para la respuesta siempre incluimos la misma línea:response.json(). ¿Qué pasaría si en el día de mañana cambia el formato en una nueva versión, y en vez de json es xml?¿Debemos volver a cambiar en todos los sitios esa línea?
-No, por eso he creado el metodo respuesta, que junto con peticion_v1 y crear_cabecera evita errores al escribir y facilita los cambios futuros.

¿Siempre debemos tratar todos los errores en cada una de las peticiones?
No, es mejor crear metodos que manejen los errores y utilizarlos en las peticiones. Tampoco es bueno dar mucha informacion de los errores al cliente porque pueden exponer problemas de seguridad


client_id=aplicacion&client_secret=clave

super usuario: 
    nombre de usuario: usuario
    contraseña: usuario

Cliente: 
    usuario: Jorge_comprador
    contraseña: contraseña12

Vendedor:
    usuario: Vendedor_ejemplo
    contraseña: falsaContra12.

