from django.db import models

# Create your models here.

class Proveedor(models.Model):
    nombre = models.CharField(max_length=200,null=False)
    razon_social = models.CharField(max_length=200,null=False,unique=True)
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
    nombre = models.CharField(max_length=100,null=False,unique=True)
    descripcion = models.CharField(max_length=2000,null=True)
    
    def __unicode__(self):
        return '%s'%(self.nombre)
    
    def __str__(self):
        return 'CATEGORIA\nNombre: %s\nDescripcion: %s'% (self.nombre,self.descripcion)
    
    class Meta:
        db_table = 'Categoria'
        ordering = ['nombre']

class Item(models.Model):
    codigo = models.CharField(unique=True,max_length=30)
    nombre = models.CharField(max_length=100,null=False)
    descripcion = models.CharField(max_length=2000,null=True)
    costo_unitario = models.FloatField(null=False)
    cantidad = models.IntegerField(default=0,null=False)
    circulando = models.BooleanField(null=False)
    proveedor = models.ForeignKey(Proveedor)
    categoria = models.ForeignKey(Categoria)
    
    def __str__(self):
        return '%s'% (self.nombre)
    
    def isActive(self):
        return self.circulando
    
    def inactivate(self):
        self.circulando=False
    
    def activate(self):
        self.circulando=True
    
    class Meta:
        db_table = 'Item'
        ordering = ['codigo']
