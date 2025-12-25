from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import Cliente, Producto, Carrito, Pedido, Page
from .forms import ClienteFormulario, BuscarClienteFormulario
from accounts.models import Avatar



def inicio(request):
    avatar = None
    if request.user.is_authenticated:
        avatar = Avatar.objects.filter(user=request.user).first()

    return render(request, "tienda/inicio.html", {"avatar": avatar})


def cliente(request):
    clientes = Cliente.objects.all()
    return render(request, "tienda/cliente.html", {"clientes": clientes})


def producto(request):
    productos = Producto.objects.filter(activo=True)
    return render(request, "tienda/producto.html", {"productos": productos})


@login_required
def carrito(request):
    carrito, created = Carrito.objects.get_or_create(user=request.user)
    items = carrito.items.all()
    total = sum(item.producto.precio * item.cantidad for item in items)

    return render(
        request,
        "tienda/carrito.html",
        {
            "carrito": carrito,
            "items": items,
            "total": total,
        },
    )

@login_required
def agregar_al_carrito(request, producto_id):
    carrito, _ = Carrito.objects.get_or_create(user=request.user)
    producto = get_object_or_404(Producto, id=producto_id)

    qs = carrito.items.filter(producto=producto)

    if qs.exists():
        item_principal = qs.first()
        total_cant = 0
        for i in qs:
            total_cant += i.cantidad

        item_principal.cantidad = total_cant + 1
        item_principal.save()
        qs.exclude(id=item_principal.id).delete()
    else:
        carrito.items.create(producto=producto, cantidad=1)

    return redirect("tienda:carrito")




@login_required
def pedido(request):
    pedidos = Pedido.objects.filter(user=request.user).order_by("-fecha")
    return render(request, "tienda/pedido.html", {"pedidos": pedidos})


@login_required
def crear_pedido(request):
    # OJO: el modelo es Carrito (mayúscula), no "carrito"
    carrito = get_object_or_404(Carrito, user=request.user)

    if not carrito.items.exists():
        return redirect("tienda:carrito")

    Pedido.objects.create(user=request.user, estado="pendiente")

    carrito.items.all().delete()  # vacía el carrito
    return redirect("tienda:pedido")


@login_required
def seguimiento_pedido(request, pedido_id):
    pedido_obj = get_object_or_404(Pedido, id=pedido_id, user=request.user)
    return render(request, "tienda/seguimiento_pedido.html", {"pedido": pedido_obj})


@login_required
def clienteFormulario(request):
    if request.method == "POST":
        form = ClienteFormulario(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            Cliente.objects.create(
                nombre=data["nombre"],
                apellido=data["apellido"],
                email=data["email"],
                telefono=data["telefono"],
            )
            return redirect("tienda:cliente")
    else:
        form = ClienteFormulario()

    return render(request, "tienda/clienteFormulario.html", {"form": form})


@login_required
def buscarClienteFormulario(request):
    form = BuscarClienteFormulario(request.GET or None)
    clientes = None

    if form.is_valid():
        apellido = form.cleaned_data["apellido"]
        clientes = Cliente.objects.filter(apellido__icontains=apellido)

    return render(
        request,
        "tienda/buscarClienteFormulario.html",
        {"form": form, "resultados": clientes},
    )



def pages_list(request):
    pages = Page.objects.all()
    return render(request, "tienda/pages_list.html", {"pages": pages})


def page_detail(request, id):
    page = get_object_or_404(Page, id=id)
    return render(request, "tienda/page_detail.html", {"page": page})


# --------- CBV Productos ---------

class ProductoListView(ListView):
    model = Producto
    template_name = "tienda/producto.html"


class ProductoDetailView(DetailView):
    model = Producto
    template_name = "tienda/producto_detail.html"
    context_object_name = "producto"


class ProductoCreateView(LoginRequiredMixin, CreateView):
    model = Producto
    template_name = "tienda/producto_create.html"
    fields = ["nombre", "descripcion", "precio", "stock", "activo"]
    success_url = reverse_lazy("tienda:producto_list")


class ProductoUpdateView(LoginRequiredMixin, UpdateView):
    model = Producto
    template_name = "tienda/producto_edit.html"
    fields = ["nombre", "descripcion", "precio", "stock", "activo"]
    success_url = reverse_lazy("tienda:producto_list")


class ProductoDeleteView(LoginRequiredMixin, DeleteView):
    model = Producto
    template_name = "tienda/producto_confirm_delete.html"
    success_url = reverse_lazy("tienda:producto_list")



