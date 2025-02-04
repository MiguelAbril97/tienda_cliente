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

    def clean(self):
 
        #Validamos con el modelo actual
        super().clean()
        nombre = self.cleaned_data.get('buscarNombre')
        descripcion = self.cleaned_data.get('buscarDescripcion')
        precio = self.cleaned_data.get('buscarPrecioMax')
        estado = self.cleaned_data.get('buscarEstado')

        if ('buscarVendedor' in self.cleaned_data):
            vendedor = self.cleaned_data.get('buscarVendedor')

        fecha = self.cleaned_data.get('buscarFecha')
        categoria = self.cleaned_data.get('buscarCategorias')
        
        #Compruebo que no deja todo vacio y la longitud de los campos precio y nombre
        if(nombre == "" 
           and descripcion==""
           and precio is None
           and len(estado) == 0 
           and fecha is None 
           and categoria==""
           ):
            if(vendedor and vendedor==""):
                error_msg = "Debe introducir al menos un valor en un campo del formulario"
                self.add_error('buscarVendedor', error_msg)
                self.add_error('buscarNombre', error_msg)
                self.add_error('buscarDescripcion', error_msg)
                self.add_error('buscarPrecioMax', error_msg)
                self.add_error('buscarEstado', error_msg)
                self.add_error('buscarVendedor', error_msg)
                self.add_error('buscarFecha', error_msg)
                self.add_error('buscarCategorias', error_msg)
            else:
                error_msg = "Debe introducir al menos un valor en un campo del formulario"
                self.add_error('buscarNombre', error_msg)
                self.add_error('buscarDescripcion', error_msg)
                self.add_error('buscarPrecioMax', error_msg)
                self.add_error('buscarEstado', error_msg)
                self.add_error('buscarVendedor', error_msg)
                self.add_error('buscarFecha', error_msg)
                self.add_error('buscarCategorias', error_msg)
        else:
            
            if(precio is not None and precio > 9999999999):
                self.add_error('buscarPrecioMax', 'Introduzca un precio maximo más bajo')
            if(nombre != "" and len(nombre) > 100):
                self.add_error('buscarNombre', 'Introduzca un nombre más corto')

class BuscarCalzado(forms.Form):
    MARCAS = [
        ("NIKE", "Nike"),
        ("ADID", "Adidas"),
        ("PUMA", "Puma"),
        ("RBK", "Reebok"),
        ("NB", "New Balance"),
        ("CLRK", "Clarks"),
        ("GUCCI", "Gucci"),
    ]

    buscarTalla = forms.IntegerField(min_value=1, max_value=50, required=False, label="Talla")
    buscarMarca = forms.ChoiceField(choices=MARCAS, required=False, label="Marca")
    buscarColor = forms.CharField(max_length=20, required=False, label="Color")
    buscarMaterial = forms.CharField(max_length=30, required=False, label="Material")
    buscarPrecioMax = forms.DecimalField(
        required=False,
        label="Precio Máximo",
        min_value=0,
        widget=forms.NumberInput()
    )
    def clean(self):
        super().clean()

        talla = self.cleaned_data.get('buscarTalla')
        marca = self.cleaned_data.get('buscarMarca')
        color = self.cleaned_data.get('buscarColor')
        material = self.cleaned_data.get('buscarMaterial')
        precio = self.cleaned_data.get('buscarPrecioMax')

        if not talla and not marca and not color and not material and not precio:
            error_msg = "Debe introducir al menos un valor en un campo del formulario"
            self.add_error('buscarTalla', error_msg)
            self.add_error('buscarMarca', error_msg)
            self.add_error('buscarColor', error_msg)
            self.add_error('buscarMaterial', error_msg)
            self.add_error('buscarPrecioMax', error_msg)

        if material and len(material) < 3:
            self.add_error('buscarMaterial', 'Material debe contener al menos 3 caracteres')
        if talla and (talla < 1 or talla > 50):
            self.add_error('buscarTalla', 'La talla debe ser entre 1 y 50')
        if precio and precio > 999:
            self.add_error('buscarPrecioMax', 'El precio máximo es 999')

        return self.cleaned_data
    
