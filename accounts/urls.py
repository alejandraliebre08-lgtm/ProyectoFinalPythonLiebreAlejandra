from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views
from .views import CambiarContrasenia


app_name = "accounts"
urlpatterns = [
    path("login/", views.login_request, name="login"),
    path("register/", views.register, name="register"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("profile/", views.profile, name="profile"),
    path("profile/edit/", views.profile_edit, name="profile_edit"),
    path("password/change/",CambiarContrasenia.as_view(),name="password_change"),
    path("about/", views.about, name="about"),
    path("pages/", views.pages_list, name="pages_list"),
    path("pages/<int:id>/", views.page_detail, name="pages_detail"),
]




