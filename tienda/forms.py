from django import forms
from django.utils import timezone
from django.contrib.auth.models import AbstractUser

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
