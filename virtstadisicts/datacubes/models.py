# Create your models here.
from django.db import models
from django.utils import timezone
from django.conf import settings
from django.utils.timezone import now


class userprofile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    photo = models.ImageField(upload_to='photos/', blank=True, null=True)

    def __str__(self):
        return self.user.username

	
class agentsgroups(models.Model):
	idagentgroup = models.AutoField(primary_key=True)
	groupagentcode = models.CharField(max_length=3, blank=True)
	groupagentdesc = models.CharField(max_length=50, blank=True)
	
	def save_agentsgroups(self):
		self.save()
	
	def __str__(self):
		return self.groupagentcode	
	

class agents(models.Model):
	idagent = models.AutoField(primary_key=True)
	agentcode = models.CharField(max_length=4, null=False)
	agentname = models.CharField(max_length=100, null=False)
	user = models.ForeignKey('auth.User')	

	def save_agent(self):
		self.save()

	def __str__(self):
		return self.agentcode

class agentrights(models.Model):
	idagentrights = models.AutoField(primary_key=True)
	idagent = models.ForeignKey(agents)
	idagentgroup = models.ForeignKey(agentsgroups)
	
	def save_agentrights(self):
		self.save
	
	def __str__(self):
		return self.idagentrights()
	
	def __str__(self):
		return self.idagent()

class carrier(models.Model):
	idcarrier = models.AutoField(primary_key=True)
	codcarrier = models.CharField(max_length=3, null=False)
	carriername = models.CharField(max_length=50, null=False)
	
	def save_carrier(self):
		self.save()

	def __str__(self):
		return self.codcarrier

class ots_deliver(models.Model):
	iddeliver = models.AutoField(primary_key=True)
	sentdate = models.DateField(blank=True, auto_now_add=True)
	ot = models.CharField(max_length=7, null=False)
	clientname = models.CharField(max_length=50, null=False)
	otname  =  models.CharField(max_length=50, null=False)
	codproduct = models.CharField(max_length=25, null=False)
	clientcommand = models.CharField(max_length=30, null=False)
	deliverparcial = models.DecimalField(max_digits=10,decimal_places=2)
	totaldeliver = models.DecimalField(max_digits=10,decimal_places=2)
	nominalprovided = models.DecimalField(max_digits=10,decimal_places=2)
	user = models.ForeignKey('auth.User')
	totalstorage = models.IntegerField(default=0)
	delivereddate = models.DateTimeField(null=True,blank=True)
	idcarrier = models.ForeignKey('carrier',default=25)
	machine = models.CharField(max_length=25, null=True)
	location = models.CharField(max_length=30, null=True)
	agent = models.IntegerField(default=0)
	enddate = models.DateTimeField(null=True, blank=True)
	originaldate = models.DateTimeField(null=True, blank=True)
 	autline = models.BigIntegerField(default=0)
	clicod = models.CharField(max_length=5, null=True)

	def save_ots_deliver(self):
		self.save()

	def __str__(self):
		return self.ot

class ots_clients(models.Model):
	idclient = models.AutoField(primary_key=True)
	clientname = models.CharField(max_length=50, null=False)
	clicod = models.CharField(max_length=5, null=True)

	def save_ots_clients(self):
		self.save()

	def __str__(self):
		return self.clientname

class ots(models.Model):
	idot = models.AutoField(primary_key=True)
	ot = models.CharField(max_length=7, null=False)
	otname  =  models.CharField(max_length=50, null=False)

	def save_ots(self):
		self.save()

	def __str__(self):
		return self.otname
