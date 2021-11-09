from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth import login as auth_login,logout,authenticate
from django.db import transaction,connections #manejo de base de datos
import json, re, os
from app_CCDev.models import *
from django.contrib.auth.decorators import login_required, permission_required
from django.core import serializers

from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from django.contrib.auth.hashers import make_password
import requests
import json
import base64

from rest_framework import serializers
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
# Create your views here.

def principal(request):
	return render(request,'principal_base.html')


def cerrar_sesion(request):
	logout(request)
	return HttpResponseRedirect(reverse('app_CCDev:principal'))

@login_required
def otra_view(request):
	CAPI(request)
	return render(request,'inicio.html')

def login(request):
	mensaje=''
	if request.method == 'POST':
		username = request.POST.get('usuario')
		contrasenia = request.POST.get('contrasenia')
		user = authenticate(username=username,password=contrasenia)
		if user is not None:
			if user.is_active:
				auth_login(request,user)
				return redirect('app_CCDev:principal')
			else:
				mensaje = 'USUARIO INACTIVO'
				return render(request,'lg.html',{'mensaje':mensaje})
		else:
			mensaje = 'USUARIO O CONTRASEÑA INCORRECTO'
			return render(request,'lg.html',{'mensaje':mensaje})

	return render(request,'lg.html')
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

@login_required
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
@login_required
def Vista_Cliente(request):
	Clients = CLIENT.objects.all()
	# CAPIClient(request)
	# CAPIACCOUNT_BANK(request)
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
				query_CLEINT['AGE'] = int(request.POST.get('AGE'))
			# STATUS
			if request.POST.get('STATUS') == '':
				errores['STATUS'] = "Debe ingresar el estado"
			else:
				query_CLEINT['STATUS'] = request.POST.get('STATUS')

			print(errores)

			if not errores:
				try:
					cliente = CLIENT(**query_CLEINT)

					# response = requests.post('https://radiant-journey-28507.herokuapp.com/buscarClientes.php', json = query_CLEINT)

					print(query_CLEINT)
					response = ''
					response = requests.post('https://radiant-journey-28507.herokuapp.com/api.php', json = query_CLEINT)

					if response.status_code == 200:
						Data = response.json()
					# 	print(Data)
					# Api Grupo Java
					response2 = ''
					response2 = requests.post('http://167.99.158.191/api_cloud_computing/clientes.php', json = query_CLEINT)

					if response2.status_code == 200:
						Data2 = response.json()
						print(Data2)
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

# Modificar CLIENT
@login_required
def modificar_CLIENT(request,id_CLIENT):
	if request.user.is_superuser:

		errores = {}
		clientes = CLIENT.objects.filter(ID=id_CLIENT)

		if request.method == 'POST':

			if request.POST.get('NAME') == '' or request.POST.get('ORIGIN') == '' or request.POST.get('AGE') == '' or request.POST.get('STATUS') == '':
				errores['NAME'] = "HAY ERRORES"

			if not errores:
				try:
					cliente = CLIENT.objects.filter(ID=id_CLIENT).update(
																			NAME = request.POST.get('NAME'),
																			ORIGIN = request.POST.get('ORIGIN'),
																			AGE = request.POST.get('AGE'),
																			STATUS = request.POST.get('STATUS'),
																			)
					clu = {"ID":str(id_CLIENT),
						  "NAME":request.POST.get('NAME'),
						  "ORIGIN":request.POST.get('ORIGIN'),
						  "AGE":int(request.POST.get('AGE')),
						  "STATUS":request.POST.get('STATUS')
						}
					response = ''
					response = requests.put('https://radiant-journey-28507.herokuapp.com/api.php', json = clu)

					if response.status_code == 200:
						Data = response.json()
						# print(Data)
					# Api grup Java
					response2 = ''
					response2 = requests.put('http://167.99.158.191/api_cloud_computing/clientes.php', json = clu)

					if response2.status_code == 200:
						Data2 = response.json()
						print(Data2)

				except Exception as e:
					transaction.rollback()
					errores['administrador'] = e
					ctx = {'clientes':clientes,'errores':errores}

					return render(request,'Vista_Cliente.html',ctx)
				else:
					transaction.commit()


					return HttpResponseRedirect(reverse('app_CCDev:Vista_Cliente')+"?ok")
			else:
				ctx = {'clientes':clientes,'errores':errores}
				return render(request,'Vista_Cliente.html',ctx)
		else:
			ctx = {'clientes':clientes}
			return render(request,'Modificar_Cliente.html',ctx)
	else:
		return redirect('app_CCDev:principal')

