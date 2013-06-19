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
        return '\"<td>%s</td><td>%s %s %s</td><td>%s</td><td>%s</td><td>%s</td><td width=\"50\">"+btnEdit+btnElim+"</td>\"' %(self.cedula,self.nombre,self.apellido1,self.apellido2,self.telefonos,self.direccion,self.e_mail1)
    #"<td>A"+((i/10>=1)?"0"+i:"00"+i)+"TB</td><td>Item"+i+"</td><td>Detalle"+i+"</td><td>$"+i+",00</td><td>"+i+"</td><td width=\"50\">"+btnEdit+btnElim+"</td>"
    
    def get_fields(self):
        return  [(field.name, field.value) for field in Cliente._meta.fields]
        
    class Meta:
        ordering =["nombre"]
                
    class Admin():
        pass