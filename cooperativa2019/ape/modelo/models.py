from django.db import models

# Create your models here.
class client(models.Model):

	listaGenero = (
		('femenino', 'Femenino'),
		('masculino', 'Masculino'),
	)

	listaCivil = (
		('soltero', 'Soltere'),
		('casado', 'Casade'),
		('divorciado', 'Divorciade'),
		('viudo', 'Viude'),
	)

	cliente_id = models.AutoField(primary_key = True)
	cedula = models.CharField(max_length = 10, unique = True, null = False)
	nombres = models.CharField(max_length = 50, null = False)
	apellidos = models.CharField(max_length = 50, null = False)		
	genero = models.CharField(max_length = 15, choices = listaGenero, default = 'femenino', null = False)
	fecha_nacimiento = models.DateField(auto_now = False, auto_now_add = False, null = False)
	estado_civil = models.CharField(max_length = 20, choices = listaCivil, default = 'soltero', null = False)	
	correo = models.EmailField(max_length = 50, null = False)
	telefono = models.CharField(max_length = 8)
	celular = models.CharField(max_length = 10)
	direccion = models.TextField(max_length = 150, default = 'sin direccion')

class cuenta(models.Model):
		listaTipo = (
			('corriente', 'Corriente'),
			('ahorros', 'Ahorros'),
		)

		cuenta_id = models.AutoField(primary_key = True)
		numero = models.CharField(max_length = 20, unique = True, null = False)
		estado = models.BooleanField(default = True)
		fecha_apertura = models.DateField(auto_now_add = True, null = False)
		tipo_cuenta = models.CharField(max_length = 30, choices = listaTipo, default = 'ahorros')
		saldo = models.DecimalField(max_digits = 10, decimal_places = 3, null = False)
		cliente = models.ForeignKey(
			'client',
			on_delete = models.CASCADE,
		)
		def str(self):
			string = str(self.saldo)+";"+str(self.cuenta_id)
			return string


class transaccion(models.Model):
	listaTipoT = (
		('deposito', 'Deposito'),
		('retiro', 'Retiro'),
		('transferencia', 'Transferencia'),
	)

	transaccion_id = models.AutoField(primary_key = True)
	fecha = models.DateTimeField(auto_now_add = True, null = False)
	tipo = models.CharField(max_length = 30, choices = listaTipoT, null = False)
	valor = models.DecimalField(max_digits = 10, decimal_places = 3, null = False)
	descripcion = models.TextField(null = False)
	responsable = models.CharField(max_length = 160, null = False)
	cuenta = models.ForeignKey(
		'cuenta',
		on_delete = models.CASCADE,
		)
