from django.db import models
from django.contrib.auth.models import User
from django.conf import settings




class Avatar(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True
    )
    image = models.ImageField(
        upload_to="avatars",
        null=True,
        blank=True
    )

    def __str__(self):
        return f"{settings.MEDIA_URL}{self.image}"


class Page(models.Model):
    titulo = models.CharField(max_length=200)
    subtitulo = models.CharField(max_length=200, blank=True, null=True)
    contenido = models.TextField()
    autor = models.ForeignKey(User, on_delete=models.CASCADE, related_name="pages")
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.titulo
