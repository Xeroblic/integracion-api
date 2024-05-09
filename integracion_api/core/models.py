from django.db import models
from django.conf import settings
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.hashers import make_password

class UsuarioPersonalizado(AbstractUser):
    telefono = models.IntegerField(blank=True, null=True)
    def save(self, *args, **kwargs):
        if self.pk is None:
            self.set_password(self.password)
        elif self.password != UsuarioPersonalizado.objects.get(pk=self.pk).password:
            self.set_password(self.password)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.username

class Ejemplo(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    edad = models.IntegerField()
    def __str__(self):
        return self.nombre
    
