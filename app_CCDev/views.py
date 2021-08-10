from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth import login as auth_login,logout,authenticate
from django.db import transaction,connections #manejo de base de datos
import json, re, os
from app_CCDev.models import *
from django.contrib.auth.decorators import login_required, permission_required
from django.core import serializers
from django.contrib.auth.hashers import make_password
import requests


from rest_framework import serializers
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
# Create your views here.

def principal(request):
	return render(request,'principal_base.html')

# def cerrar_sesion(request):
# 	logout(request)
# 	return HttpResponseRedirect(reverse('Iuth_app:login'))


def otra_view(request):
	CAPI(request)
	return render(request,'inicio.html')

class Apisend(APIView):
	ctx = {}
	def get(self, request, format=None):
		clientes = list(Cliente.objects.all().values('id','nombres','apellidos','usuario','fecha_registro','estado'))

		if clientes:
			ctx = {'clientes':clientes}
			
			return Response(ctx)
		else:
			ctx = {'error','No hay Registros'}
			return Response(ctx)


def CAPI(request):
	ctx = {}
	Dapi = requests.get('https://ccdevp.herokuapp.com/vista/ApiCliente')
	Data = Dapi.json()
	print (Data)
	# if Data:
	# 	ctx = {'books':books['results']}
	# else:
	# 	ctx = {'books':books['results']}	
	return render(request,'inicio.html')

# @login_required
def Vista_Tcuenta(request):
	Tcuentas = Tipo_Cuenta.objects.all()

	if request.user.is_superuser:
		ret_data,query_Tcuenta,errores = {},{},{}

		if request.method == 'POST':
			ret_data['tipo_cuenta'] = request.POST.get('tipo_cuenta')
			
			if request.POST.get('tipo_cuenta') == '':
				errores['tipo_cuenta'] = "Debe ingresar El tipo de cuenta"
			elif Tipo_Cuenta.objects.filter(tipo_cuenta = request.POST.get('tipo_cuenta')).exists(): 
				#Si el registro ya existe en la base de datos
				errores['existe'] = 'Tipo de Cuenta existente!!'		
			else:
				query_Tcuenta['tipo_cuenta'] = request.POST.get('tipo_cuenta')

			print(errores)

			if not errores:
				try:
					tcuenta = Tipo_Cuenta(**query_Tcuenta)
					tcuenta.save()
					pass
				except Exception as e:
					transaction.rollback()
					errores['administrador'] = e
					ctx = {'Tcuentas':Tcuentas,'errores':errores,'ret_data':ret_data}

					return render(request,'Vista_Tcuenta.html',ctx)
				else:
					transaction.commit()
					return HttpResponseRedirect(reverse('app_CCDev:Vista_Tcuenta')+'?ok')
			else:
				ctx = {'Tcuentas':Tcuentas,'errores':errores,'ret_data':ret_data}
				return render(request,'Vista_Tcuenta.html',ctx)
		else:
			ctx = {'Tcuentas':Tcuentas}
			return render(request,'Vista_Tcuenta.html',ctx)
	else:
		return redirect('app_CCDev:principal')	

# Registro Vista Cliente
def Vista_Cliente(request):
	Clients = CLIENT.objects.all()
	CAPIClient(request)
	CAPIACCOUNT_BANK(request)
	if request.user.is_superuser:
		query_CLEINT,errores = {},{}

		if request.method == 'POST':
			
			# ID
			if request.POST.get('ID') == '':
				errores['ID'] = "Debe ingresar El ID"
			elif CLIENT.objects.filter(ID = request.POST.get('ID')).exists(): 
				#Si el registro ya existe en la base de datos
				errores['existe'] = 'ID ya Existente!!'		
			else:
				query_CLEINT['ID'] = request.POST.get('ID')
			# NAME
			if request.POST.get('NAME') == '':
				errores['NAME'] = "Debe ingresar el nombre"
			else:
				query_CLEINT['NAME'] = request.POST.get('NAME')
			# ORIGIN
			if request.POST.get('ORIGIN') == '':
				errores['ORIGIN'] = "Debe ingresar el origen"
			else:
				query_CLEINT['ORIGIN'] = request.POST.get('ORIGIN')
			# AGE
			if request.POST.get('AGE') == '':
				errores['AGE'] = "Debe ingresar la edad"
			else:
				query_CLEINT['AGE'] = request.POST.get('AGE')
			# STATUS
			if request.POST.get('STATUS') == '':
				errores['STATUS'] = "Debe ingresar el estado"
			else:
				query_CLEINT['STATUS'] = request.POST.get('STATUS')

			print(errores)

			if not errores:
				try:
					cliente = CLIENT(**query_CLEINT)
					cliente.save()
					
				except Exception as e:
					transaction.rollback()
					errores['administrador'] = e
					ctx = {'Clients':Clients,'errores':errores}

					return render(request,'Vista_Cliente.html',ctx)
				else:
					transaction.commit()
					return HttpResponseRedirect(reverse('app_CCDev:Vista_Cliente')+"?ok")
			else:
				ctx = {'Clients':Clients,'errores':errores}
				return render(request,'Vista_Cliente.html',ctx)
		else:
			ctx = {'Clients':Clients}
			return render(request,'Vista_Cliente.html',ctx)
	else:
		return redirect('app_CCDev:principal')	

