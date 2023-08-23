from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Registro(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=80)
    contenido = models.TextField()
    imagen = models.ImageField(upload_to='registro/', null=True, blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['usuario', 'fecha_creacion']

    def __str__(self):
        return self.titulo