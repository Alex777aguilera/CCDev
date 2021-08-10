from django.urls import path

from . import views

app_name = 'app_CCDev'

urlpatterns = [
 path('', views.principal, name='principal'),
 path('vista/data', views.otra_view, name='otra_view'),	
#  Envio de api
 path('vista/ApiCliente', views.Apisend.as_view(), name='ApiSend'),	
 path('vista/ApisendCLIENT', views.ApisendCLIENT.as_view(), name='ApisendCLIENT'),	
 path('vista/ApisendACCOUNT_BANK', views.ApisendACCOUNT_BANK.as_view(), name='ApisendACCOUNT_BANK'),	
# Formularios
 path('vista/Tipo/Cuenta', views.Vista_Tcuenta, name='Vista_Tcuenta'),	
 path('vista/Vista_Cliente', views.Vista_Cliente, name='Vista_Cliente'),	
 path('vista/Vista_CBanco', views.Vista_CBanco, name='Vista_CBanco'),	
]