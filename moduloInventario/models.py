from django.db import models

# Create your models here.

class Proveedor(models.Model):
    nombre = models.CharField(max_length=200,null=False)
    razon_social = models.CharField(max_length=200,null=False,unique=True)
    ruc = models.CharField(max_length=20,null=False)
    telefono = models.CharField(max_length=10,null=True)
    
    def __unicode__(self):
        return '%s'%(self.razon_social)

    def __str__(self):
        return '%s'% (self.razon_social)

    class Meta:
        db_table = 'Proveedor'
        ordering = ['razon_social']
    
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
    cantidad = models.IntegerField(null=True)
    valor_venta = models.FloatField(null=False)
    categoria = models.ForeignKey(Categoria)
    
    def __str__(self):
        return '%s %s'% (self.codigo, self.nombre)
    
    class Meta:
        db_table = 'Item'
        ordering = ['codigo']
    
class Orden_Compra(models.Model):
    proveedor = models.ForeignKey(Proveedor)
    factura = models.IntegerField(null=False)
    fecha = models.DateField(null=False)
    valor_total = models.FloatField(null=False)
    
    def __str__(self):
        return '%d'% (self.id)
    
    class Meta:
        db_table = 'Compras'
        ordering = ['fecha']
    
class Detalle_Orden_Compra(models.Model):
    item = models.ForeignKey(Item)
    orden = models.ForeignKey(Orden_Compra)
    cantidad = models.IntegerField(null=False)
    valor_unitario = models.FloatField(null=False)
        
    def __str__(self):
        return '%d - %s'%(self.orden.id,self.item)
    
    class Meta:
        db_table = 'Detalles_Compras'
        ordering = ['orden']
    