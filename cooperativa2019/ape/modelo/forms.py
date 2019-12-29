from django import forms #importacion
from ape.modelo.models import client, cuenta, transaccion

class formularioCliente(forms.ModelForm):
	
	class Meta:  #class meta permite migrar 
		model = client
		fields = ["cedula", "nombres", "apellidos", "fecha_nacimiento", "genero", "estado_civil",
				"telefono", "celular", "correo", "direccion"]

class formularioCuenta(forms.ModelForm):

	class Meta:
		model = cuenta
		fields = ["numero", "tipo_cuenta", "saldo"]

class formularioTransaccion(forms.ModelForm):

	class Meta:
		model = transaccion
		fields = ["valor", "descripcion"]
