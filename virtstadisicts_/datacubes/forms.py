from django import forms
from .models import userprofile, ots_deliver, carrier
from django.forms.models import inlineformset_factory
from django.forms import ModelChoiceField, ChoiceField
from django.contrib.auth.models import User
from django.forms import formset_factory
import datetime
from django.contrib.admin.widgets import AdminDateWidget
from django.forms.extras.widgets import SelectDateWidget

class FormsetForm(forms.Form):
    delete= forms.BooleanField(required=False, initial=False)
    # some other fields with data

class carrier_form(forms.Form):
	codcarrier = forms.CharField(max_length=3)
	carriername = forms.CharField(max_length=50)
		
	def clean_codcarrier(self):
		codcarrier = self.cleaned_data['codcarrier']
		if carrier.objects.filter(codcarrier=codcarrier):
			raise forms.ValidationError('Revise los datos')
		return codcarrier
		
	def clean_carriername(self):
		carriername = self.cleaned_data['carriername']
		if carrier.objects.filter(carriername=carriername):
			raise forms.ValidationError('Revise los datos')
		return carriername

class deliver_form(forms.Form):
	    ot = forms.CharField(max_length=7)
	    clientname = forms.CharField(max_length=50)
	    codproduct = forms.CharField(max_length=25)
	    clientcommand = forms.CharField(max_length=30)
	    totalstorage = forms.DecimalField(max_digits=10,decimal_places=2)
	    trans = forms.BooleanField(required=False, initial=False)
	    carriermassive = forms.IntegerField()
	    machine = forms.CharField(max_length=25)
	    location = forms.CharField(max_length=30)
	   	
	    def clean_ot(self):
		ot = self.cleaned_data['ot']
		if ots_deliver.objects.filter(ot=ot):
		    raise forms.ValidationError('Ya existe un email igual en la db.')
		return ot

	    def clean_clientname(self):
		clientname = self.cleaned_data['clientname']
		if ots_deliver.objects.filter(clientname=clientname):
		    raise forms.ValidationError('Ya existe un email igual en la db.')
		return clientname

	    def clean_codproduct(self):
		codproduct = self.cleaned_data['codproduct']
		if ots_deliver.objects.filter(codproduct=codproduct):
		    raise forms.ValidationError('Ya existe un email igual en la db.')
		return codproduct

	    def clean_clientcommand(self):
		clientcommand = self.cleaned_data['clientcommand']
		if ots_deliver.objects.filter(clientcommand=clientcommand):
		    raise forms.ValidationError('Ya existe un email igual en la db.')
		return clientcommand

	    def clean_totalstorage(self):
		totalstorage = self.cleaned_data['totalstorage']
		if ots_deliver.objects.filter(totalstorage=totalstorage):
		    raise forms.ValidationError('Indica una quantitat correcta')
		return totalstorage


