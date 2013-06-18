from django.db import models

class Cliente(models.Model):
    cedula = models.CharField(max_length=10)
    nombre = models.CharField(max_length=30)
    apellido1 = models.CharField(max_length=30)
    apellido2 = models.CharField(max_length=30)
    fecha_nacimiento = models.DateField()
    #maximo cuatro telefonos separados por coma
    telefonos = models.CharField(max_length=43)
    direccion = models.CharField(max_length=100)
    e_mail1 = models.EmailField()
    e_mail2 = models.EmailField()
    ruc = models.CharField(max_length=15)
    
    def __str__(self):
        return '%s %s %s' %(self.nombre,self.apellido1,self.apellido2)
    
    class Admin:
        pass