from django.urls import path

from . import views

app_name = 'app_CCDev'

urlpatterns = [
 path('', views.principal, name='principal'),
 path('vista/data', views.otra_view, name='otra_view'),	
 path('vista/ApiCliente', views.Apisend.as_view(), name='ApiSend'),	
# Formularios
 path('vista/Tipo/Cuenta', views.Vista_Tcuenta, name='Vista_Tcuenta'),	
]