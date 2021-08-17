from django.db import models
from django.contrib.auth.models import User
import sys
# Create your models here.

class Cliente(models.Model):
    nombres = models.CharField(max_length=100, null = False,blank=False)
    apellidos = models.CharField(max_length=100, null = False,blank=False)
    usuario = models.ForeignKey(User,on_delete=models.CASCADE, null=False,blank=False)
    fecha_registro = models.DateField(auto_now_add=True)
    estado = models.BooleanField()

    def __str__(self):
        return "{}-{}-{}-{}".format(self.pk,self.nombres,self.apellidos, self.usuario.username)

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


class Cuenta(models.Model):
    id_cliente = models.ForeignKey(Cliente,on_delete=models.CASCADE, null=False,blank=False)
    id_tipo_cuenta = models.ForeignKey(Tipo_Cuenta,on_delete=models.CASCADE, null=False,blank=False)
    fecha_creacion = models.DateField(auto_now_add=True)
    saldo_inicial = models.DecimalField(decimal_places=2, max_digits=6,null=False,blank=False)
    saldo_anterior = models.DecimalField(decimal_places=2, max_digits=6,null=False,blank=False,default=0)
    saldo_actual = models.DecimalField(decimal_places=2, max_digits=6,null=False,blank=False)

    def __str__(self):
        return "{}-{}-{}-{}".format(self.pk,self.id_cliente.nombres,self.id_cliente.apellidos,self.id_tipo_cuenta.tipo_cuenta)


class Transacciones(models.Model):
    id_cuenta = models.ForeignKey(Cuenta,on_delete=models.CASCADE, null=True)
    id_cliente = models.ForeignKey(Cliente,on_delete=models.CASCADE, null=True)
    id_tipo_transaccion = models.ForeignKey(Tipo_Transaccion,on_delete=models.CASCADE, null=True)
    fecha_transaccion = models.DateField(auto_now_add=True)
    saldo_actual = models.DecimalField(decimal_places=2, max_digits=6,null=False,blank=False)
    saldo_anterior = models.DecimalField(decimal_places=2, max_digits=6,null=False,blank=False,default=0)
    usuario = models.CharField(max_length=50,null=False,blank=False)
    id_tipo_moneda = models.ForeignKey(Tipo_Moneda,on_delete=models.CASCADE, null=True)

    def __str__(self):
        return "{}-{}-{}-{}".format(self.pk,self.id_cuenta,self.id_cliente.nombres,self.id_cliente.apellidos,self.id_tipo_transaccion.tipo_transaccion)

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