# Registro Vista Cuenta de banco
def Vista_CBanco(request):
	Cuentas = ACCOUNT_BANK.objects.all()
	# CAPIClient(request)
	# CAPIACCOUNT_BANK(request)
	if request.user.is_superuser:
		query_CBanck,errores = {},{}

		if request.method == 'POST':
			balance = 0
			# ID
			if request.POST.get('ID') == '':
				errores['ID'] = "Debe ingresar El ID"
			elif ACCOUNT_BANK.objects.filter(ID = request.POST.get('ID')).exists(): 
				#Si el registro ya existe en la base de datos
				errores['existe'] = 'ID ya Existente!!'		
			else:
				query_CBanck['ID'] = request.POST.get('ID')
			# DATES
			if request.POST.get('DATES') == '':
				errores['DATES'] = "Debe ingresar los datos"
			else:
				query_CBanck['DATES'] = request.POST.get('DATES')
			# DESCR
			if request.POST.get('DESCR') == '':
				errores['DESCR'] = "Debe ingresar la descripcion"
			else:
				query_CBanck['DESCR'] = request.POST.get('DESCR')
			# ID_CLIENT
			if request.POST.get('ID_CLIENT') == '':
				errores['ID_CLIENT'] = "Debe ingresar el cliente"
			else:
				query_CBanck['ID_CLIENT'] = request.POST.get('ID_CLIENT')
			# TYPE
			if request.POST.get('TYPE') == '':
				errores['TYPE'] = "Debe ingresar el tipo"
			else:
				query_CBanck['TYPE'] = request.POST.get('TYPE')
			# DEBT
			if request.POST.get('DEBT') == '':
				errores['DEBT'] = "Debe ingresar el debito"
			else:
				query_CBanck['DEBT'] = request.POST.get('DEBT')
				debito = float(request.POST.get('DEBT'))
			# CRED
			if request.POST.get('CRED') == '':
				errores['CRED'] = "Debe ingresar el credito"
			else:
				query_CBanck['CRED'] = request.POST.get('CRED')
				credito = float(request.POST.get('CRED'))
			# BALANCE
			balance = (credito - debito)
			if debito > credito:
				errores['BALANCE'] = "Debito sobrepasa al credito!!"
			else:
				query_CBanck['BALANCE'] = float(balance)
				print(query_CBanck['BALANCE'])
			

			if not errores:
				try:
					Ccuenta = ACCOUNT_BANK(**query_CBanck)
					Ccuenta.save()
					
				except Exception as e:
					transaction.rollback()
					errores['administrador'] = e
					print(e)
					ctx = {'Cuentas':Cuentas,'errores':errores}

					return render(request,'Vista_CBanco.html',ctx)
				else:
					transaction.commit()
					return HttpResponseRedirect(reverse('app_CCDev:Vista_CBanco')+"?ok")
			else:
				print(errores)
				ctx = {'Cuentas':Cuentas,'errores':errores}
				return render(request,'Vista_CBanco.html',ctx)
		else:
			ctx = {'Cuentas':Cuentas}
			return render(request,'Vista_CBanco.html',ctx)
	else:
		return redirect('app_CCDev:principal')	


# Envio de Api
#API CLIENTE
class ApisendCLIENT(APIView):
	ctx = {}
	def get(self, request, format=None):
		clientes = list(CLIENT.objects.all().values('ID','NAME','ORIGIN','AGE','STATUS'))
		
		if clientes:
			ctx = {'clientes':clientes}
			return Response(ctx)
		else:
			ctx = {'error','No hay Registros'}
			return Response(ctx)

def CAPIClient(request):
	url = requests.get('http://127.0.0.1:8000/vista/ApisendCLIENT')
	
	if url.status_code == 200:
		Data = url.json()
		ApiData = Data['clientes']
		for i in range(0,len(ApiData)):
			
			a = ApiData[i]
			id = a['ID']
			nombre = a['NAME']
			origen = a['ORIGIN']
			edad = a['AGE']
			estado = a['STATUS']
			print(type(id))
			print(type(edad))

			if CLIENT.objects.filter(ID = id).exists():
				print('existe ese id')
			else:
				print('no existe, se almacenara')
		


#API ACCOUNT_BANK
class ApisendACCOUNT_BANK(APIView):
	ctx = {}
	def get(self, request, format=None):
		CBancos = list(ACCOUNT_BANK.objects.all().values('ID','DATES','DESCR','ID_CLIENT','TYPE','DEBT','CRED','BALANCE'))
		
		if CBancos:
			ctx = {'CBancos':CBancos}
			return Response(ctx)
		else:
			ctx = {'error','No hay Registros'}
			return Response(ctx)

#API captura de datos de ACCOUNT BANK
def CAPIACCOUNT_BANK(request):
	url = requests.get('http://127.0.0.1:8000/vista/ApisendACCOUNT_BANK')
	
	if url.status_code == 200:
		Data = url.json()
		ApiData = Data['CBancos']
		for i in range(0,len(ApiData)):
			
			a = ApiData[i]
			id = a['ID']
			datos = a['DATES']
			descripcion = a['DESCR']
			cliente = a['ID_CLIENT']
			estado = a['TYPE']
			debito = a['DEBT']
			credito = a['CRED']
			balance = a['BALANCE']
			print(type(id))
			print(type(balance))

			if ACCOUNT_BANK.objects.filter(ID = id).exists():
				print('existe ese id')
			else:
				print('no existe, se almacenara')