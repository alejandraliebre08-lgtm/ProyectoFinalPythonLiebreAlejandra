from django.contrib import admin
from .models import Cliente, Producto, Pedido, Carrito, Page

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ("nombre", "apellido", "email", "telefono", "direccion")
    search_fields = ("nombre", "apellido", "email")


    def save_model(self, request, obj, form, change):
      
        if not getattr(obj, "user_id", None):
            obj.user = request.user
        super().save_model(request, obj, form, change)

admin.site.register(Producto)
admin.site.register(Pedido)
admin.site.register(Carrito)
admin.site.register(Page)
