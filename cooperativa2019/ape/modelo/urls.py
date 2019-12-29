from django.urls import path

from . import views

urlpatterns = [

    path('', views.principal, name='cliente'),
    path('crear_cliente/', views.crear),
    path('modificar_cliente/', views.modificar),
    path('borrar_cliente/', views.borrar),
    path('cuentas_cliente/', views.cuentas),
    path(r'crear_cuenta/(?P<dni>d+)/$', views.crear_cuentas, name='crear_cuentas'),
    path(r'deposito/(?P<numero>d+)/$', views.depositar, name='deposito'),
    path(r'retiro/(?P<numero>d+)/$', views.retirar, name='retiro'),
    path(r'transferencia/(?P<numero>d+)/$', views.transferir, name='transferencia'),
    path(r'borrar_cuenta/(?P<numero>d+)/$', views.borrar_cuenta, name='borrar_cuenta'),
]