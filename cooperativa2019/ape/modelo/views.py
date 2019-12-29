from django.contrib.auth.decorators import login_required

from django.shortcuts import render, redirect

from .forms import formularioCliente, formularioCuenta, formularioTransaccion

from ape.modelo.models import client, cuenta, transaccion

from django.contrib import messages
# Create your views here.

@login_required
def principal(request):
	listado = client.objects.all().order_by('apellidos')

	context = {

		'lista': listado,

	}

	return render (request, 'principal_cliente.html', context)

@login_required
def crear(request):

	usuario = request.user #peticion es procesada por el framework, agrega el usuario

	formulario = formularioCliente(request.POST)

	formCuenta = formularioCuenta(request.POST)

	if usuario.groups.filter(name = 'Administrativo').exists():


			if request.method == 'POST':
				if formulario.is_valid() and formCuenta.is_valid():
					datos = formulario.cleaned_data #obteniendo todos los datos del formulario
					cliente = client()  #creando objeto de clase cliente
					cliente.cedula = datos.get('cedula')
					cliente.nombres = datos.get('nombres')
					cliente.apellidos = datos.get('apellidos')
					cliente.fecha_nacimiento = datos.get('fecha_nacimiento')
					cliente.genero = datos.get('genero')
					cliente.estado_civil = datos.get('estado_civil')
					cliente.correo = datos.get('correo')	
					cliente.telefono = datos.get('telefono')			
					cliente.celular = datos.get('celular')
					cliente.direccion = datos.get('direccion')
					cliente.save()

					datosCuenta = formCuenta.cleaned_data #obteniendo los datos del formulario cuenta
					cuent = cuenta() #creando objeto de clase cuenta
					cuent.numero = datosCuenta.get('numero')
					cuent.estado = True
					cuent.fecha_apertura = datosCuenta.get('fecha_apertura')
					cuent.tipo_cuenta = datosCuenta.get('tipo_cuenta')
					cuent.saldo = datosCuenta.get('saldo')
					cuent.cliente = cliente
					cuent.save()

					return redirect(principal)
	
	else: 
		messages.add_message(request, messages.ERROR, "NO tienes autorizacion para hacer eso")
		return redirect(principal)

	context = {

		'formulario': formulario,
		'formCuenta': formCuenta,
	}

	return render (request, 'cliente/crear_cliente.html', context)

@login_required
def modificar(request):

	usuario = request.user

	dni = request.GET['cedula']

	cliente = client.objects.get(cedula = dni)

	formulario = formularioCliente(instance = cliente)

	if usuario.groups.filter(name = 'Administrativo').exists():

		if request.method == 'POST':

			formulario = formularioCliente(request.POST, instance = cliente)

			if formulario.is_valid():

			#cliente = formulario.save(commit = FALSE)
				cliente.save()

				return redirect(principal)

	else: 
		messages.add_message(request, messages.ERROR, "NO tienes autorizacion para hacer eso")
		return redirect(principal)				

	context = {

		'objeto' : cliente,
		'form': formulario,

	}

	return render (request, 'cliente/modificar_cliente.html', context)

@login_required
def borrar(request):

	usuario = request.user

	if usuario.groups.filter(name = 'Administrativo').exists():

		dni = request.GET['cedula']

		cliente = client.objects.get(cedula = dni)
	
		cliente.delete()

		return redirect(principal)

	else: 
		messages.add_message(request, messages.ERROR, "NO tienes autorizacion para hacer eso")
		return redirect(principal)		

@login_required
def cuentas(request):

	dni = request.GET['cedula']

	cliento = client.objects.get(cedula = dni) 

	cuentas = cuenta.objects.filter(cliente_id = cliento.cliente_id)

	context = {

		'ctas': cuentas,
		'cte': cliento,

	}

	return render (request, 'cuenta/cuentas_cliente.html', context)

@login_required
def crear_cuentas(request, dni):	

	usuario = request.user

	clintu = client.objects.get(cedula=dni)
	
	formCuenta = formularioCuenta(request.POST)

	if usuario.groups.filter(name = 'Administrativo').exists():


			if request.method == 'POST':
				if formCuenta.is_valid():			

					datosCuenta = formCuenta.cleaned_data #obteniendo los datos del formulario cuenta
					cuent = cuenta() #creando objeto de clase cuenta
					cuent.numero = datosCuenta.get('numero')
					cuent.estado = True
					cuent.fecha_apertura = datosCuenta.get('fecha_apertura')
					cuent.tipo_cuenta = datosCuenta.get('tipo_cuenta')
					cuent.saldo = datosCuenta.get('saldo')
					cuent.cliente = clintu
					cuent.save()

					return redirect('/cliente/cuentas_cliente?cedula='+dni)
	
	else: 
		messages.add_message(request, messages.ERROR, "NO tienes autorizacion para hacer eso")
		return redirect('/cliente/cuentas_cliente?cedula='+dni)	


	context = {

		'form': formCuenta,

	}

	return render (request, 'cuenta/crear_cuenta.html', context)


