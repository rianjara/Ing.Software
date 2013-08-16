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
        return '%s'% (self.razon_social)

    class Meta:
        db_table = 'OS_INVENTARIO_PROVEEDORES'
        ordering = ['razon_social']
    
class Categoria(models.Model):
    nombre = models.CharField(max_length=100,null=False,unique=True)
    descripcion = models.CharField(max_length=2000,null=True)
    
    def __unicode__(self):
        return '%s'%(self.nombre)
    
    def __str__(self):
        return 'CATEGORIA\nNombre: %s\nDescripcion: %s'% (self.nombre,self.descripcion)
    
    class Meta:
        db_table = 'OS_INVENTARIO_CATEGORIAS'
        ordering = ['nombre']

class Item(models.Model):
    codigo = models.CharField(unique=True,max_length=30)
    nombre = models.CharField(max_length=100,null=False)
    descripcion = models.CharField(max_length=2000,null=True)
    categoria = models.ForeignKey(Categoria)
    cantidad_disponible = models.IntegerField(null=False)
    
    def __str__(self):
        return '%s'% (self.nombre)
    
    class Meta:
        db_table = 'OS_INVENTARIO_ITEMS'
        ordering = ['codigo']
        
class Item_Costo_Venta(models.Model):
    item = models.ForeignKey(Item)
    valor = models.FloatField(null=False)
    fecha_desde = models.DateTimeField(null=False)
    fecha_hasta = models.DateTimeField(null=True)
    promocional = models.BooleanField(null=False,default=False)
    
    class Meta:
        db_table = 'OS_INVENTARIO_VALOR_VENTAS'
        ordering = ['item']
    
class Item_Adq_Proveedor(models.Model):
    item = models.ForeignKey(Item)
    proveedor = models.ForeignKey(Proveedor)
    cantidad_compra = models.IntegerField(null=False)
    valor_compra = models.FloatField(null=False)
    fecha_compra = models.DateField(null=False)
    
    class Meta:
        db_table = 'OS_INVENTARIO_PROVEEDORES_ITEMS'
        ordering = ['item']

class Item_Adq_Pendiente(models.Model):
    item = models.ForeignKey(Item,unique=True)
    cantidad = models.IntegerField(null=False,default=0)
    
    class Meta:
        db_table = 'OS_INVENTARIO_PENDIENTES'
        ordering = ['item']
    