from moduloInventario.views import new_provider
from django.test.testcases import TestCase
#create_nuevo_proveedor
#Proveedor

#nombre
#razon_social
#ruc
#telefono

#primary key duplicada
class SimpleTest(TestCase):
    def tc_inventario_p001(self):
        self.assertEqual(
                         new_provider(
                                                nombre='proveedor\'s name',
                                                razon_social='EL PROVEEDOR',
                                                ruc='0930102918001',
                                                telefono='2948539'
                                                )
                         , 'El proveedor no se ha podido guardar con exito...')
    
    #ingreso exitoso
    def tc_inventario_p002(self):
        self.assertEqual(
                         new_provider(
                                                nombre='proveedor',
                                                razon_social='TU PROVEEDOR',
                                                ruc='0930102918001',
                                                telefono='2948539'
                                                )
                         ,'El proveedor no se ha podido guardar con exito...' )
    
    #primary key vacia
    def tc_inventario_p003(self):
        self.assertEqual(
                     new_provider(
                                            nombre='proveedor',
                                            razon_social='',
                                            ruc='0930102918001',
                                            telefono='2948539'
                                            )
                     ,'El proveedor no se ha podido guardar con exito...' )
    
    #RUC invalido
    def tc_inventario_p004(self):
        self.assertEqual(
                     new_provider(
                                            nombre='proveedor',
                                            razon_social='TU PROVEEDOR',
                                            ruc='123453339001',
                                            telefono='2948539'
                                            )
                     ,'El proveedor no se ha podido guardar con exito...' )
    
    #campos erroneo tipo de dato
    def tc_inventario_p005(self):
        self.assertEqual(
                     new_provider(
                                            nombre='proveedor',
                                            razon_social='JOHN, TU PROVEEDOR',
                                            ruc='no es un RUC',
                                            telefono='esto no es un telefono'
                                            )
                     ,'El proveedor no se ha podido guardar con exito...' )
#-----------------------------------------------------------------------------------------------------------------------------

