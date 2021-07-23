from django.shortcuts import render
from django.http import HttpResponseRedirect,JsonResponse, HttpResponse
from django.urls import reverse
from django.contrib.auth import login as auth_login,logout,authenticate
from django.db import transaction,connections #manejo de base de datos
import json, re, os
from app_CCDev.models import *
from django.contrib.auth.decorators import login_required, permission_required
from django.core import serializers
from django.contrib.auth.hashers import make_password

from rest_framework import serializers
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
# Create your views here.

def principal(request):
	return render(request,'principal_base.html')
		
def otra_view(request):
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