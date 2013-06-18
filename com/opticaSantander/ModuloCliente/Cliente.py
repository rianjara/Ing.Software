'''
Created on 15/06/2013

@author: Aníbal
'''

class Cliente(object):
    '''
    Clase Cliente permite instanciar un cliente con información relevante de este
    para facturación y mantenimiento de historia clínica
    '''


    def __init__(self, nombre, apellido1, apellido2, razonSocial = None, cedula, telefono = None, direccion = None, eMail = None):
        
        #Constructor recibe como parámetros obligatorios:
        #-Nombre del cliente
        #-Primer Apellido del Cliente
        #-Segundo Apellido del Cliente
        #-Cédula
        
        #recibe como parámetros opcionales:
        #-Razón Social en caso de ser una empresa
        #-teléfono del cliente
        #-direccion del cliente o empresa
        #-e-mail *varios valores
        
        self.nombre = nombre
        self.apellido1 = apellido1
        self.apellido2 = apellido2
        self.cedula = cedula
        if razonSocial is not None:
            self.razonSocial = razonSocial
        else:
            self.razonSocial ='%s %s %s' %(nombre,apellido1,apellido2)
        self.telefono = telefono
        self.direccion = direccion
        self.eMail = eMail        