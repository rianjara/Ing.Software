from django.db import models
from moduloInventario.models import Orden_Compra,Detalle_Orden_Compra

class Gastos(models.Model):
    """
    Genera un nuevo modelo llamado Gastos .

    """
    concepto = models.CharField(null=True, max_length=30)
    valor_gasto = models.DecimalField(max_digits=5,decimal_places=3)
    fecha_gasto = models.DateField(null=True)
    beneficiario = models.CharField(null=True, max_length=20)
    factura=models.IntegerField(max_length=10)
    
    
    def __str__(self):
        return '%s'% (self.valor_gasto)
    
    class Meta:
        """
        Establece el nombre de la tabla con un orden en base al campo fecha_gasto.

        """
        db_table = 'Gastos'
        ordering = ['fecha_gasto']
        
class Cuentas_x_pagar(models.Model):
    """
    Genera una nuevo modelo cuentas por pagar relacionada con :model:`moduloInventario.Detalle_Orden_Compra`.

    """
    Detalle_Orden_Compra = models.ForeignKey(Detalle_Orden_Compra)
    fecha_vencimiento = models.DateField(null=True)
   
    
    
    def __str__(self):
        return '%s'% (self.valor_gasto)
    
    class Meta:
        """
        Asigna un nombre a la tabla Cuentas_x_pagar siguiendo un orden de acuerdo a fecha de nacimiento`.

        """
        db_table = 'Cuentas_x_pagar'
        ordering = ['fecha_vencimiento']
