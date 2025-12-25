from django.urls import path
from . import views
from .views import ProductoListView, ProductoDetailView, ProductoCreateView, ProductoUpdateView, ProductoDeleteView

urlpatterns = [
    path("", views.inicio, name="Inicio"),
    path("cliente/", views.cliente, name="Cliente"),
    path("producto/", views.producto, name="Producto"),
    path("carrito/", views.carrito, name="Carrito"),
    path("carrito/agregar/<int:producto_id>/", views.agregar_al_carrito, name="agregar_carrito"),
    path("pedido/", views.pedido, name="Pedido"),
    path("pedido/crear/", views.crear_pedido, name="crear_pedido"),    
    path("pedido/seguimiento/<int:pedido_id>/", views.seguimiento_pedido, name="seguimiento_pedido"),
    path("clienteFormulario/", views.clienteFormulario, name="clienteFormulario"),
    path("buscarClienteFormulario/", views.buscarClienteFormulario, name="buscarClienteFormulario"),       

    # Vistas basadas en clases
    path("productos/", ProductoListView.as_view(), name="producto_list"),
    path("productos/<int:pk>/", ProductoDetailView.as_view(), name="producto_detail"),
    path("productos/crear/", ProductoCreateView.as_view(), name="producto_create"),
    path("productos/editar/<int:pk>/", ProductoUpdateView.as_view(), name="producto_edit"),
    path("productos/eliminar/<int:pk>/", ProductoDeleteView.as_view(), name="producto_delete"),
 ]