#Eliminar cliente
@login_required
def Eliminar_cliente(request,id_cliente):
	ctx ={}

	eliminar = CLIENT.objects.get(pk=id_cliente).delete()
	ctx = {"id":id_cliente}
	response = ''
	response = requests.delete('https://radiant-journey-28507.herokuapp.com/api.php', json = ctx)

	if response.status_code == 200:
		Data = response.json()
		# print(Data)
	# Api Grup Java
	ctx2 ={}

	ctx2 = {"ID":id_cliente}
	response2 = ''
	response2 = requests.delete('http://167.99.158.191/api_cloud_computing/clientes.php', json = ctx2)

	if response2.status_code == 200:
		Data2 = response2.json()
		print(Data2)


	return HttpResponseRedirect(reverse('app_CCDev:Vista_Cliente'))

# Registro Vista Cuenta de banco
@login_required
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
				query_CBanck['DEBT'] = float(request.POST.get('DEBT'))
				debito = float(request.POST.get('DEBT'))
			# CRED
			if request.POST.get('CRED') == '':
				errores['CRED'] = "Debe ingresar el credito"
			else:
				query_CBanck['CRED'] = float(request.POST.get('CRED'))
				credito = float(request.POST.get('CRED'))
			# BALANCE
			balance = (credito - debito)
			if debito > credito:
				errores['BALANCE'] = "Debito sobrepasa al credito!!"
			else:
				query_CBanck['BALANCE'] = float(balance)



			if not errores:
				try:
					Ccuenta = ACCOUNT_BANK(**query_CBanck)
					response = ''
					response = requests.post('https://radiant-journey-28507.herokuapp.com/api_banco.php', json = query_CBanck)

					if response.status_code == 200:
						Data = response.json()
						#print(Data)
					response2 = ''
					response2 = requests.post('http://167.99.158.191/api_cloud_computing/banco.php', json = query_CBanck)

					if response2.status_code == 200:
						Data2 = response.json()
						print(Data2)
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

# Modificar Account Bank
@login_required
def Modificar_CBanco(request,id_ACCOUNT_BANK):
	if request.user.is_superuser:

		errores = {}
		ABanck = ACCOUNT_BANK.objects.filter(ID=id_ACCOUNT_BANK)

		if request.method == 'POST':

			if request.POST.get('DATES') == '' or request.POST.get('DESCR') == '' or request.POST.get('ID_CLIENT') == '' or request.POST.get('TYPE') == '' or request.POST.get('TYPE') == '':
				errores['NAME'] = "HAY ERRORES"

			if not errores:
				try:
					cliente = ACCOUNT_BANK.objects.filter(ID=id_ACCOUNT_BANK).update(
																			DATES = request.POST.get('DATES'),
																			DESCR = request.POST.get('DESCR'),
																			ID_CLIENT = request.POST.get('ID_CLIENT'),
																			TYPE = request.POST.get('TYPE'),
																			DEBT = request.POST.get('DEBT'),
																			CRED = request.POST.get('CRED'),
																			BALANCE = request.POST.get('BALANCE'),
																			)
					jucb = {"ID": str(id_ACCOUNT_BANK),
     						"DATES": request.POST.get('DATES'),
      						"DESCR": request.POST.get('DESCR'),
      						"ID_CLIENT": request.POST.get('ID_CLIENT'),
     						"TYPE": request.POST.get('TYPE'),
     						"DEBT": request.POST.get('DEBT'),
      						"CRED": request.POST.get('CRED'),
      						"BALANCE": request.POST.get('BALANCE')}
					response = ''
					response = requests.put('https://radiant-journey-28507.herokuapp.com/api_banco.php', json = jucb)

					if response.status_code == 200:
						Data = response.json()
						#print(Data)
					response2 = ''
					response2 = requests.put('http://167.99.158.191/api_cloud_computing/banco.php', json = jucb)

					if response2.status_code == 200:
						Data2 = response.json()
						print(Data2)
				except Exception as e:
					transaction.rollback()
					errores['administrador'] = e
					ctx = {'ABanck':ABanck,'errores':errores}

					return render(request,'Modificar_CBanco.html',ctx)
				else:
					transaction.commit()


					return HttpResponseRedirect(reverse('app_CCDev:Vista_CBanco')+"?ok")
			else:
				ctx = {'ABanck':ABanck,'errores':errores}
				return render(request,'Modificar_CBanco.html',ctx)
		else:
			ctx = {'ABanck':ABanck}
			return render(request,'Modificar_CBanco.html',ctx)
	else:
		return redirect('app_CCDev:principal')

