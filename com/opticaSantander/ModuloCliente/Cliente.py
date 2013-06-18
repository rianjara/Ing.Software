'''
Created on 15/06/2013

@author: An�bal
'''

class Cliente(object):
    '''
    Clase Cliente permite instanciar un cliente con informaci�n relevante de este
    para facturaci�n y mantenimiento de historia cl�nica
    '''


    def __init__(self, nombre, apellido1, apellido2, razonSocial = None, cedula, telefono = None, direccion = None, eMail = None):
        
        #Constructor recibe como par�metros obligatorios:
        #-Nombre del cliente
        #-Primer Apellido del Cliente
        #-Segundo Apellido del Cliente
        #-C�dula
        
        #recibe como par�metros opcionales:
        #-Raz�n Social en caso de ser una empresa
        #-tel�fono del cliente
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