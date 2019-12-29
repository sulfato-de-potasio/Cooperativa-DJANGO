from django import forms #importacion


class formularioLogin(forms.Form):
	username = forms.CharField()
	password = forms.CharField(widget = forms.PasswordInput())