from django.db import models
from moduloClientes.models import Cliente
from moduloInventario.models import Item

TIPO_PAGO_CHOICES = (('EFECTIVO', 'Efectivo'),
                 ('CHEQUE', (('PCF','Banco Pacifico'),
                          ('PCH','Banco de Pichincha'),
                          ('GYQ','Banco de Guayaquil'),
                          ('AMZ','Banco Amazonas'),
                          ('PRO','Banco Produbanco'),
                          ('CTR','Banco Central del Ecuado'),
                          ('SLD','Banco Solidario'),
                          ('PRM','Banco Promerica'),
                          ('INT','Banco Internacional'),
                          ('BNF','Banco Nacional de Fomento'),
                          ('BGR','Banco General Ruminahui'),
                          ('LOJ','Banco de Loja'),
                          ('AUS','Banco del Austro'),
                          ('BLV','Banco Bolivariano'),
                          ('MCH','Banco de Machala'),
                          ('BCN','Banco Coopnacional'),
                          ('UNB','Banco Unibanco'),
                          )),
                 ('TARJETA_CREDITO',(('VIS','Visa'),
                                         ('MTC','Master Card'),
                                         ('AME','American Express'),
                                         ('CUO','Cuota Facil'),
                                         )),
                  ('TARJETA_DEBITO',(('PCF','Banco Pacifico'),
                                          ('PCH','Banco de Pichincha'),
                                          ('GYQ','Banco de Guayaquil'),
                                          ('AMZ','Banco Amazonas'),
                                          ('PRO','Banco Produbanco'),
                                          ('CTR','Banco Central del Ecuado'),
                                          ('SLD','Banco Solidario'),
                                          ('PRM','Banco Promerica'),
                                          ('INT','Banco Internacional'),
                                          ('BNF','Banco Nacional de Fomento'),
                                          ('BGR','Banco General Ruminahui'),
                                          ('LOJ','Banco de Loja'),
                                          ('AUS','Banco del Austro'),
                                          ('BLV','Banco Bolivariano'),
                                          ('MCH','Banco de Machala'),
                                          ('BCN','Banco Coopnacional'),
                                          ('UNB','Banco Unibanco'),
                                          ))
                  ,)

class OrdenPedido(models.Model):
    codigo = models.CharField(primary_key=True,max_length=10, unique=True)
    codigo_factura = models.CharField(null=True, max_length=20)
    fecha_compra = models.DateField()
    fecha_facturacion = models.DateField(null=True)#poner la fecha actual por defecto
    cliente = models.ForeignKey(Cliente)
    items = models.ManyToManyField(Item, through='Item_OrdenPedido_Cantidad')
    detalle = models.TextField(null=True, max_length=50)
    
    def __str__(self):
        return '%s'% (self.codigo)
    
    class Meta:
        db_table = 'Orden_Pedido'
        ordering = ['fecha_compra']
        
    class Admin:
        pass
        
class Item_OrdenPedido_Cantidad(models.Model):
    orden_pedido = models.ForeignKey(OrdenPedido)
    item = models.ForeignKey(Item)
    cantidad = models.IntegerField()
    #precios varian de acuerdo a promociones y valor compra de proveedores
    precio_venta_unitario = models.DecimalField(max_digits=8, decimal_places=4)
    #porcentaje validado en front end que sea menor que 100
    porcentaje_descuento = models.DecimalField(null=True,max_digits=8, decimal_places=4 )
    
    def __str__(self):
        return '<%s,%s,%d>'% (self.item,self.orden_pedido,self.cantidad)
    
    class Admin:
        pass
    
    class Meta:
        db_table = 'Item_OrdenPedido_Cantidad'
    
class Abono(models.Model):
    fecha = models.DateField()
    orden_pedido = models.ForeignKey(OrdenPedido)
    tipo_pago = models.CharField(max_length=30,choices=TIPO_PAGO_CHOICES)
    monto = models.DecimalField(max_digits=8, decimal_places=4)
    
    class Meta:
        db_table = 'Abono'
        ordering = ['fecha']
    
    class Admin:
        pass
    
    
    