class ots_deliver_form(forms.Form):
	    sentdate = forms.DateField(widget=SelectDateWidget)
	    ot = forms.CharField(max_length=7)
	    clientname = forms.CharField(max_length=50)
	    otname = forms.CharField(max_length=50)
	    codproduct = forms.CharField(max_length=25)
	    clientcommand = forms.CharField(max_length=30)
	    deliverparcial = forms.DecimalField(max_digits=10,decimal_places=2)
	    totaldeliver = forms.DecimalField(max_digits=10,decimal_places=2)
	    nominalprovided = forms.DecimalField(max_digits=10,decimal_places=2)
	    totalstorage = forms.DecimalField(max_digits=10,decimal_places=2)
	    delivereddate = forms.DateTimeField(widget=SelectDateWidget)
	    idcarrier = forms.IntegerField(required=False)
	    machine = forms.CharField(max_length=25)
	    location = forms.CharField(max_length=30)
	    agent = forms.CharField(max_length=50)
	    
	    def clean_sentdate(self):
		sentdate = self.cleaned_data['sentdate']
		if ots_deliver.objects.filter(sentdate=sentdate):
		    raise forms.ValidationError('Nombre de usuario ya registrado.')
		return sentdate

	    def clean_ot(self):
		ot = self.cleaned_data['ot']
		if ots_deliver.objects.filter(email=email):
		    raise forms.ValidationError('Ya existe un email igual en la db.')
		return ot

	    def clean_clientname(self):
		clientname = self.cleaned_data['clientname']
		if ots_deliver.objects.filter(clientname=clientname):
		    raise forms.ValidationError('Ya existe un email igual en la db.')
		return clientname

	    def clean_otname(self):
		otname = self.cleaned_data['otname']
		if ots_deliver.objects.filter(otname=otname):
		    raise forms.ValidationError('Ya existe un email igual en la db.')
		return otname

	    def clean_codproduct(self):
		codproduct = self.cleaned_data['codproduct']
		if ots_deliver.objects.filter(codproduct=codproduct):
		    raise forms.ValidationError('Ya existe un email igual en la db.')
		return codproduct

	    def clean_clientcommand(self):
		clientcommand = self.cleaned_data['clientcommand']
		if ots_deliver.objects.filter(clientcommand=clientcommand):
		    raise forms.ValidationError('Ya existe un email igual en la db.')
		return clientcommand

	    def clean_deliverparcial(self):
		deliverparcial = self.cleaned_data['deliverparcial']
		if ots_deliver.objects.filter(deliverparcial=deliverparcial):
		    raise forms.ValidationError('Ya existe un email igual en la db.')
		return deliverparcial

	    def clean_totaldeliver(self):
		totaldeliver = self.cleaned_data['totaldeliver']
		if ots_deliver.objects.filter(totaldeliver=totaldeliver):
		    raise forms.ValidationError('Ya existe un email igual en la db.')
		return totaldeliver

	    def clean_nominalprovided(self):
		nominalprovided = self.cleaned_data['nominalprovided']
		if ots_deliver.objects.filter(nominalprovided=nominalprovided):
		    raise forms.ValidationError('Ya existe un email igual en la db.')
		return nominalprovided

	    def clean_totalstorage(self):
		totalstorage = self.cleaned_data['totalstorage']
		if ots_deliver.objects.filter(totalstorage=totalstorage):
		    raise forms.ValidationError('Indica una quantitat correcta')
		return totalstorage
	    
	    def clean_delivereddate(self):
		delivereddate = self.cleaned_data['delivereddate']
		if ots_deliver.objects.filter(delivereddate=delivereddate):
		    raise forms.ValidationError('Error en el format de la data')
		return delivereddate

	    def clean_idcarrier(self):
		idcarrier = self.cleaned_data['idcarrier']
		if ots_deliver.objects.filter(idcarrier=idcarrier):
		    raise forms.ValidationError('Selecciona un transportista')
		return idcarrier

class registeruser_form(forms.Form):
	    username = forms.CharField(min_length=5)
	    email = forms.EmailField()
	    password = forms.CharField(widget=forms.PasswordInput())
	    password2 = forms.CharField(widget=forms.PasswordInput())
	    photo = forms.ImageField(required=False)

	    def clean_username(self):
		username = self.cleaned_data['username']
		if User.objects.filter(username=username):
		    raise forms.ValidationError('Nombre de usuario ya registrado.')
		return username

	    def clean_email(self):
		email = self.cleaned_data['email']
		if User.objects.filter(email=email):
		    raise forms.ValidationError('Ya existe un email igual en la db.')
		return email

	    def clean_password2(self):
		password = self.cleaned_data['password']
		password2 = self.cleaned_data['password2']
		if password != password2:
		    raise forms.ValidationError('Password not mismatch.')
		return password2

class usereditemail_form(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control'}))

    def __init__(self, *args, **kwargs):
        """Obtener request"""
        self.request = kwargs.pop('request')
        return super(usereditemail_form, self).__init__(*args, **kwargs)

    def clean_email(self):
        email = self.cleaned_data['email']
        # Comprobar si ha cambiado el email
        actual_email = self.request.user.email
        username = self.request.user.username
        if email != actual_email:
            # Si lo ha cambiado, comprobar que no exista en la db.
            # Exluye el usuario actual.
            existe = User.objects.filter(email=email).exclude(username=username)
            if existe:
                raise forms.ValidationError('E-mail exist on the system')
        return email

class usereditpassword_form(forms.Form):

    actual_password = forms.CharField(
        label='Old Password',
        min_length=5,
        widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    password = forms.CharField(
        label='Mew Password',
        min_length=5,
        widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    password2 = forms.CharField(
        label='Repeat New Password',
        min_length=5,
        widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    def clean_password2(self):
        """Comprueba que password y password2 sean iguales."""
        password = self.cleaned_data['password']
        password2 = self.cleaned_data['password2']
        if password != password2:
            raise forms.ValidationError('Password mismatch')
        return password2