#Eliminar cuenta de Banco
@login_required
def Eliminar_ACCOUNT_BANK(request,id_ACCOUNT_BANK):
	ctx,ctx2={},{}
	eliminar = ACCOUNT_BANK.objects.filter(ID=id_ACCOUNT_BANK).delete()
	ctx = {"id":id_ACCOUNT_BANK}
	response = ''
	response = requests.delete('https://radiant-journey-28507.herokuapp.com/api_banco.php', json = ctx)

	if response.status_code == 200:
		Data = response.json()
		# print(Data)
	ctx2 = {"ID":id_ACCOUNT_BANK}
	response2 = ''
	response2 = requests.delete('http://167.99.158.191/api_cloud_computing/banco.php', json = ctx2)

	if response2.status_code == 200:
		Data2 = response.json()
		print(Data2)
	return HttpResponseRedirect(reverse('app_CCDev:Vista_CBanco'))

# Envio de Api
#Api Login Simple
class ApiLogin(APIView):

	def post (self, request, format=None):

		ctx = {}

		if request.method == 'POST':
			Data = json.loads(request.body)
			contrasenia = Data['pass']
			username = Data['user']
			user = authenticate(username=username,password=contrasenia)
			if user is not None:
				if user.is_active:
					auth_login(request,user)
					#print(json.dumps({"c": 0, "b": 0, "a": 0}, sort_keys=True))
					ctx = {'Data': 'True','Mensaje':'Acceso Consedido'}
					return Response(ctx)
				else:
					ctx = {'Data': 'False','Mensaje':'USUARIO INACTIVO'}
					return Response(ctx)
			else:
				ctx = {'Data': 'False','Mensaje':'USUARIO O CONTRASEÑA INCORRECTO'}
				return Response(ctx)

#Api cliente movil
#API Tipo_producto
class ApiTipo_producto(APIView):
	ctx = {}

	def get(self, request, format=None):
		print(request.body)
		if request.body:#Suponiendo que se enviara el id en el Json
			Data = json.loads(request.body)
			id_tp = Data['ID'] #Id del tipo de producto a filtrar
			if Tipo_producto.objects.filter(pk=id_tp).exists():
				T_producto = list(Tipo_producto.objects.filter(pk=id_tp).values('pk','descripcion_producto'))
			else:
				T_producto = list(Tipo_producto.objects.all().values('pk','descripcion_producto'))
				ctx = {'Id':'No Encontrado','T_producto':T_producto}
				return Response(ctx)
		else:
			T_producto = list(Tipo_producto.objects.all().values('pk','descripcion_producto'))



		if T_producto:
			ctx = {'T_producto':T_producto}
			return Response(ctx)
		else:
			ctx = {'error','No hay Registros'}
			return Response(ctx)
	def post(self, request, format=None):
		query_Tproducto,errores, ctx = {},{},{}
		if  request.method == 'POST':

			# print(request.body)
			Data = json.loads(request.body)
			D_producto = Data['descripcion_producto']


			if Tipo_producto.objects.filter(descripcion_producto = D_producto).exists():
				ctx = {'Sussces','existe ya este tipo de producto'}

			else:


				# descripcion_producto
				if type(D_producto) != str:
					errores['descripcion_producto'] = "La descripcion del producto no es un string"
				else:
					query_Tproducto['descripcion_producto'] = D_producto

				print(errores)

				if not errores:
					ctx = {'Sussces','Se almaceno con exito'}
					T_producto = Tipo_producto(**query_Tproducto)
					T_producto.save()
				else:
					ctx = {'error': errores}
			return Response(ctx)
	def put(self, request):
		if  request.method == 'PUT':
			Data = json.loads(request.body)
			id_tp = Data['ID'] #Id del tipo de producto a filtrar
			if Tipo_producto.objects.filter(pk=id_tp).exists():

				D_producto = Data['descripcion_producto']

				T_producto = Tipo_producto.objects.filter(pk=id_tp).update(
																					descripcion_producto = D_producto,

																					)
				ctx = {'Sussces','Datos modificados'}
				return Response(ctx)
			else:
				ctx = {'Error','ID no existente'}
				return Response(ctx)
	def delete(self, request):
		if request.method == 'DELETE':
			Data = json.loads(request.body)
			id_tp = Data['ID']
			if Tipo_producto.objects.filter(pk=id_tp).exists():
				eliminar = Tipo_producto.objects.filter(pk=id_tp).delete()
				ctx = {'Sussces','Registro Eliminado'}
				return Response(ctx)
			else:
				ctx = {'Error','ID no existente'}
				return Response(ctx)

