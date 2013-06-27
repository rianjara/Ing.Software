from django.db import models

class Cliente(models.Model):
    cedula = models.CharField(max_length=10,null=True)
    nombre = models.CharField(max_length=30)
    apellido1 = models.CharField(max_length=30,null=True)
    apellido2 = models.CharField(max_length=30,null=True)
    fecha_nacimiento = models.DateField(null=True)
    #maximo cuatro telefonos separados por coma
    telefonos = models.CharField(max_length=43)
    direccion = models.CharField(max_length=100)
    e_mail1 = models.EmailField(null=True)
    e_mail2 = models.EmailField(null=True)
    ruc = models.CharField(max_length=15)
    
    def __str__(self):
        return '%s %s' %(self.cedula,self.nombre)
    #"<td>A"+((i/10>=1)?"0"+i:"00"+i)+"TB</td><td>Item"+i+"</td><td>Detalle"+i+"</td><td>$"+i+",00</td><td>"+i+"</td><td width=\"50\">"+btnEdit+btnElim+"</td>"
    
    def get_fields(self):
        return  [(field.name, field.value) for field in Cliente._meta.fields]
        
    class Meta:
        ordering =["nombre"]
                
    class Admin():
        pass

class Consultas(models.Model):
    EYE_CHOICES = (('IZQUIERDO', 'Ojo Izquierdo'),('DERECHO', 'Ojo Derecho'),)
    VISION_CHOICES = (('CERCA', 'Vision de Cerca'),('LEJOS', 'Vision de Lejos'),)
    ESTADO_CHOICES=(('PENDIENTE', 'Consulta Pendiente'),('REALIZADA', 'Consulta Realizada'),('Proceso', 'Consulta en Proceso'),)
    cliente=models.ForeignKey(Cliente)
    esfera=models.DecimalField(max_digits=5,decimal_places=3)
    cilindro=models.DecimalField(max_digits=5,decimal_places=3)
    eje=models.IntegerField(max_length=4)
    av=models.DecimalField(max_digits=5,decimal_places=3)
    add=models.DecimalField(max_digits=5,decimal_places=3)
    dp=models.DecimalField(max_digits=5,decimal_places=3)
    fecha=models.DateField()
    Diagnostico = models.CharField(max_length=200,null=True)
    Observaciones = models.CharField(max_length=200,null=True)
    vista = models.CharField(choices=VISION_CHOICES,max_length=15)
    ojo = models.CharField(choices=EYE_CHOICES,max_length=15)      
    estado = models.CharField(choices=ESTADO_CHOICES,max_length=15)
    
    class Meta:
        ordering=["fecha"]
        
        
        
    