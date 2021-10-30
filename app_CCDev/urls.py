from django.urls import path

from . import views

app_name = 'app_CCDev'

urlpatterns = [
 path('login',views.login,name="login"),
 path('', views.principal, name='principal'),
 path('cerrar_sesion',views.cerrar_sesion,name="cerrar_sesion"),
 path('vista/data', views.otra_view, name='otra_view'),	
#  Envio de api 
#Api cliente
 path('vista/ApiCliente', views.Apisend.as_view(), name='ApiSend'),	
 ##	
 path('vista/ApisendCLIENT', views.ApisendCLIENT.as_view(), name='ApisendCLIENT'),	
 path('vista/ApisendCLIENT/<str:id_CLIENT>/', views.ApisendCLIENT.as_view(), name='Process'),	
 #Api Cuenta de banco
 path('vista/ApisendACCOUNT_BANK', views.ApisendACCOUNT_BANK.as_view(), name='ApisendACCOUNT_BANK'),	
 path('vista/ApisendACCOUNT_BANK/<str:id_CB>/', views.ApisendACCOUNT_BANK.as_view(), name='ProcesBanck'),	
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

 #ApiMovil / login
 path('Api/Login', views.ApiLogin.as_view(), name='ApiLogin'),	
 path('Api/Cliente', views.ApiCliente.as_view(), name='ApiCliente'),	
 path('Api/Tipo/producto', views.ApiTipo_producto.as_view(), name='ApiTipo_producto'),
 
]