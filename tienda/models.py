# tienda/models.py
from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField


class Cliente(models.Model):
    nombre = models.CharField(max_length=40)
    apellido = models.CharField(max_length=40)
    email = models.EmailField()  
    telefono = models.CharField(max_length=20, blank=True, null=True)
    direccion = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"

class Producto(models.Model):
    nombre = models.CharField(max_length=50)
    descripcion = models.TextField(blank=True, null=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre


class Carrito(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    creado = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Carrito de {self.user.username}"


class CarritoItem(models.Model):
    carrito = models.ForeignKey(
        Carrito, on_delete=models.CASCADE, related_name="items"
    )
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)

    def subtotal(self):
        return self.producto.precio * self.cantidad

    def __str__(self):
        return f"{self.producto.nombre} x{self.cantidad}"



class Pedido(models.Model):
    ESTADOS = (
        ("pendiente", "Pendiente"),
        ("confirmado", "Confirmado"),
        ("enviado", "Enviado"),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=20, choices=ESTADOS, default="pendiente")
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"Pedido #{self.id} - {self.user.username}"




class Page(models.Model):
    titulo = models.CharField(max_length=200)                 # CharField 1
    subtitulo = models.CharField(max_length=200, blank=True, null=True) # CharField 2

    contenido = RichTextField()                               # TEXTO ENRIQUECIDO ✔️
    imagen = models.ImageField(upload_to="pages", blank=True, null=True)  # IMAGEN ✔️

    autor = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="pages"
    )

    fecha_creacion = models.DateTimeField(auto_now_add=True)  # FECHA ✔️

    def __str__(self):
        return self.titulo
