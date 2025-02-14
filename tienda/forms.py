from django import forms
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from .helper import *

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
    buscarFecha = forms.DateField(
        label="Fecha de Publicación",
        required=False,
        widget=forms.DateInput(format="%Y-%m-%d", attrs={"type": "date"})
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
    fecha_de_publicacion = forms.DateTimeField(
        label="Fecha de Publicación",
        required=True,
        widget=forms.DateTimeInput(
            format="%Y-%m-%d %H:%M:%S", 
            attrs={"type": "datetime-local"}
        )
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

class BuscarCalzado(forms.Form):
    
    buscarNombre = forms.CharField(required=False, label="Nombre")
    MARCAS = [
        ("''","Cualquiera"),
        ("NIKE", "Nike"),
        ("ADID", "Adidas"),
        ("PUMA", "Puma"),
        ("RBK", "Reebok"),
        ("NB", "New Balance"),
        ("CLRK", "Clarks"),
        ("GUCCI", "Gucci"),
    ]
    buscarTalla = forms.IntegerField(min_value=1, max_value=50, required=False, label="Talla")
    buscarMarca = forms.ChoiceField(
        choices=MARCAS,
        required=False,
        label="Marca",
        widget=forms.RadioSelect(),
        initial="''"
    )
    buscarColor = forms.CharField(max_length=20, required=False, label="Color")
    buscarMaterial = forms.CharField(max_length=30, required=False, label="Material")
    buscarPrecioMax = forms.DecimalField(
        required=False,
        label="Precio Máximo",
        min_value=0,
        widget=forms.NumberInput()
    )

class CalzadoForm(forms.Form):
    MARCAS = [
        ("NIKE", "Nike"),
        ("ADID", "Adidas"),
        ("PUMA", "Puma"),
        ("RBK", "Reebok"),
        ("NB", "New Balance"),
        ("CLRK", "Clarks"),
        ("GUCCI", "Gucci"),
    ]
    
    talla = forms.CharField(max_length=2,
                            required=True, 
                            label="Talla")
    marca = forms.CharField(
        max_length=5,
        choices=MARCAS,
        required=True,
    )
    color = forms.CharField(max_length=20, 
                            label="Color")
    
    material = forms.CharField(max_length=30,
                               required=True, 
                                label="Material"
                                )
    
    def __init__(self, *args, **kwargs):
        super(CalzadoForm, self).__init__(*args, **kwargs)
        
        productosDisponibles = helper.obtener_productos()
        self.fields['vendedor'] = forms.ChoiceField(
            choices=productosDisponibles,
            required=True,
            widget=forms.Select(),
            label="Producto"
        )

       
    
class BuscarMueble(forms.Form):
    buscarNombre = forms.CharField(required=False, label="Nombre")
    buscarMaterial = forms.CharField(required=False, label="Material")
    buscarAnchoMin = forms.FloatField(
        required=False,
        label="Ancho mínimo",
        widget=forms.NumberInput()
    )
    buscarAnchoMax = forms.FloatField(
        required=False,
        label="Ancho máximo",
        widget=forms.NumberInput()
    )
    buscarAltoMin = forms.FloatField(
        required=False,
        label="Alto mínimo",
        widget=forms.NumberInput()
    )
    buscarAltoMax = forms.FloatField(
        required=False,
        label="Alto máximo",
        widget=forms.NumberInput()
    )
    buscarProfundidadMin = forms.FloatField(
        required=False,
        label="Profundidad mínima",
        widget=forms.NumberInput()
    )
    buscarProfundidadMax = forms.FloatField(
        required=False,
        label="Profundidad máxima",
        widget=forms.NumberInput()
    )
    buscarPesoMax = forms.IntegerField(
        required=False,
        label="Peso máximo",
        widget=forms.NumberInput()
    )
    
class MueblesForm(forms.Form):
    material = forms.CharField(max_length=30, required=True, label="Material")
    ancho = forms.FloatField(required=True, label="Ancho")
    alto = forms.FloatField(required=True, label="Alto")
    profundidad = forms.FloatField(required=True, label="Profundidad")
    peso = forms.IntegerField(required=True, label="Peso")

    def __init__(self, *args, **kwargs):
        super(MueblesForm, self).__init__(*args, **kwargs)
        productosDisponibles = helper.obtener_productos()
        self.fields['producto'] = forms.ChoiceField(
            choices=productosDisponibles,
            required=True,
            widget=forms.Select(),
            label="Producto"
        )    



class BuscarConsola(forms.Form):
    buscarNombre = forms.CharField(required=False, label="Nombre")
    buscarModelo = forms.CharField(required=False, label="Modelo")
    buscarColor = forms.CharField(required=False, label="Color")
    buscarMemoria = forms.IntegerField(
        required=False,
        label="Memoria",
        widget=forms.NumberInput()
    )
    buscarPrecioMax = forms.DecimalField(
        required=False,
        label="Precio Máximo",
        min_value=0,
        widget=forms.NumberInput(attrs={'placeholder': '1000.00'})
    )

class ConsolasForm(forms.Form):
    modelo = forms.CharField(max_length=50, required=True, label="Modelo")
    color = forms.CharField(max_length=20, required=True, label="Color")
    memoria = forms.CharField(max_length=20, required=True, label="Memoria")

    def __init__(self, *args, **kwargs):
        super(ConsolasForm, self).__init__(*args, **kwargs)
        productosDisponibles = helper.obtener_productos()
        self.fields['producto'] = forms.ChoiceField(
            choices=productosDisponibles,
            required=True,
            widget=forms.Select(),
            label="Producto"
        )