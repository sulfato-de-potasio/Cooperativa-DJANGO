from django.urls import path

from . import views

urlpatterns = [

    path('', views.entrar, name = 'autenticar'),
    path(r'logout', views.expirar, name = 'expirar_sesion'),
]