class Apiproductos(APIView):
	ctx = {}
	def get(self, request, format=None):
		a = Producto.objects.get(pk=1)
		# print(type(a.img_producto))
		# res = (a.img_producto, 'utf-8')
		# #res = bytes(str(a.img_producto), 'utf-8')
		# print(res)

		print(type(a.img_producto))
		#print(a.img_producto)

		#Convirtiendo a Base64
		img_base64 = base64.b64encode(str(a.img_producto).encode('utf-8'))
		print(type(img_base64))
		lista_prod = []
		if request.body:#Suponiendo que se enviara el id en el Json
			Data = json.loads(request.body)
			id_p = Data['ID'] #Id del tipo de producto a filtrar
			if Producto.objects.filter(pk=id_p).exists():
				#productos = list(Producto.objects.filter(pk=id_p).values('pk','nombre_producto','descripcion','fecha_expira','precio','cantidad','tipo_producto','fecha_registro'))
				p = Producto.objects.get(pk=id_p)
				lista_prod = [{'pk':p.pk, 'nombre_producto':p.nombre_producto, 'descripcion':p.descripcion, 'fecha_expira':p.fecha_expira, 'precio':p.precio, 'cantidad':p.cantidad, 'tipo_producto':p.tipo_producto.id, 'fecha_registro':p.fecha_registro, 'imagen':base64.b64encode(str(p.img_producto).encode('utf-8'))}]
				ctx = {'Id':'Encontrado','productos':lista_prod}
				return Response(ctx)
			else:
				#productos = list(Producto.objects.all().values('pk','nombre_producto','descripcion','fecha_expira','precio','cantidad','tipo_producto','fecha_registro'))
				for p in Producto.objects.all():
					lista_prod.append({'pk':p.pk, 'nombre_producto':p.nombre_producto, 'descripcion':p.descripcion, 'fecha_expira':p.fecha_expira, 'precio':p.precio, 'cantidad':p.cantidad, 'tipo_producto':p.tipo_producto.id, 'fecha_registro':p.fecha_registro, 'imagen':base64.b64encode(str(p.img_producto).encode('utf-8'))})
				
				ctx = {'Id':'No Encontrado','productos':lista_prod}
				return Response(ctx)
		else:
			for p in Producto.objects.all():
				lista_prod.append({'pk':p.pk, 'nombre_producto':p.nombre_producto, 'descripcion':p.descripcion, 'fecha_expira':p.fecha_expira, 'precio':p.precio, 'cantidad':p.cantidad, 'tipo_producto':p.tipo_producto.id, 'fecha_registro':p.fecha_registro, 'imagen':base64.b64encode(str(p.img_producto).encode('utf-8'))})
			
			#productos = list(Producto.objects.all().values('pk','nombre_producto','descripcion','fecha_expira','precio','cantidad','tipo_producto','fecha_registro'))

		if lista_prod:
			ctx = {'Id':'Id no solicitado','productos':lista_prod}#'img_producto':res
			return Response(ctx)
		else:
			ctx = {'error','No hay Registros'}
			return Response(ctx)
