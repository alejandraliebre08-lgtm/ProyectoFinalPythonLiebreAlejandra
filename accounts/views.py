from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import UserRegisterForm, UserEditForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy
from .forms import AvatarFormulario
from .models import Avatar


@login_required
def editar_perfil(request):
    if request.method == "POST":
        form = UserEditForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect("profile")
    else:
        form = UserEditForm(instance=request.user)

    return render(request, "accounts/profile_edit.html", {"form": form})


def about(request):
    return render(request, "accounts/about.html")



def login_request(request):
    msg_login = ""

    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():
            usuario = form.cleaned_data.get("username")
            contrasenia = form.cleaned_data.get("password")

            user = authenticate(username=usuario, password=contrasenia)

            if user is not None:
                login(request, user)
                return redirect("tienda:inicio")

            msg_login = "Usuario o contraseña incorrectos"
    else:
        form = AuthenticationForm()

    return render(
        request,
        "accounts/login.html",
        {
            "form": form,
            "msg_login": msg_login
        }
    )



@login_required
def logout_view(request):
    logout(request)
    return redirect("inicio")


def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  
            return redirect("Inicio")  
        else:
            return render(request, "accounts/register.html", {"form": form})
    else:
        form = UserRegisterForm()
        return render(request, "accounts/register.html", {"form": form})
    

@login_required
def profile(request):
    return render(request, "accounts/profile.html")

@login_required
def profile_edit(request):
    # El usuario para poder editar su perfil primero debe estar logueado.
    # Al estar logueado, podemos encontrar dentro del request la instancia
    # del usuario -> request.user
    usuario = request.user

    if request.method == "POST":
        miFormulario = UserEditForm(request.POST, instance=request.user)

        if miFormulario.is_valid():
            miFormulario.save()

            # Retornamos al inicio una vez guardados los datos
            return render(request, "tienda/inicio.html")

    else:
        miFormulario = UserEditForm(instance=request.user)

    return render(
        request,
        "accounts/profile_edit.html", {"mi_form": miFormulario, "usuario": usuario}
        )    

@login_required
def agregar_avatar(request):
    if request.method == "POST":
        form = AvatarFormulario(request.POST, request.FILES)
        if form.is_valid():
            Avatar.objects.update_or_create(
                user=request.user,
                defaults={"imagen": request.FILES.get("imagen")}
            )
            return redirect("tienda:inicio")
    else:
        form = AvatarFormulario()

    return render(request, "accounts/agregar_avatar.html", {"form": form})



# --------- CBV Usuario ---------

class CambiarContrasenia(LoginRequiredMixin, PasswordChangeView):

    template_name = 'accounts/password_change.html'
    success_url = reverse_lazy('EditarPerfil')

