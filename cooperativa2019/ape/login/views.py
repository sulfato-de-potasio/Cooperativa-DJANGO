from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render
from .forms import formularioLogin
from django.contrib import messages

# Create your views here.
def entrar(request):

	#las arrobas son anotaciones 

	if request.method == 'POST':
		formulario = formularioLogin(request.POST)
		if formulario.is_valid():
			usuario = request.POST['username']
			clave = request.POST['password']
			user = authenticate(username = usuario, password = clave)
			if user is not None:
				if user.is_active:
					login(request, user)
					return HttpResponseRedirect(reverse('cliente'))
				else: 
					print('usuario desactivado')
			else: 
				messages.add_message(request, messages.WARNING, "Clave y / o Usuario Invalidos")
	else: 
		formulario = formularioLogin()
	context = {

		'form' : formulario,		

	}

	return render (request, 'sesion/login.html', context)

@login_required
def expirar(request):

	logout(request)

	return HttpResponseRedirect(reverse('home-page'))