#API CLIENTE
class ApiCliente(APIView):
    ctx={}
    def get(self, request, format=None):

        if request.body:
            Data = json.loads(request.body)
            id_c = Data['ID'] #Id del tipo de producto a filtrar
            if Cliente.objects.filter(pk=id_c).exists():
                clientes = list(Cliente.objects.all().values('pk','nombres','apellidos','avatar','usuario','correo','direccion','n_identidad','genero','fecha_registro','estado'))
                ctx = {'Id':'Encontrado','clientes':clientes}
                return Response(ctx)
            else:
                clientes = list(Cliente.objects.all().values('pk','nombres','apellidos','avatar','usuario','correo','direccion','n_identidad','genero','fecha_registro','estado'))
                ctx = {'Id':'No Encontrado','clientes':clientes}
                return Response(ctx)

        else:
            clientes = list(Cliente.objects.all().values('pk','nombres','apellidos','avatar','usuario','correo','direccion','n_identidad','genero','fecha_registro','estado'))

        if clientes:
            ctx = {'Id':'No Solicitado','clientes':clientes}
            return Response(ctx)
        else:
            ctx = {'error','No hay Registros'}
            return Response(ctx)
    def post(self, request, format=None):

        query_CLEINT,errores, ctx = {},{},{}
        rango = 0
        username = ''
        lista_correo = []
        if  request.method == 'POST':
            Data = json.loads(request.body)

            nombre = Data['nombres']
            apellido = Data['apellidos']
            avatar = Data['avatar']
            correo = Data['correo']
            direccion = Data['direccion']
            n_identidad = Data['n_identidad']
            genero = Data['genero']


            if User.objects.filter(email = correo).exists():
                ctx = {'error','existe ese correo'}
            else:
                lista_correo.append(correo)
                password = Data['password']
                rango = correo.find('@') #Devulve la posicion donde esta el @
                for x in range(0,rango):
                    username += correo[x]

				# NAME
                if type(nombre) != str:
                    errores['nombres'] = "El nombre no es un string"
                else:
                    query_CLEINT['nombres'] = nombre
                # Apellido
                if type(apellido) != str:
                    errores['apellidos'] = "El apellidos no es un string"
                else:
                    query_CLEINT['apellidos'] = apellido
				# avatar
                # if type(avatar) != bin:
                #     print(type(avatar))
                #     errores['avatar'] = "El avatar no es un binario"
                # else:
                #     query_CLEINT['avatar'] = avatar
				# Correo
                if type(correo) != str:
                    errores['correo'] = "El correo no es un String"
                else:
                    query_CLEINT['correo'] = correo
                    email = correo
				# direccion
                if type(direccion) != str:
                    errores['direccion'] = "La direccion no es un string"
                else:
                    query_CLEINT['direccion'] = direccion
                # n_identidad
                if type(n_identidad) != str:
                    errores['n_identidad'] = "El n_identidad no es un string"
                else:
                    query_CLEINT['n_identidad'] = n_identidad
                # genero
                if type(genero) != int and Genero.objects.get(pk=int(genero)).exists() :
                    errores['genero'] = "El genero no es un entero"
                else:
                    query_CLEINT['genero'] =  Genero.objects.get(pk=int(genero))
                print(errores)


                if not errores:
                    ctx = {'Sussces','Se almaceno con exito'}
                    # Creación de usuario
                    User.objects.create_user(username, email, password)
                    user = User.objects.last()
                    query_CLEINT['usuario'] = user
                    query_CLEINT['estado'] = True
                    cliente = Cliente(**query_CLEINT)
                    cliente.save()
                else:
                    ctx = {'error': errores}
                return Response(ctx)
            return Response(ctx)
    def put(self, request):
        if  request.method == 'PUT':
            Data = json.loads(request.body)
            idC = Data['ID']
            if Cliente.objects.filter(pk=idC).exists():
                nombre = Data['nombres']
                apellido = Data['apellidos']
                # avatar = Data['avatar']
                correo = Data['correo']
                direccion = Data['direccion']

                cliente = Cliente.objects.filter(pk=idC).update(
																					nombres = nombre,
																					apellidos = apellido,
																					# avatar = avatar,
																					correo = correo ,
                                                                                    direccion = direccion,

																					)
                ctx = {'Sussces','Datos modificados'}
                return Response(ctx)
            else:
                ctx = {'Error','ID no existente'}
                return Response(ctx)
    def delete(self, request):
        if request.method == 'DELETE':
            Data = json.loads(request.body)
            idC = Data['ID']
            if Cliente.objects.filter(pk=idC,estado = True).exists():
                cliente = Cliente.objects.filter(pk=idC).update(estado = False,	)
                id_usuario = Cliente.objects.get(pk=idC)

                user = User.objects.filter(pk=int(id_usuario.usuario.pk)).update(is_active = False,	)
                ctx = {'Sussces','Cliente inhabilitado '}
                return Response(ctx)
            else:
                ctx = {'Error','ID no existente o Usuario Inhabilitado'}
                return Response(ctx)
