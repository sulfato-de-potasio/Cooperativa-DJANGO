from django.contrib import admin

# Register your models here.
from .models import client
from .models import cuenta
from .models import transaccion 

class AdminCliente(admin.ModelAdmin):

	list_display = ["cedula", "apellidos", "nombres", "genero"] 
	list_editable = ["apellidos", "nombres"] 
	list_filter = ["genero", "estado_civil"]
	search_fields = ["cedula", "apellidos"]

	class Meta:
		model = client

admin.site.register(client, AdminCliente)

class AdminCuenta(admin.ModelAdmin):

	list_display = ["numero", "estado", "fecha_apertura", "tipo_cuenta", "saldo"]
	list_editable = ["estado"]
	list_filter = ["tipo_cuenta", "estado"]
	search_fields = ["numero"]

	class Meta:
		model = cuenta

admin.site.register(cuenta, AdminCuenta)

class AdminTransa(admin.ModelAdmin):

	list_display = ["fecha", "tipo", "valor", "responsable", "descripcion"]
	list_editable = ["tipo"]
	list_filter = ["tipo", "fecha"]
	search_fields = ["responsable", "valor"]

	class Meta:
		model = transaccion

admin.site.register(transaccion, AdminTransa)