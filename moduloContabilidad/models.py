from django.db import models
from moduloInventario.models import Orden_Compra,Detalle_Orden_Compra

class Gastos(models.Model):
    concepto = models.CharField(null=True, max_length=30)
    valor_gasto = models.DecimalField(max_digits=5,decimal_places=3)
    fecha_gasto = models.DateField(null=True)
    beneficiario = models.CharField(null=True, max_length=20)
    factura=models.IntegerField(max_length=10)
    
    
    def __str__(self):
        return '%s'% (self.valor_gasto)
    
    class Meta:
        db_table = 'Gastos'
        ordering = ['fecha_gasto']
        
class Cuentas_x_pagar(models.Model):
    Detalle_Orden_Compra = models.ForeignKey(Detalle_Orden_Compra)
    fecha_vencimiento = models.DateField(null=True)
   
    
    
    def __str__(self):
        return '%s'% (self.valor_gasto)
    
    class Meta:
        db_table = 'Cuentas_x_pagar'
        ordering = ['fecha_vencimiento']