# API Carrito
class ApiCarrito_Cliente(APIView):
    ctx={}
    def get(self, request, format=None):

        if request.body:
            Data = json.loads(request.body)
            id_Carrito = Data['ID']
            usuario = str(Data['usuario'])
            id_usuario =User.objects.get(username=usuario)
            print(id_usuario)
            if Carrito.objects.filter(pk=id_Carrito,usuario=id_usuario.pk).exists():
                carritos = list(Carrito.objects.filter(usuario=id_usuario.pk).values('pk','producto','cantidad','usuario'))
            else:
                carritos = list(Carrito.objects.all().values('pk','producto','cantidad','usuario'))
                ctx = {'Id':'No Encontrado','carrito':carritos}
                return Response(ctx)
        else:
            carritos = list(Carrito.objects.all().values('pk','producto','cantidad','usuario'))


        if carritos:
            ctx = {'carrito':carritos}
            return Response(ctx)
        else:
            ctx = {'error','No hay Registros'}
            return Response(ctx)
    def post(self, request, format=None):
        query_carrito,errores, ctx = {},{},{}
        if  request.method == 'POST':
            Data = json.loads(request.body)
            cantidad = Data['cantidad']
            producto = Data['producto']
            usuario = Data['usuario']
            # Cantidad
            if type(cantidad) != float:
                errores['cantidad'] = "La catidad del producto no es un decimal"
            else:
                query_carrito['cantidad'] = cantidad
            	# Producto
            if type(producto) != int:
                errores['producto'] = "El producto  no es un entero"
            else:
                query_carrito['producto'] = producto
            print(errores)
            if not errores:
                ctx = {'Sussces','Se almaceno con exito'}
				# carito = Carrito(**query_carrito)
				# carito.save()
                return Response(ctx)
            else:
                ctx = {'error': errores}
                return Response(ctx)
	# def put(self, request):
	# 	if  request.method == 'PUT':
	# 		Data = json.loads(request.body)
	# 		id_tp = Data['ID'] #Id del tipo de producto a filtrar
	# 		if Tipo_producto.objects.filter(pk=id_tp).exists():
    #
	# 			D_producto = Data['descripcion_producto']
    #
	# 			T_producto = Tipo_producto.objects.filter(pk=id_tp).update(
	# 																				descripcion_producto = D_producto,
    #
	# 																				)
	# 			ctx = {'Sussces','Datos modificados'}
	# 			return Response(ctx)
	# 		else:
	# 			ctx = {'Error','ID no existente'}
	# 			return Response(ctx)
	# def delete(self, request):
	# 	if request.method == 'DELETE':
	# 		Data = json.loads(request.body)
	# 		id_tp = Data['ID']
	# 		if Tipo_producto.objects.filter(pk=id_tp).exists():
	# 			eliminar = Tipo_producto.objects.filter(pk=id_tp).delete()
	# 			ctx = {'Sussces','Registro Eliminado'}
	# 			return Response(ctx)
	# 		else:
	# 			ctx = {'Error','ID no existente'}
	# 			return Response(ctx)




######################################
#API CLIENTE CC
class ApisendCLIENT(APIView):
	ctx = {}
	@method_decorator(csrf_exempt)
	def dispatch(self, request, *args, **kwargs):
		return super().dispatch(request, *args, **kwargs)


	def get(self, request, format=None,id_CLIENT=""):
		clientes = list(CLIENT.objects.all().values('ID','NAME','ORIGIN','AGE','STATUS'))

		if clientes:
			ctx = {'clientes':clientes}
			return Response(ctx)
		else:
			ctx = {'error','No hay Registros'}
			return Response(ctx)
	def post(self, request, format=None):
		query_CLEINT,errores, ctx = {},{},{}
		if  request.method == 'POST':

			# print(request.body)
			Data = json.loads(request.body)


			id = Data['ID']
			nombre = Data['NAME']
			origen = Data['ORIGIN']
			edad = Data['AGE']
			estado = Data['STATUS']

			if CLIENT.objects.filter(ID = id).exists():
				ctx = {'Sussces','existe ese id'}

			else:

				# ID
				if type(id) != str:
					errores['id'] = "El ID no es un string"
				else:
					query_CLEINT['ID'] = id
				# NAME
				if type(nombre) != str:
					errores['NAME'] = "El nombre no es un string"
				else:
					query_CLEINT['NAME'] = nombre
				# ORIGIN
				if type(origen) != str:
					errores['ORIGIN'] = "El origen no es un string"
				else:
					query_CLEINT['ORIGIN'] = origen
				# AGE
				if type(edad) != int:
					errores['AGE'] = "La edad no es un entero"
				else:
					query_CLEINT['AGE'] = edad
				# STATUS
				if type(estado) != str:
					errores['STATUS'] = "El estado no es un string"
				else:
					query_CLEINT['STATUS'] = estado
				print(errores)

				if not errores:
					ctx = {'Sussces','Se almaceno con exito'}
					cliente = CLIENT(**query_CLEINT)
					cliente.save()
				else:
					ctx = {'error': errores}
			return Response(ctx)
	def put(self, request):
		if  request.method == 'PUT':
			Data = json.loads(request.body)
			idC = Data['ID']
			if CLIENT.objects.filter(ID=idC).exists():

				nombre = Data['NAME']
				origen = Data['ORIGIN']
				edad = Data['AGE']
				estado = Data['STATUS']

				cliente = CLIENT.objects.filter(ID=idC).update(
																					NAME = nombre,
																					ORIGIN = origen,
																					AGE = edad,
																					STATUS = estado ,
																					)
				ctx = {'Sussces','Datos modificados'}
				return Response(ctx)
			else:
				ctx = {'Error','ID no existente'}
				return Response(ctx)
	def delete(self, request):
		if request.method == 'DELETE':
			Data = json.loads(request.body)
			idC = Data['ID']
			if CLIENT.objects.filter(ID=idC).exists():
				eliminar = CLIENT.objects.filter(ID=idC).delete()
				ctx = {'Sussces','Registro Eliminado'}
				return Response(ctx)
			else:
				ctx = {'Error','ID no existente'}
				return Response(ctx)

