from django.db import models
from django.contrib.auth.models import User
import sys
# Create your models here.

class Tipo_Cuenta(models.Model):
    tipo_cuenta = models.CharField(max_length=50, null= False,blank=False)

    def __str__(self):
        return "{}-{}".format(self.pk,self.tipo_cuenta)

class Tipo_Transaccion(models.Model):
    tipo_transaccion = models.CharField(max_length=50, null= False,blank=False)

    def __str__(self):
        return "{}-{}".format(self.pk,self.tipo_transaccion)

class Tipo_Moneda(models.Model):
    tipo_moneda = models.CharField(max_length=10, null= False,blank=False)

    def __str__(self):
        return "{}-{}".format(self.pk,self.tipo_moneda)

# Tablas feas
class CLIENT(models.Model):
    ID = models.CharField(max_length=100, primary_key=True)
    NAME = models.CharField(max_length=250, null= False,blank=False)
    ORIGIN = models.CharField(max_length=30, null= False,blank=False)
    AGE = models.PositiveIntegerField()
    STATUS = models.CharField(max_length=10, null= False,blank=False)

    def __str__(self):
        return "{}-{}-{}".format(self.ID,self.NAME,self.STATUS)

class ACCOUNT_BANK(models.Model):
    ID = models.CharField(max_length=100, primary_key=True)
    DATES = models.CharField(max_length=8, null= False,blank=False)
    DESCR = models.CharField(max_length=500, null= False,blank=False)
    ID_CLIENT = models.CharField(max_length=100, null= False,blank=False)
    TYPE = models.CharField(max_length=1, null= False,blank=False)
    DEBT = models.FloatField(null= False,blank=False)
    CRED = models.FloatField(null= False,blank=False)
    BALANCE = models.FloatField(null= False,blank=False)

    def __str__(self):
        return "{}-{}".format(self.ID,self.ID_CLIENT,self.CRED)

#Tablas mobil
#Catalagos
class Genero(models.Model):
    descripcion_genero = models.CharField(max_length=20,null = False,blank=False)

    def __str__(self):
        return "{}-{}".format(self.pk,self.descripcion_genero)

#
class Tipo_pago(models.Model):
    descripcion_pago = models.CharField(max_length=20,null = False,blank=False)

    def __str__(self):
        return "{}-{}".format(self.pk,self.descripcion_pago)
#
class Tipo_producto(models.Model):
    descripcion_producto = models.CharField(max_length=20,null = False,blank=False)

    def __str__(self):
        return "{}-{}".format(self.pk,self.descripcion_producto)

#Transaccionales
#Empresa
class Empresa(models.Model):
    nombre_empresa = models.CharField(max_length=20,null = False,blank=False)
    logo =  models.BinaryField(blank = False, null = False, editable = True)
    descripcion = models.CharField(max_length=200)
    direccion = models.CharField( max_length=290)
    telefono = models.CharField(max_length=15)
    email = models.CharField( max_length=50)



    def __str__(self):
        return "{}-{}".format(self.pk,self.nombre_empresa)

#Poducto
class Producto(models.Model):
    nombre_producto = models.CharField(max_length=50,null = False,blank=False)
    img_producto = models.BinaryField(blank = False, null = False, editable = True)
    descripcion = models.CharField(max_length=200)
    fecha_expira = models.DateField(auto_now=False, auto_now_add=False)
    precio  =  models.DecimalField ( max_digits = 10 , decimal_places = 2 , null = True )
    cantidad  =  models.DecimalField ( max_digits = 10 , decimal_places = 2 , null = True )
    tipo_producto = models.ForeignKey(Tipo_producto,on_delete=models.CASCADE, null=False,blank=False)
    fecha_registro = models.DateField(auto_now=False)

    def __str__(self):
        return "{}-{}-{}-{}".format(self.pk,self.nombre_producto,self.tipo_producto.descripcion_producto,self.img_producto)

#Cliente
class Cliente(models.Model):
    nombres = models.CharField(max_length=100, null = False,blank=False)
    apellidos = models.CharField(max_length=100, null = False,blank=False)
    avatar =  models.BinaryField(blank = True, null = True, editable = True)
    usuario = models.ForeignKey(User,on_delete=models.CASCADE, null=False,blank=False)
    correo = models.CharField(max_length=50, null= True)
    direccion = models.CharField(max_length=100, null= False, blank = False)
    n_identidad = models.CharField(max_length=30, null= False, blank = False)
    genero = models.ForeignKey(Genero,on_delete=models.CASCADE, null=False,blank=False)
    fecha_registro = models.DateField(auto_now_add=True)
    estado = models.BooleanField()

    def __str__(self):
        return "{}-{}-{}-{}".format(self.pk,self.nombres,self.apellidos, self.usuario.username,self.usuario.pk)


#Carrito
class Carrito(models.Model):

    cantidad = models.DecimalField(max_digits=10,decimal_places=2, null=True)
    producto =  models.ForeignKey(Producto, on_delete=models.CASCADE, null=False,blank=False)
    usuario = models.ForeignKey(User,on_delete=models.CASCADE, null=True)
    def __str__(self):
        return "{}-{} |{}".format(self.pk,self.cantidad,self.producto.nombre_producto)


#Orden
class Orden(models.Model):

    carrito = models.ForeignKey(Carrito,on_delete=models.CASCADE, null=True)
    usuario = models.ForeignKey(User,on_delete=models.CASCADE, null=True)
    subtotal  =  models.DecimalField( max_digits = 10 , decimal_places = 2 , null = True )
    isv  =  models.DecimalField( max_digits = 10 , decimal_places = 2 , null = True )
    total  =  models.DecimalField( max_digits = 10 , decimal_places = 2 , null = True )
    t_pago = models.ForeignKey(Tipo_pago,on_delete=models.CASCADE, null=True)
    fecha_registro = models.DateField(auto_now_add=True)


    def __str__(self):
        return "{}-{} |{}".format(self.pk,self.carrito,self.producto.nombre_producto.nombre_producto)

#Detalle Orden
class Detalle_Orden(models.Model):
    orden = models.ForeignKey(Orden,on_delete=models.CASCADE, null=True)
    cantidad = models.DecimalField(max_digits=10,decimal_places=2, null=True)
    precio  =  models.DecimalField( max_digits = 10 , decimal_places = 2 , null = True )
    producto = models.ForeignKey(Producto,on_delete=models.CASCADE, null=True)
    total_producto = models.DecimalField(max_digits=10,decimal_places=2, null=True)

    def __str__(self):
        return "{}-{} |{}".format(self.pk,self.orden.producto.nombre_producto.nombre_producto)
