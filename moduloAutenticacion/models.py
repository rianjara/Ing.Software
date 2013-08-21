from django.db import models
from django.contrib.auth.models import User

class Usuario(models.Model):
    user = models.CharField(primary_key=True, max_length=20)
    nombre = models.CharField(max_length=20)
    apellido = models.CharField(max_length=20)