class BuscarMueble(forms.Form):
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
    
    def clean(self):
       
        super().clean()

        material = self.cleaned_data.get('buscarMaterial')
        ancho_min = self.cleaned_data.get('buscarAnchoMin')
        ancho_max = self.cleaned_data.get('buscarAnchoMax')
        alto_min = self.cleaned_data.get('buscarAltoMin')
        alto_max = self.cleaned_data.get('buscarAltoMax')
        profundidad_min = self.cleaned_data.get('buscarProfundidadMin')
        profundidad_max = self.cleaned_data.get('buscarProfundidadMax')
        peso_max = self.cleaned_data.get('buscarPesoMax')

        if(material == "" 
             and ancho_min is None and ancho_max is None 
             and alto_min is None and alto_max is None
             and profundidad_min is None and profundidad_max is None
             and peso_max is None
             ):

             error_msg = "Debe introducir al menos un valor en un campo del formulario"


             self.add_error('buscarMaterial', error_msg)
             self.add_error('buscarAnchoMin', error_msg)
             self.add_error('buscarAnchoMax', error_msg)
             self.add_error('buscarAltoMin', error_msg)
             self.add_error('buscarAltoMax', error_msg)
             self.add_error('buscarProfundidadMin', error_msg)
             self.add_error('buscarProfundidadMax', error_msg)
             self.add_error('buscarPesoMax', error_msg)

        #Me aseguro de que ninguno de los màximos sean menores que los mínimos
        if(not ancho_min is None and not ancho_max is None and ancho_min > ancho_max):
            self.add_error('buscarAnchoMin','El ancho mínimo no puede ser mayor al maximo')
            self.add_error('buscarAnchoMax','El ancho mínimo no puede ser mayor al maximo')
        
        if(not alto_min is None and not alto_max is None and  alto_min > alto_max):
            self.add_error('buscarAltoMin', 'El alto mínimo no puede ser mayor al máximo')
            self.add_error('buscarAltoMax', 'El alto mínimo no puede ser mayor al máximo')

        if(not profundidad_max is None and not profundidad_min is None and  profundidad_min > profundidad_max):
            self.add_error('buscarProfundidadMin', 'La profundidad mínima no puede ser mayor a la máxima')
            self.add_error('buscarProfundidadMax', 'La profundidad mínima no puede ser mayor a la máxima')
        
        #tambien de que el peso maximo no sea menor o igual a 0
        if(not peso_max is None and peso_max <= 0):
            self.add_error('buscarPesoMax', 'El peso debe ser mayor a 0')

        
        return self.cleaned_data


class BuscarConsola(forms.Form):
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

    def clean(self):
        super().clean()

        modelo = self.cleaned_data.get('buscarModelo')
        color = self.cleaned_data.get('buscarColor')
        memoria = self.cleaned_data.get('buscarMemoria')
        precio = self.cleaned_data.get('buscarPrecioMax')

        if (modelo == "" 
            and color == "" 
            and memoria is None  
            and precio is None):
            error_msg = "Debe introducir al menos un valor en un campo del formulario"
            self.add_error('buscarModelo', error_msg)
            self.add_error('buscarColor', error_msg)
            self.add_error('buscarMemoria', error_msg)
            self.add_error('buscarPrecioMax', error_msg)

        #Compruebo la longitud del color y vulvo a usar la validacion de antes
        if (not color !="" and len(color) < 4):
            self.add_error('buscarColor', 'Color invalido')
        elif(color and not color.isalpha()):
            self.add_error('color', 'El color debe contener solo letras.')
        if (memoria != "" and not memoria.isdigit()):
            raise forms.ValidationError("El campo memoria debe contener solo números.")

        return self.cleaned_data