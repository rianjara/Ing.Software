from django.test import TestCase
from moduloClientes.views import create_nuevo_cliente, create_nueva_consulta

class SimpleTest(TestCase):

#create_nuevo_cliente
#cedula=aaaaaaaaaa
#nombre= Pepito
#apellido1=Apellido1
#apellido2=Apellido2
#telefonos=telefono10
#direccion=Avenida123
#e_mail1=email1@mail.com
#e_mail2=email2@mail.com
#ruc=aaaaaaaaaaaaa
    def tc_001(self):
        self.assertEqual(create_nuevo_cliente(cedula='aaaaaaaaaa',
                                              nombre='Pepito',
                                              apellido1='Apellido1',
                                              apellido2='Apellido2',
                                              telefonos='telefono10',
                                              direccion='Avenida123',
                                              e_mail1='email1@mail.com',
                                              e_mail2='email2@mail.com',
                                              ruc='aaaaaaaaaaaaa'), 'El cliente no se pudo crear')
    
    '''
    cedula=1234567890
    nombre= Pepito
    apellido1=Apellido1
    apellido2=Apellido2
    telefonos=042445566
    direccion=Avenida 123
    e_mail1=email1@mail.com
    e_mail2=email2@mail.com
    ruc=1234567890001'''
    def tc_002(self):
        self.assertEqual(create_nuevo_cliente(cedula='1234567890',
                                              nombre='Pepito',
                                              apellido1='Apellido1',
                                              apellido2='Apellido2',
                                              telefonos='telefono10',
                                              direccion='Avenida123',
                                              e_mail1='email1@mail.com',
                                              e_mail2='email2@mail.com',
                                              ruc='1234567890001'), 'El cliente no se pudo crear')
    '''
    cedula=1234567890
    nombre= 
    apellido1=Apellido1
    apellido2=Apellido2
    telefonos=
    direccion=
    e_mail1=email1@mail.com
    e_mail2=email2@mail.com
    ruc='''
    def tc_003(self):
        self.assertEqual(create_nuevo_cliente(cedula='1234567890',
                                              apellido1='Apellido1',
                                              apellido2='Apellido2',
                                              e_mail1='email1@mail.com',
                                              e_mail2='email2@mail.com',), 'El cliente no se pudo crear')
    '''
    cedula=0929791648
    nombre= Anibal
    apellido1=Vasuqez
    apellido2=Clad
    telefonos=042478645
    direccion=19 E/ Maldonado y Calicuchima
    e_mail1=aniavasq@gmail.com
    e_mail2=aniavasq@espol.edu.ec
    ruc=0929791648001'''
    def tc_004(self):
        self.assertEqual(create_nuevo_cliente(cedula='0929791648',
                                              nombre='Anibal',
                                              apellido1='Vasuqez',
                                              apellido2='Clad',
                                              telefonos='042478645',
                                              direccion='19 E/ Maldonado y Calicuchima',
                                              e_mail1='aniavasq@gmail.com',
                                              e_mail2='aniavasq@espol.edu.ec',
                                              ruc='0929791648001'), 'Creación de cliente exitosa')
    
    #-----------------------------------------------------------------------------------------------------------------------------
    
    #nueva_consulta
    
    #valores no numericos en el campo esfera
    def tc_consulta_p001(self):
        self.assertEqual(
                         create_nueva_consulta(
                                        esfera='nada',
                                        cilindro=0.89,
                                        eje=190,
                                        av=0.34,
                                        add=0.30,
                                        dp=0.40,
                                        fecha='1990-03-03',
                                        Diagnostico='Miopia',
                                        Observaciones='NN',
                                        vista='CERCA',
                                        ojo='DERECHO',
                                        estado='PENDIENTE')
                         ,'Tipo de datos inválido...' )
    #valores de eje ingresado de forma errónea
         
    def tc_consulta_p002(self):
        self.assertEqual(
                         create_nueva_consulta(
                                        esfera=0.90,
                                        cilindro=0.89,
                                        eje=190,
                                        av=0.34,
                                        add=0.30,
                                        dp=0.40,
                                        fecha='1990-03-03',
                                        Diagnostico='Miopia',
                                        Observaciones='NN',
                                        vista='CERCA',
                                        ojo='DERECHO',
                                        estado='PENDIENTE')
                         ,'El valor del eje debe ser menor de 180 grados...' )
    
    #Datos no ingresados en campos obligatorios
    def tc_consulta_p003(self):
        self.assertEqual(
                         create_nueva_consulta(
                                        esfera='',
                                        cilindro='',
                                        eje=180,
                                        av=0.34,
                                        add=0.30,
                                        dp=0.40,
                                        fecha='1990-03-03',
                                        Diagnostico='Miopia',
                                        Observaciones='NN',
                                        vista='CERCA',
                                        ojo='DERECHO',
                                        estado='PENDIENTE')
                         ,'Los campos esfera y cilindro son obligatorios...' )
    
    #Consulta ingresada de forma exitosa
    def tc_consulta_p004(self):
        self.assertEqual(
                      create_nueva_consulta(
                                        esfera=0.80,
                                        cilindro=-0.10,
                                        eje=180,
                                        av=0.34,
                                        add=0.30,
                                        dp=0.40,
                                        fecha='1990-03-03',
                                        Diagnostico='Miopia',
                                        Observaciones='NN',
                                        vista='CERCA',
                                        ojo='DERECHO',
                                        estado='PENDIENTE')
                     ,'La consulta se creó con éxito..' )