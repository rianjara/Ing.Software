from django.db import models

# Create your models here.

class Proveedor(models.Model):
    nombre = models.CharField(max_length=200,null=False)
    razon_social = models.CharField(max_length=200,null=False,primary_key=True)
    ruc = models.CharField(max_length=20,null=False)
    telefono = models.CharField(max_length=20,null=True)
    
    def __unicode__(self):
        return '%s'%(self.razon_social)

    def __str__(self):
        return '%s'% (self.nombre)

    class Meta:
        db_table = 'Proveedor'
        ordering = ['nombre']
    
class Categoria(models.Model):
    nombre = models.CharField(max_length=100,null=False,primary_key=True)
    descripcion = models.CharField(max_length=2000,null=True)
    
    def __unicode__(self):
        return '%s'%(self.nombre)
    
    def __str__(self):
        return 'CATEGORIA\nNombre: %s\nDescripcion: %s'% (self.nombre,self.descripcion)
    
    class Meta:
        db_table = 'Categoria'
        ordering = ['nombre']

class Item(models.Model):
    codigo = models.CharField(primary_key=True,max_length=30)
    nombre = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=2000)
    costo_unitario = models.FloatField()
    cantidad = models.FloatField(default=0)
    circulando = models.BooleanField(null=False)
    
    proveedor = models.ForeignKey(Proveedor)
    categoria = models.ForeignKey(Categoria)
    
    def __str__(self):
        return '%s'% (self.nombre)
    
    class Meta:
        db_table = 'Item'
        ordering = ['codigo']
