"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from moduloInventario.models import Item, Categoria, Proveedor
from moduloInventario.views import create_item


class CrearItem(TestCase):
    def setUp(self):
        Categoria.objects.create(nombre='Lentes',descripcion='fasdfasfasfas')
        Proveedor.objects.create(nombre='Angel',razon_social='Ninguna',ruc='1234567890')
        Item.objects.create(codigo='ln_001',nombre='Lentes Bifocales 001',descripcion=None,cantidad=10,costo_unitario=47.50,circulando=True,categoria=Categoria.objects.get(nombre='Lentes'),proveedor=Proveedor.objects.get(nombre='Angel'))
        
    """   
    CASO DE PRUEBA: CP_001
    DESCRIPCIPCION: Creacion exitosa de un item
    ENTRADAS:
        - pv_codigo = 'ln_002'
        - pv_nombre = 'Lentes para cerca'
        - pv_descripcion = None
        - pi_cantidad = 50
        - pf_valor = 45.89
        - pv_categoria = 'Lentes'
        - pv_proveedor = 'Ninguna'
    SALIDA ESPERADA:
        - 'Operacion Exitosa. El item se ha creado con exito.'
    PRECONDICIONES:
        - No debe existir un item con pv_codigo 'ln_002' en la base de datos
        - Para conectarse a la base lo hace por medio del usuario 'admin'
    POSTCONDICIONES:
        - El Item con pv_codigo 'ln_002' se ha insertado en la base de datos
    """
    def test_item_cp001(self):
        self.assertEqual(create_item('ln_002', 'Lentes para cerca 001', None, 50, 45.89, 'Lentes', 'Ninguna'), 'Operacion Exitosa. El item se ha creado con exito.')
        

    """   
    CASO DE PRUEBA: CP_002
    DESCRIPCIPCION: Creacion fallida de un item, item con codigo repetido
    ENTRADAS:
        - pv_codigo = 'ln_001'
        - pv_nombre = 'Lentes para cerca'
        - pv_descripcion = None
        - pi_cantidad = 50
        - pf_valor = 45.89
        - pv_categoria = 'Lentes'
        - pv_proveedor = 'Ninguna'
    SALIDA ESPERADA:
        - 'Operacion Fallida. Ya existe un item con el codigo que desea ingresar.'
    PRECONDICIONES:
        - No debe existir un item con pv_codigo 'ln_002' en la base de datos
        - Para conectarse a la base lo hace por medio del usuario 'admin'
    POSTCONDICIONES:
        - El Item con pv_codigo 'ln_001' existe en la base
    """
    def test_item_cp002(self):
        self.assertEqual(create_item('ln_001', 'Lentes para cerca 001', None, 50, 45.89, 'Lentes', 'Ninguna'), 'Operacion Fallida. Ya existe item con dicho codigo.')
    

    """   
    CASO DE PRUEBA: CP_003
    DESCRIPCIPCION: Creacion fallida de un item, categoria no existe
    ENTRADAS:
        - pv_codigo = 'ln_003'
        - pv_nombre = 'Lentes para cerca'
        - pv_descripcion = None
        - pi_cantidad = 50
        - pf_valor = 45.89
        - pv_categoria = None
        - pv_proveedor = 'Ninguna'
    SALIDA ESPERADA:
        - 'Operacion Fallida. Categoria no existe.'
    PRECONDICIONES:
        - No debe existir un item con pv_codigo 'ln_002' en la base de datos
        - Para conectarse a la base lo hace por medio del usuario 'admin'
    POSTCONDICIONES:
        - El Item con pv_codigo 'ln_003' no se inserta en la base
    """
    def test_item_cp003(self):
        self.assertEqual(create_item('ln_003', 'Lentes para cerca 001', None, 50, 45.89, None, 'Ninguna'), 'Operacion Fallida. Categoria no existe.')
    

    """   
    CASO DE PRUEBA: CP_004
    DESCRIPCIPCION: Creacion fallida de un item, proveedor no existe
    ENTRADAS:
        - pv_codigo = 'ln_004'
        - pv_nombre = 'Lentes para cerca'
        - pv_descripcion = None
        - pi_cantidad = 50
        - pf_valor = 45.89
        - pv_categoria = 'Lentes'
        - pv_proveedor = 'ESPOL'
    SALIDA ESPERADA:
        - 'Operacion Fallida. Categoria no existe.'
    PRECONDICIONES:
        - No debe existir un item con pv_codigo 'ln_002' en la base de datos
        - Para conectarse a la base lo hace por medio del usuario 'admin'
    POSTCONDICIONES:
        - El Item con pv_codigo 'ln_004' no se inserta en la base
    """
    def test_item_cp004(self):
        self.assertEqual(create_item('ln_004', 'Lentes para cerca 001', None, 50, 45.89, 'Lentes', 'ESPOL'), 'Operacion Fallida. Proveedor no existe.')
    

    """   
    CASO DE PRUEBA: CP_005
    DESCRIPCIPCION: Creacion fallida de un item, se envia NULL en un campo requerido
    ENTRADAS:
        - pv_codigo = 'ln_005'
        - pv_nombre = None
        - pv_descripcion = None
        - pi_cantidad = 50
        - pf_valor = 45.89
        - pv_categoria = 'Lentes'
        - pv_proveedor = 'Ninguna'
    SALIDA ESPERADA:
        - 'Operacion Fallida. Categoria no existe.'
    PRECONDICIONES:
        - No debe existir un item con pv_codigo 'ln_002' en la base de datos
        - Para conectarse a la base lo hace por medio del usuario 'admin'
    POSTCONDICIONES:
        - El Item con pv_codigo 'ln_005' no se inserta en la base
    """
    def test_item_cp005(self):
        self.assertEqual(create_item('ln_005', None, None, 50, 45.89, 'Lentes', 'Ninguna'), 'Operacion Fallida. Algun campo requerido se ha enviado vacio.')
    

    """   
    CASO DE PRUEBA: CP_006
    DESCRIPCIPCION: Creacion fallida de un item, tipos de dato no coinciden
    ENTRADAS:
        - pv_codigo = 'ln_006'
        - pv_nombre = 'Lentes para cerca'
        - pv_descripcion = None
        - pi_cantidad = 'Cero'
        - pf_valor = 45.89
        - pv_categoria = 'Lentes'
        - pv_proveedor = 'Ninguna'
    SALIDA ESPERADA:
        - 'Operacion Fallida. Categoria no existe.'
    PRECONDICIONES:
        - No debe existir un item con pv_codigo 'ln_002' en la base de datos
        - Para conectarse a la base lo hace por medio del usuario 'admin'
    POSTCONDICIONES:
        - El Item con pv_codigo 'ln_006' no se inserta en la base
    """
    def test_item_cp006(self):
        self.assertEqual(create_item('ln_006', 'Lentes para cerca', None, 'Cero', 45.89, 'Lentes', 'Ninguna'), 'Operacion Fallida. En algun campo se esta enviando un tipo de dato incorrecto.')


class EliminarItem(TestCase):
    def setUp(self):
        Item.objects.create(codigo='ln_002',nombre='Lentes Bifocales 001',descripcion=None,cantidad=10,costo_unitario=47.50,circulando=True,categoria=Categoria.objects.get(nombre='Lentes'),proveedor=Proveedor.objects.get(nombre='Proveedor1'))