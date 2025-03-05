Clonamos los dos repositorios en la carpeta que vayamos a utilizar

![Clonar repositorios](imagenes_tutorial/clonar_repositorios.png)

Para utilizar la aplicación es necesario tener python3.
Empezaremos configurando el servidor API (tiendaSegundaMano) desde VSCode. Abrimos la terminal integrada de VisualStudio y ejecutamos los siguientes comandos en orden:
python3 -m venv myvenv
source myvenv/bin/activate 
python -m pip install --upgrade pip
pip install -r requirements.txt

![Comandos iniciales](imagenes_tutorial/comandos.png)

Con esto habremos creado el entorno virtual e instalado los paquetes listados en requirements.txt
Ahora creamos el archivo llamado .env. Copiamos el contenido de .env.plantilla, lo pegamos en nuestro .env y ponemos la configuracion necesaria para tener la aplicacion en desarrollo
Podemos generar nuestro secret key introduciendo el siguiente comando en la terminal:
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"

![Configuración del entorno](imagenes_tutorial/env.png)

Creamos la base de datos con: python manage.py migrate.
Creamos un superusuario con: python3 manage.py createsuperuser
Iniciamos el servidor con python3 manage.py runserver. El servidor se inicia en el puerto 8000
Vamos al navegador web y nos dirigimos a http://127.0.0.1:8000/oauth2/applications/

Te redireccionara a una pantalla de login, introduce el superusuario que hayas creado. 
Esto te llevara al index, vueve a introducir el enlace de antes y entonces te mostrará la ventana de inicio para la configuracion del oauth (segunda imagen)

![Login OAuth2](imagenes_tutorial/login_oauth2.png)
![OAuth Inicio](imagenes_tutorial/oauth1.png)

Ahora introduce el nombre de la aplicacion, una identificacion y la contraseña. 
Es importante que los campos Client type y Authorization grant type esten como en la imagen

![Configuración OAuth](imagenes_tutorial/oauth_configuracion.png)

Ahora vamos al panel de administracion y creamos las categorias que vatas a utilizar en tu aplicacion: http://127.0.0.1:8000/admin

![Categorías](imagenes_tutorial/categoria.png)

Volvemos a VScode y detenemos el servidor (Ctrl+C en terminal) e importamoslos los grupos y permisos de los grupos almacenados en fixtures/datos.json

![Grupos](imagenes_tutorial/grupos.png)

Con esto ya tenemos el servidor API configurado. Ahora vamos al cliente, lo primero que debemos hacer es configurar el entorno virtual exactamente igual que en el servidor, tambien configuarmos el .env usando la plantilla de cliente. Los datos de clientid y secret que haya introdicido en el registro de Oauth deben introducirse en el .env:

![Comandos Cliente](imagenes_tutorial/comandos_cliente.png)
![Configuración ENV Cliente](imagenes_tutorial/env_cliente.png)

Creamos la base de datos con python3 manage.py migrate
Iniciamos nuestro servidor API, y nuestro servidor cliente debemos iniciarlo en otro puerto: python3 manage.py runserver -puerto-. Hay que tener en cuenta que las peticiones de la aplicacion estan hechas a un servidor en el puerto 8000. Si cambia el puerto en el que se ejecuta la API deben cambiarse las peticiones

Una vez levante los servidores, si va al navegador podra ver el inicio

![Página de inicio](imagenes_tutorial/index.png)

Vamos a crearnos un usuario vendedor para probar las peticiones POST. Haciendo click en Registrar vera el formulario

![Registro](imagenes_tutorial/registro.png)

Si hemos rellenado los datos correctamente nos reenviara a la pagina de inicio. Ahora veremos nuestro nombre de usuario y un boton de Logout. Si hacemos click en logout cerraremos la sesion y podremos volver a iniciarla con el de Login

![Login Cliente](imagenes_tutorial/login_cliente.png)

Si entramos en crear producto veremos el formulario de creacion. 
Si rellenamos todos los campos correctamente podremos crear un producto y nos redirigira a
la lista de todos los productos que haya creado ese vendedor

![Crear Producto](imagenes_tutorial/producto_crear.png)
![Lista de Productos](imagenes_tutorial/lista_productos.png)

Si hacemos click en el icono del lapiz bajo el nombre podremos 
editar el nombre de ese producto

![Actualizar Producto](imagenes_tutorial/producto_actualizar.png)
![Nombre Actualizado](imagenes_tutorial/nombre_actualizado.png)

En el lapiz de abajo nos llevara a un formulario que nos permite editar 
todos los datos

![Editar Producto](imagenes_tutorial/producto_editar.png)
![Producto Editado](imagenes_tutorial/producto_editado.png)

Haciendo click en la papelera podra eliminar ese producto

![Confirmar Eliminación](imagenes_tutorial/confirmar_eliminacion.png)
![Producto Eliminado](imagenes_tutorial/eliminado.png)

Para hacer una busqueda de un producto tendremos el siguiente formulario. 
Al rellenarlo con los datos que queremos nos mostrará todos los productos que cumplan
las condiciones. Si el usuario es un vendedor se limitara la busqueda solo a los productos
publicados por ese vendedor.

![Formulario de Búsqueda](imagenes_tutorial/formulario_buscar.png)

Al buscar por los parametros que se indican en la anterior captura nos mostraria el siguiente
resultado

![Resultado de Búsqueda](imagenes_tutorial/busqueda.png)


