from django import forms



class ClienteFormulario(forms.Form):
    nombre = forms.CharField(max_length=40)
    apellido = forms.CharField(max_length=40)
    email = forms.EmailField()
    telefono = forms.CharField(max_length=20)

class BuscarClienteFormulario(forms.Form):
    apellido = forms.CharField(max_length=40)
    email = forms.EmailField(required=False)
