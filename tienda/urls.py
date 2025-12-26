from django.urls import path
from . import views
from .views import ProductoListView, ProductoDetailView, ProductoCreateView, ProductoUpdateView, ProductoDeleteView

app_name = "tienda"

urlpatterns = [
    path("", views.inicio, name="inicio"),
    path("cliente/", views.cliente, name="cliente"),
    path("producto/", views.producto, name="producto"),
    path("carrito/", views.carrito, name="carrito"),
    path("carrito/agregar/<int:producto_id>/", views.agregar_al_carrito, name="agregar_carrito"),
    path("pedido/", views.pedido, name="pedido"),
    path("pedido/crear/", views.crear_pedido, name="crear_pedido"),  
    path("pedido/eliminar/<int:pk>/", views.pedido_eliminar, name="pedido_eliminar"),
    path("pedido/seguimiento/<int:pedido_id>/", views.seguimiento_pedido, name="seguimiento_pedido"),
    path("pages/", views.pages_list, name="pages_list"),
    path("pages/<int:id>/", views.page_detail, name="pages_detail"),
    path("clienteFormulario/", views.clienteFormulario, name="clienteFormulario"),
    path("buscarClienteFormulario/", views.buscarClienteFormulario, name="buscarClienteFormulario"),       

    # Vistas basadas en clases
    path("productos/", ProductoListView.as_view(), name="producto_list"),
    path("productos/<int:pk>/", ProductoDetailView.as_view(), name="producto_detail"),
    path("productos/crear/", ProductoCreateView.as_view(), name="producto_create"),
    path("productos/editar/<int:pk>/", ProductoUpdateView.as_view(), name="producto_edit"),
    path("productos/eliminar/<int:pk>/", ProductoDeleteView.as_view(), name="producto_delete"),
 ]