def CAPIClient(request):
	query_CLEINT,errores = {},{}
	url = requests.get('https://radiant-journey-28507.herokuapp.com/buscarClientes.php')
	# url2 = requests.get('https://radiant-journey-28507.herokuapp.com/buscarClientes.php')

	if url.status_code == 200:
		Data = url.json()
		# Data2 = url2.json()

		ApiData = Data['clientes']
		# ApiData2 = Data2['clientes']
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
				# ID
				if type(id) != str:
					errores['id'] = "El ID no es un string"
				else:
					query_CLEINT['ID'] = id
				# NAME
				if type(nombre) != str:
					errores['NAME'] = "El nombre no es un string"
				else:
					query_CLEINT['NAME'] = nombre
				# ORIGIN
				if type(origen) != str:
					errores['ORIGIN'] = "El origen no es un string"
				else:
					query_CLEINT['ORIGIN'] = origen
				# AGE
				if type(edad) != int:
					errores['AGE'] = "La edad no es un entero"
				else:
					query_CLEINT['AGE'] = edad
				# STATUS
				if type(estado) != str:
					errores['STATUS'] = "El estado no es un string"
				else:
					query_CLEINT['STATUS'] = estado
				print(errores)

				if not errores:
					cliente = CLIENT(**query_CLEINT)
					cliente.save()