@login_required
def depositar(request, numero):

	usuario = request.user

	cta = cuenta.objects.get(numero=numero)

	clien = client.objects.get(cliente_id = cta.cliente_id)

	cedu = clien.cedula

	formulario = formularioTransaccion(request.POST)

	if usuario.groups.filter(name = 'Cajera').exists():

		if request.method == 'POST':

			if formulario.is_valid():

				datos = formulario.cleaned_data
				cta.saldo = cta.saldo + datos.get('valor')
				cta.save()
				transa = transaccion()
				transa.tipo = 'deposito'
				transa.valor = datos.get('valor')
				transa.descripcion = datos.get('descripcion')
				transa.responsable = 'el que deposito'
				transa.cuenta = cta
				transa.save()
				#mensaje = 'Transa realizada con exito'
				#return render(request, 'transas/estatus.html', locals())
				messages.add_message(request, messages.SUCCESS, "Se ha hecho el deposito con exito")
				return redirect('/cliente/cuentas_cliente?cedula='+cedu)
	else: 
		messages.add_message(request, messages.ERROR, "NO tienes autorizacion para hacer eso")
		return redirect('/cliente/cuentas_cliente?cedula='+cedu)	


	context = {

		'ceta': cta,
		'cli': clien,
		'form': formulario,

	} 

	return render (request, 'transas/depositar.html', context)


@login_required
def retirar(request, numero):

	usuario = request.user

	cta = cuenta.objects.get(numero=numero)

	clien = client.objects.get(cliente_id = cta.cliente_id)

	cedu = clien.cedula

	formulario = formularioTransaccion(request.POST)

	if usuario.groups.filter(name = 'Cajera').exists():

		if request.method == 'POST':

			if formulario.is_valid():

				datos = formulario.cleaned_data
				cta.saldo = cta.saldo - datos.get('valor')
				cta.save()
				transa = transaccion()
				transa.tipo = 'retiro'
				transa.valor = datos.get('valor')
				transa.descripcion = datos.get('descripcion')
				transa.responsable = 'el que deposito'
				transa.cuenta = cta
				transa.save()
				messages.add_message(request, messages.SUCCESS, "Se ha retirado con exito")
				return redirect('/cliente/cuentas_cliente?cedula='+cedu)
	else: 
		messages.add_message(request, messages.ERROR, "NO tienes autorizacion para hacer eso")
		return redirect('/cliente/cuentas_cliente?cedula='+cedu)	

	context = {

		'ceta': cta,
		'cli': clien,
		'form': formulario,

	} 

	return render (request, 'transas/retiro.html', context)


@login_required
def transferir(request, numero):

	usuario = request.user

	cta = cuenta.objects.get(numero=numero)

	clien = client.objects.get(cliente_id = cta.cliente_id)

	formulario = formularioTransaccion(request.POST)

	if usuario.groups.filter(name = 'Cajera').exists():

		if request.method == 'POST':

			nctaT = request.POST.get('Ncuenta')

			ctaT = cuenta.objects.get(numero=nctaT)

			if formulario.is_valid():

				datos = formulario.cleaned_data
				if cuenta.objects.filter(numero=nctaT).exists():
					cta.saldo = cta.saldo - datos.get('valor')
					ctaT.saldo = ctaT.saldo + datos.get('valor')
					cta.save()
					ctaT.save()
					transa = transaccion()
					transa.tipo = 'transferencia'
					transa.valor = datos.get('valor')
					transa.descripcion = datos.get('descripcion')
					transa.responsable = 'el que deposito'
					transa.cuenta = cta
					transa.save()
					transax = transaccion()
					transax.tipo = 'transferencia'
					transax.valor = datos.get('valor')
					transax.descripcion = datos.get('descripcion')
					transax.responsable = 'el que deposito'
					transax.cuenta = ctaT
					transax.save()
					messages.add_message(request, messages.SUCCESS, "Se ha hecho la transferencia con exito")
					return redirect('/cliente/cuentas_cliente?cedula='+clien.cedula)	
				else: 
					messages.add_message(request, messages.SUCCESS, "Algo ha salido mal")
					return redirect('/cliente/cuentas_cliente?cedula='+clien.cedula)

	else: 
		messages.add_message(request, messages.ERROR, "NO tienes autorizacion para hacer eso")
		return redirect('/cliente/cuentas_cliente?cedula='+clien.cedula)	

	context = {

		'ceta': cta,
		'cli': clien,
		'form': formulario,

	} 

	return render (request, 'transas/transferencia.html', context)

@login_required
def borrar_cuenta(request, numero):

	usuario = request.user

	cuent = cuenta.objects.get(numero = numero)

	clien = client.objects.get(cliente_id = cuent.cliente_id)

	if usuario.groups.filter(name = 'Administrativo').exists():
	
		cuent.delete()

		return redirect('/cliente/cuentas_cliente?cedula='+clien.cedula)

	else: 
		messages.add_message(request, messages.ERROR, "NO tienes autorizacion para hacer eso")
		return redirect('/cliente/cuentas_cliente?cedula='+clien.cedula)