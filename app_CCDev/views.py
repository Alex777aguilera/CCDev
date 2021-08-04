from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect,JsonResponse, HttpResponse
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