#API ACCOUNT_BANK
class ApisendACCOUNT_BANK(APIView):
	ctx = {}
	def get(self, request, format=None,id_CB=""):
		CBancos = list(ACCOUNT_BANK.objects.all().values('ID','DATES','DESCR','ID_CLIENT','TYPE','DEBT','CRED','BALANCE'))
		print(id_CB)
		if CBancos:
			ctx = {'CBancos':CBancos}
			return Response(ctx)
		else:
			ctx = {'error','No hay Registros'}
			return Response(ctx)
	def post(self, request, format=None):
		query_CBanck,errores, ctx = {},{},{}
		if  request.method == 'POST':

			Data = json.loads(request.body)
			id = Data['ID']
			datos = Data['DATES']
			descripcion = Data['DESCR']
			cliente = Data['ID_CLIENT']
			estado = Data['TYPE']
			debito = float(Data['DEBT'])
			credito = float(Data['CRED'])
			balance = float(Data['BALANCE'])
			if ACCOUNT_BANK.objects.filter(ID = id).exists():
				ctx = {'Sussces','existe ese id'}
			else:

				# ID
				if type(id) != str:
					errores['ID'] = "El ID no es un string"
				else:
					query_CBanck['ID'] = id
				# DATES
				if type(datos) != str:
					errores['DATES'] = "los Datos no es un string"
				else:
					query_CBanck['DATES'] = datos
				# DESCR
				if type(descripcion) != str:
					errores['DESCR'] = "La descripcion no es un string"
				else:
					query_CBanck['DESCR'] = descripcion
				# ID_CLIENT
				if type(cliente) != str:
					errores['ID_CLIENT'] = "El cliente no es un string"
				else:
					query_CBanck['ID_CLIENT'] = cliente
				# TYPE
				if type(estado) != str:
					errores['TYPE'] = "El tipo no es un string"
				else:
					query_CBanck['TYPE'] = estado
				# DEBT
				if type(debito) != float:
					errores['DEBT'] = "El debito no es un float"
				else:
					query_CBanck['DEBT'] = debito
				# CRED
				if type(credito) != float:
					errores['CRED'] = "El credito no es un float"
				else:
					query_CBanck['CRED'] = debito
				# BALANCE
				if type(balance) != float:
					errores['BALANCE'] = "El balance no es un float"
				else:
					query_CBanck['BALANCE'] = balance

				print(errores)
				if not errores:
					Ccuenta = ACCOUNT_BANK(**query_CBanck)
					Ccuenta.save()
					ctx = {'Sussces','Se almaceno con exito'}
				else:
					ctx = {'Error':errores}
			return Response(ctx)
	def put(self, request):
		if request.method == 'PUT':
			Data = json.loads(request.body)
			idAb = Data['ID']
			if ACCOUNT_BANK.objects.filter(ID = idAb).exists():
				Data = json.loads(request.body)


				datos = Data['DATES']
				descripcion = Data['DESCR']
				cliente = Data['ID_CLIENT']
				estado = Data['TYPE']
				debito = float(Data['DEBT'])
				credito = float(Data['CRED'])
				balance = float(Data['BALANCE'])

				cbanco = ACCOUNT_BANK.objects.filter(ID=idAb).update(
																			DATES = datos,
																			DESCR = descripcion,
																			ID_CLIENT = cliente,
																			TYPE = estado,
																			DEBT = debito,
																			CRED = credito,
																			BALANCE = balance,
																			)
				ctx = {'Sussces','Datos modificados'}
				return Response(ctx)
			else:
				ctx = {'Error','ID no existente'}
				return Response(ctx)
	def delete(self, request):
		if request.method == 'DELETE':
			Data = json.loads(request.body)
			idAb = Data['ID']
			if  ACCOUNT_BANK.objects.filter(ID = idAb).exists():
				eliminar = ACCOUNT_BANK.objects.filter(ID=idAb).delete()
				ctx = {'Sussces','Registro Eliminado'}
				return Response(ctx)
			else:
				ctx = {'Error','ID no existente'}
				return Response(ctx)

#API captura de datos de ACCOUNT BANK
def CAPIACCOUNT_BANK(request):
	query_CLEINT,errores = {},{}
	url = requests.get('https://radiant-journey-28507.herokuapp.com/buscarBancos.php')
	# url2 = requests.get('https://radiant-journey-28507.herokuapp.com/buscarBancos.php')

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
			print(type(float(balance)))

			if ACCOUNT_BANK.objects.filter(ID = id).exists():
				print('existe ese id')
			else:
				print('no existe, se almacenara')
				# ID
				if type(id) != str:
					errores['ID'] = "El ID no es un string"
				else:
					query_CLEINT['ID'] = id
				# DATES
				if type(datos) != str:
					errores['DATES'] = "los Datos no es un string"
				else:
					query_CLEINT['DATES'] = datos
				# DESCR
				if type(descripcion) != str:
					errores['DESCR'] = "La descripcion no es un string"
				else:
					query_CLEINT['DESCR'] = descripcion
				# ID_CLIENT
				if type(cliente) != str:
					errores['ID_CLIENT'] = "El cliente no es un string"
				else:
					query_CLEINT['ID_CLIENT'] = cliente
				# TYPE
				if type(estado) != str:
					errores['TYPE'] = "El tipo no es un string"
				else:
					query_CLEINT['TYPE'] = estado
				# DEBT
				if type(debito) != float:
					errores['DEBT'] = "El debito no es un float"
				else:
					query_CLEINT['DEBT'] = debito
				# CRED
				if type(credito) != float:
					errores['CRED'] = "El credito no es un float"
				else:
					query_CLEINT['CRED'] = debito
				# BALANCE
				if type(balance) != float:
					errores['BALANCE'] = "El balance no es un float"
				else:
					query_CLEINT['BALANCE'] = balance

				print(errores)
				if not errores:
					Ccuenta = ACCOUNT_BANK(**query_CBanck)
					Ccuenta.save()
