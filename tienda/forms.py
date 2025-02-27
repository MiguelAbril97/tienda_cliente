from django import forms
from django.contrib.auth.models import AbstractUser
from .helper import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class BusquedaProductoSimple(forms.Form):
    textoBusqueda = forms.CharField(required=True)

class BuscarProducto(forms.Form): 

    buscarNombre = forms.CharField(required=False, label="Nombre")
    buscarDescripcion = forms.CharField(required=False,label="Descripción")
    buscarPrecioMax = forms.DecimalField(
        required=False,
        label="Precio Máximo",
        min_value=0,
        widget=forms.NumberInput(attrs={'min': '0'})
    )
    ESTADOS=[
        ("CN", "Como nuevo"),
        ("U", "Usado"),
        ("MU", "Muy usado"),
    ]
    buscarEstado = forms.MultipleChoiceField(
        choices=ESTADOS,
        required=False,
        widget=forms.CheckboxSelectMultiple(),
        label="Estado"
    )
    buscarCategorias = forms.CharField(
        label= 'Categorías',
        required=False,
    )
    buscarVendedor =forms.CharField(
        label="Vendedor",
        required=False,
    ) 
 
class ProductoForm(forms.Form):
    ESTADOS=[
        ("CN", "Como nuevo"),
        ("U", "Usado"),
        ("MU", "Muy usado"),
    ]
    nombre = forms.CharField(
        required=True, 
        label="Nombre",
        max_length=100  
    )
    descripcion = forms.CharField(
        required=True,
        label="Descripción",
        widget=forms.Textarea  
    )
    precio = forms.DecimalField(  
        required=True,
        label="Precio",
        max_digits=10,
        decimal_places=2,
        min_value=0,
        widget=forms.NumberInput(attrs={'min': '0'})
    )
    estado = forms.ChoiceField(  
        choices=ESTADOS,
        required=True,
        label="Estado"
    )

    def __init__(self, *args, **kwargs):
        super(ProductoForm, self).__init__(*args, **kwargs)
        
        vendedoresDisponibles = helper.obtener_vendedores()
        self.fields['vendedor'] = forms.ChoiceField(
            choices=vendedoresDisponibles,
            required=True,
            widget=forms.Select(),
            label="Vendedor"
        )

        categoriasDisponibles = helper.obtener_categorias()
        self.fields['categorias'] = forms.MultipleChoiceField(
            choices=categoriasDisponibles,
            required=True,
            widget=forms.CheckboxSelectMultiple(),
            label="Categorías"
        )
    
class ProductoActualizarNombreForm(forms.Form):
    nombre = forms.CharField(
        required=True, 
        label="Nombre",
        max_length=100  
    )
    
    
class CompraForm(forms.Form):
    GARANTIA = [
        ("UNO", "Un año"),
        ("DOS", "Dos años"),
    ]
    
    total = forms.DecimalField(max_digits=10,
                               decimal_places=2,
                               required=True,
                               label="Total")
    garantia = forms.ChoiceField(choices=GARANTIA,
                                 required=True,
                                 label="Garantía")

    def __init__(self, *args, **kwargs):
        super(CompraForm, self).__init__(*args, **kwargs)
        compradores_disponibles = helper.obtener_compradores()
        productos_disponibles = helper.obtener_productos()
        
        self.fields['comprador'] = forms.ChoiceField(
            choices=compradores_disponibles,
            required=True,
            widget=forms.Select(),
            label="Comprador"
        )
        
        self.fields['producto'] = forms.MultipleChoiceField(
            choices=productos_disponibles,
            required=True,
            label="Productos",
            help_text="Mantén pulsada la tecla control para seleccionar varios elementos"
        )

class CompraActualizarGarantiaForm(forms.Form):
    GARANTIA = [
        ("UNO", "Un año"),
        ("DOS", "Dos años"),
    ]
    garantia = forms.ChoiceField(choices=GARANTIA, required=True, label="Garantía")
        

class ValoracionForm(forms.Form):
    puntuacion = forms.IntegerField(min_value=1, 
                                    max_value=5, 
                                    required=True, 
                                    label="Puntuación")
    comentario = forms.CharField(widget=forms.Textarea, 
                                 required=False, 
                                 label="Comentario")

    def __init__(self, *args, **kwargs):
        super(ValoracionForm, self).__init__(*args, **kwargs)
        usuarios_disponibles = helper.obtener_compradores()
        compras_disponibles = helper.obtener_compras()
        
        self.fields['usuario'] = forms.ChoiceField(
            choices=usuarios_disponibles,
            required=True,
            widget=forms.Select(),
            label="Usuario"
        )
        
        self.fields['compra'] = forms.ChoiceField(
            choices=compras_disponibles,
            required=True,
            widget=forms.Select(),
            label="Compra"
        )

class ValoracionActualizarPuntuacionForm(forms.Form):
    puntuacion = forms.IntegerField(min_value=1, 
                                    max_value=5, 
                                    required=True, 
                                    label="Puntuación")
    

##################################################
##################################################
########   USUARIO  #########################

class RegistroForm(UserCreationForm):
    roles = (
        (2,'compradores'),
        (3,'vendedores')
    )
    rol = forms.ChoiceField(choices=roles)
    telefono = forms.CharField(max_length=9, label="Teléfono")
    direccion = forms.CharField(max_length=150, label="Dirección")
    nombre = forms.CharField(max_length=60, required=False, label="Nombre")
    apellidos = forms.CharField(max_length=60, required=False, label="Apellidos")
    razonSocial = forms.CharField(max_length=150, required=False, label="Razón Social")
    direccionFiscal = forms.CharField(max_length=150, required=False, label="Dirección Fiscal. Dejelo en blanco si es igual a su dirección")
    class Meta:
        model = User
        fields = ('rol', 'username', 'email', 'telefono', 'direccion', 
                  'password1', 'password2',
                  'nombre', 'apellidos', 
                  'razonSocial', 'direccionFiscal')
        widgets = {
            'email': forms.EmailInput(),
        }
        
class LoginForm(forms.Form):
    usuario = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())
    