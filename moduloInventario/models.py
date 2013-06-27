from django.db import models

# Create your models here.

class Item(models.Model):
    codigo = models.CharField(primary_key=True,max_length=30)
    nombre = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=500)
    proveedor = models.CharField(max_length=30,null=True)
    costo_unitario = models.FloatField()
    cantidad = models.FloatField(default=0)
    
    def __str__(self):
        return '%s'% (self.nombre)
    
    class Meta:
        db_table = 'Item'
        ordering = ['codigo']
    
CATEGORIAS_CHOICES = (
        ('MARCOS', 'MARCOS'),
        ('GAFAS', 'GAFAS'),
        ('LENT_CONT', 'LENTES_DE_CONTACTO'),
        ('SOL', 'SOLUCIONES'),
        ('VARIOS', 'VARIOS'),
  )

class Inventario(models.Model):
    nombre_categoria = models.CharField(choices=CATEGORIAS_CHOICES,max_length=18)
    items = models.ForeignKey(Item)
    
    def __str__(self):
        return '%s'% (self.nombre_categoria)
    
    class Meta:
        db_table = 'Inventario'
        order_with_respect_to = 'items'
        ordering = ['id']
        
