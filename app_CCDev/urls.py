from django.urls import path

from . import views

app_name = 'app_CCDev'

urlpatterns = [
 path('', views.principal, name='principal'),
 path('vista/data', views.otra_view, name='otra_view'),	
#  Envio de api 
 path('vista/ApiCliente', views.Apisend.as_view(), name='ApiSend'),	
 path('vista/UpdateApiCliente', views.UpdateCLIENT.as_view(), name='UpdateCLIENT'),	#update
 path('vista/ApisendCLIENT', views.ApisendCLIENT.as_view(), name='ApisendCLIENT'),	
 path('vista/ApisendACCOUNT_BANK', views.ApisendACCOUNT_BANK.as_view(), name='ApisendACCOUNT_BANK'),	
# Formularios 
#Cliente
 path('vista/Tipo/Cuenta', views.Vista_Tcuenta, name='Vista_Tcuenta'),	
 path('vista/Vista_Cliente', views.Vista_Cliente, name='Vista_Cliente'),
 path('modificar/CLIENT/<str:id_CLIENT>/', views.modificar_CLIENT, name="modificar_CLIENT"),
 path('Eliminar/CLIENT/<str:id_cliente>/', views.Eliminar_cliente, name="Eliminar_cliente"),
 #Cuenta Banco	
 path('vista/Vista_CBanco', views.Vista_CBanco, name='Vista_CBanco'),	
 path('modificar/ACCOUNT_BANK/<str:id_ACCOUNT_BANK>/', views.Modificar_CBanco, name="Modificar_CBanco"),
 path('Eliminar/ACCOUNT_BANK/<str:id_ACCOUNT_BANK>/', views.Eliminar_ACCOUNT_BANK, name="Eliminar_ACCOUNT_BANK"),
]