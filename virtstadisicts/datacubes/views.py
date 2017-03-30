# Create your views here.
# -*- coding: utf-8 -*-
from django.conf import settings
from django.views.generic import CreateView, ListView, DetailView, UpdateView
from django.shortcuts import render
from .models import ots_deliver, userprofile, ots, ots_clients, carrier, agents, agentsgroups, agentrights
from django.db.models import Count
from django.shortcuts import render,get_object_or_404
from .forms import registeruser_form, usereditemail_form, usereditpassword_form, ots_deliver_form, carrier_form, deliver_form, agentrights_form
from django.shortcuts import redirect
from django.template.context_processors import csrf
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.db import connection
from django.db.models.query import QuerySet
from django.db.models import Count
from django.forms import formset_factory
from django.template import RequestContext
from django.template.loader import get_template
from django.http import HttpResponse, QueryDict
from django.forms.models import model_to_dict
from django.utils.encoding import force_text
from django.utils.encoding import smart_unicode
from django import template
from django.utils.encoding import smart_str
import string
import MySQLdb
import locale
from io import BytesIO
from django.conf import settings
from reportlab.pdfgen import canvas
from reportlab.lib.enums import TA_RIGHT, TA_JUSTIFY
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Paragraph, TableStyle, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, landscape
from reportlab.platypus import Table
from reportlab.lib.units import inch
import datetime, timezones, time
from django.utils import timezone
from django.utils.dateformat import DateFormat
from django.utils.formats import get_format
import StringIO
import xlsxwriter
from dateutil.parser import parse
from django.utils.dateparse import parse_date


def WriteToExcel(weather_data):
    #print "NEW XLS FILE"
    output = StringIO.StringIO()
    workbook = xlsxwriter.Workbook(output, {'remove_timezone': True})
    bold = workbook.add_format({'bold': True})
    money = workbook.add_format({'num_format': '$#,##0'})
    date_format = workbook.add_format({'num_format': 'dd/mm/yyyy',
	    'bold': False,
	    'font_size': 9,
	    'align': 'center',
	    'valign': 'vcenter'
    })
    date_time_format = workbook.add_format({'num_format': 'dd/mm/yyyy hh:mm:ss',
	    'bold': False,
	    'font_size': 9,
	    'align': 'center',
	    'valign': 'vcenter'
    })
    # Here we will adding the code to add data
    worksheet_s = workbook.add_worksheet("Summary")
    title = workbook.add_format({
	    'bold': True,
	    'font_size': 14,
	    'align': 'center',
	    'valign': 'vcenter'
    })
    header = workbook.add_format({
	    'bold': True,
	    'bg_color': '#F7F7F7',
	    'font_size': 9,
	    'color': 'black',
	    'align': 'center',
	    'valign': 'top',
	    'border': 1
    }) 
    field = workbook.add_format({
	    'bold': False,
	    'font_size': 9,
	    'align': 'center',
	    'valign': 'vcenter'
    })
    title_text = "Llistat de comandes entregades"
    worksheet_s.merge_range('B2:H2', title_text, title)
    worksheet_s.write(4, 0, u"Dt.Enviada", header)
    worksheet_s.write(4, 1, u"OT", header)
    worksheet_s.write(4, 2, u"Client", header)
    worksheet_s.write(4, 3, u"Desc_OT", header)
    worksheet_s.write(4, 4, u"Producte", header)
    worksheet_s.write(4, 5, u"Cod.Comanda", header)
    worksheet_s.write(4, 6, u"Dt.Fi", header)
    worksheet_s.write(4, 7, u"Entrega Parcial", header)
    worksheet_s.write(4, 8, u"Entrega Total", header)
    worksheet_s.write(4, 9, u"Nominal", header)
    worksheet_s.write(4, 10, u"Total Magatzem", header)
    worksheet_s.write(4, 11, u"Dt.Expedició", header)
    worksheet_s.write(4, 12, u"Transportista", header)
    worksheet_s.write(4, 13, u"Màquina", header)
    worksheet_s.write(4, 14, u"Agent", header)
    worksheet_s.write(4, 15, u"Localitazació", header)
    for idx, data in enumerate(weather_data):
	    row = 5 + idx
	 
	    if data.sentdate is not None:
	       tmp = data.sentdate
	       nativedt = tmp.strftime('%d/%m/%Y')
	       worksheet_s.write_string(row, 0, nativedt, field)
	    else:
               nativedt = ''
	       worksheet_s.write_string(row, 0, nativedt, field)
	    worksheet_s.write_string(row, 1, data.ot, field)
	    worksheet_s.write_string(row, 2, data.clientname, field)
	    worksheet_s.write_string(row, 3, data.otname, field)
	    worksheet_s.write_string(row, 4, data.codproduct, field)
	    worksheet_s.write_string(row, 5, data.clientcommand, field)
	    try:
	    	nt2 = data.enddate.strftime('%d/%m/%Y')
	    	if data.enddate is not None:
	       		nativedt2 = data.enddate.replace(tzinfo=None)
	       		worksheet_s.write_string(row, 6, nt2, field)
	    	else:
	      		nativedt2 = ''
	       		worksheet_s.write_string(row, 6, nativedt2, field)
	    except:
	        nativedt2 = ''
	       	worksheet_s.write_string(row, 6, nativedt2, field)
	    worksheet_s.write_number(row, 7, data.totaldeliver, field)
	    worksheet_s.write_number(row, 8, data.deliverparcial, field)
	    worksheet_s.write_number(row, 9, data.nominalprovided, field)
	    worksheet_s.write_number(row, 10, data.totalstorage, field)
	    try:
	    	nt2 = data.delivereddate.strftime('%d/%m/%Y')
	    	if data.delivereddate is not None:
	       		nativedt2 = data.delivereddate.replace(tzinfo=None)
	       		worksheet_s.write_datetime(row, 11, nativedt2, date_time_format)
	    	else:
	      		nativedt2 = ''
	       		worksheet_s.write_string(row, 11, nativedt2, field)
	    except:
	        nativedt2 = ''
	       	worksheet_s.write_string(row, 11, nativedt2, field)
	    worksheet_s.write_string(row, 12, data.idcarrier.carriername, field)
	    worksheet_s.write_string(row, 13, data.machine, field)
	    worksheet_s.write_number(row, 14, data.agent, field)
	    worksheet_s.write_string(row, 15, data.location, field)
    workbook.close()
    xlsx_data = output.getvalue()
    # xlsx_data contains the Excel file
    return xlsx_data

# Create your views here.
@login_required(login_url='/login/')
def index(request):
    return render(request, 'datacubes/index.html', {})

@login_required(login_url='/login/')
def agentrights_vw(request):
    ar = agentrights.objects.select_related('idagent').select_related('idagentgroup').order_by('idagent')
    return render(request, 'datacubes/agentrights_list.html', {'ar': ar})

@login_required(login_url='/login/')
def agentrights_detail_vw(request, pk):
    ar = agentrights.objects.get(pk=pk)
    ar2 = agentrights.objects.select_related('idagent').select_related('idagentgroup').filter(idagent =  ar.idagent)
    argrps = agentsgroups.objects.all()
    arid = ar.idagent

    if request.method == "POST":
	if request.POST['action'] == "add":
	   print "Click option add"
    	   formset = agentrights_form(request.POST)
	   newgrp = request.POST['newgrp']
	   tmpagent = agents.objects.get(agentcode=arid)
	   tmpnewgrp = agentsgroups.objects.get(idagentgroup=newgrp)
	   print arid
	   print tmpagent.idagent
	   print request.POST['newgrp']
	   exist = agentrights.objects.filter(idagent=tmpagent.idagent,idagentgroup=tmpnewgrp.idagentgroup)
	   if not exist:
	   	newaggrp = agentrights.objects.create(idagent=tmpagent, idagentgroup=tmpnewgrp)
	elif request.POST['action'] == "del":
	   print "Click option del"
    	   formset = agentrights_form(request.POST)
	   delgrp = request.POST.getlist('delgrp')
	   arid = agentrights.objects.values_list('idagent_id').filter(pk=pk)
	   qy = agentrights.objects.filter(idagent_id=arid).count()
	   print qy
	   if qy > 1:
		   for ix in range(0,len(delgrp)):
		    try: 
			tmpdelrecord = str(delgrp[ix]).replace(".","")
			print tmpdelrecord
			if tmpdelrecord:
				agentrights.objects.filter(idagentrights=tmpdelrecord).delete()
		    except Exception as e:
			print e
	   else:
		print "Imposible to delete record. Its recordcount equal 1"
	elif request.POST['action'] == "reset":
		formset = agentrights_form()
		print arid
		print request.POST['newgrp']
    else:
	formset = agentrights_form()

    context = {
		'formset': formset,
        	'ar2': ar2,
	        'argrps': argrps,
		'arid': arid,
    	      }

    return render(request, 'datacubes/agentrights_detail.html', context)

@login_required(login_url='/login/')
def carrier_vw(request):
    carriers = carrier.objects.order_by('idcarrier')
    return render(request, 'datacubes/carrier_list.html', {'carriers': carriers})

@login_required(login_url='/login/')
def carrier_detail_vw(request, pk):
    carriers = get_object_or_404(carrier, pk=pk)
    return render(request, 'datacubes/carrier_detail.html', {'carriers': carriers})

@login_required(login_url='/login/')
def carrier_detail_vw_(request, pk):
    carriers = get_object_or_404(carrier, pk=pk)
    if request.method == "POST":
    	form = carrier_form(request.POST)
        if form.is_valid():
        	car = form.save(commit=False)
             	car.save()
      		return redirect('datacubes.views.carrier_list', pk=carriers.pk)
    else:
    	form = carrier_form()

    context = {
    		'form': form,
        	'carriers': carriers,
    	      }
    return render(request, 'datacubes/carrier_edit.html', context)

@login_required(login_url='/login/')
def deliver_vw(request):
    clidataini = ots_clients.objects.values('clientname').order_by('clientname').distinct()
    otdataini = ots.objects.values('ot').order_by('ot').distinct()
    dtini  = datetime.datetime.now()
    dtfi = datetime.datetime.now()
    dtentrega = datetime.datetime.now()
    detail = ots_deliver.objects.order_by('sentdate').all().filter(iddeliver=-1)
    extra = 0
    actualcli = ""
    actualot = ""
    rows = []
    action = ""
    car = carrier.objects.values('idcarrier', 'codcarrier','carriername')
    detailct = 0
    user = request.user
    print user
# Wokflow actions
    if request.method == 'POST':
	if request.POST['action'] == "apply":
#            formset = DeliverFormset(request.POST, request.FILES)
	    #print "Method POST and action eq apply"
	    assignaciomasiva = "Single Assigned"
	    assignaciomasivadt = "Single Assigned"
	    actualcli = request.POST['cliini']
	    actualot = request.POST['otini']
	    dtini_ = request.POST['dtini']
	    dtfi_ = request.POST['dtfi']
	    if "trans" in request.POST:
	    	assignaciomasiva = request.POST['carriermassive']
	    if "dtent" in request.POST:
	    	assignaciomasivadt = request.POST['dtentrega']
	    extra = 1
	    dfini = datetime.datetime.strptime(dtini_, "%d/%m/%Y").date() 
	    dffi = datetime.datetime.strptime(dtfi_, "%d/%m/%Y").date() 
	    dtini = dfini
	    dtfi = dffi
    	    v_clicod = ots_clients.objects.values('clicod').filter(clientname = actualcli)
	    if actualcli == "Tots" and actualot == "Totes":
    	      detail = ots_deliver.objects.select_related('idcarrier').order_by('sentdate','clientname','ot').all().filter(sentdate__range=[str(dfini), str(dffi)])
	    elif actualcli == "Tots" and actualot <> "Totes":
	      detail = ots_deliver.objects.select_related('idcarrier').order_by('sentdate','ot','clientname').all().filter(ot = actualot)
	    elif actualcli <> "Tots" and actualot == "Totes":
    	      detail = ots_deliver.objects.select_related('idcarrier').order_by('sentdate','ot','clientname').all().filter(sentdate__range=[str(dfini), str(dffi)], clicod = v_clicod)
	    elif actualcli <> "Tots" and actualot <> "Totes":
    	      detail = ots_deliver.objects.select_related('idcarrier').order_by('sentdate','ot','clientname').all().filter(sentdate__range=[str(dfini), str(dffi)], clicod = v_clicod, ot = actualot)
	    else:
	      detail = ots_deliver.objects.select_related('idcarrier').order_by('sentdate','ot','clientname').all().filter(sentdate__range=[str(dfini), str(dffi)])
    	    detailct = ots_deliver.objects.count() 
	    for ix in detail:
		    rows.append(ix)
		    #print "======================================================================================="	    
		    #print "===					DICT VALUES				       ==="
		    #print "===				Value ID --->   ", ix.iddeliver,"		       ==="
		    #print "===				Value OT --->   ", ix.ot,"			       ==="
		    #print "===				Value CLIENT NAME --->   ", ix.clientname,"	       ==="
		    #print "===				Value COD PRODUCT --->   ", ix.codproduct,"	       ==="
		    #print "===				Value COMMAND CLI --->  ", ix.clientcommand,"	       ==="
		    #print "===				Value DELIVERED DATE ---> ",ix.delivereddate,"         ==="
		    #print "===				Value STORAGE --->   ", ix.totalstorage,"	       ==="
		    #print "===				Value CARRIER --->   ", ix.idcarrier.idcarrier,"       ==="
		    #print "===				Value CARRIER 2 --->   ", ix.idcarrier,"               ==="
		    #print "===									               ==="
		    #print "===				Value MASIVE ASSIGN --->   ", assignaciomasiva,"       ==="
		    #print "===				Value MASIVE ASSIGN DT --->   ", assignaciomasivadt,"  ==="
		    #print "======================================================================================="	    
    	    formset = deliver_form()
            context = {
           'formset': formset,
           'action': action,
	   'rows': rows,
           'extra': 1,
           'carrier': car,
           'cliini': clidataini,
           'otini': otdataini,
           'dtini': dtini,
           'dtfi': dtfi,
           'dtentrega': dtentrega,
           'actualot': actualot,
           'actualcli': actualcli,
           }
	elif request.POST['action'] == "save":
		formset = deliver_form(request.POST)
		idtmp = request.POST.getlist('iddeliver')
		ottmp = request.POST.getlist('ot')
		prodtmp = request.POST.getlist('codproduct')
		comtmp = request.POST.getlist('clientcommand')
		storagetmp = request.POST.getlist('totalstorage')
		carriertmp = request.POST.getlist('idcarrier')
		dtdeltmp = request.POST.getlist('delivereddate')
	    	assignaciomasiva = 0
		#print "Length list ot %d " % len(ottmp)
	    	if "trans" in request.POST:
	    		assignaciomasiva = 1
	    	assignaciomasivadt = 0
	    	if "dtent" in request.POST:
	    		assignaciomasivadt = 1
			
		for ix in range(0,len(ottmp)):
			up_id = idtmp[ix]
			tmptime = time.strftime("%H:%M:%S")
			if assignaciomasivadt == 0:
			 if dtdeltmp[ix] == '                   ':
				up_deldt = '0'
			 else :
				try:
	    				datedelivered = parse(dtdeltmp[ix])
					up_deldt = datedelivered.strftime("%Y-%m-%d")
				except:
					up_deldt = '0'
	
			elif assignaciomasivadt == 1:
				dtent = parse(request.POST['dtentrega'])
				up_deldt = dtent.strftime("%Y-%m-%d %H:%M:%S")

			if assignaciomasiva == 0:
				up_car = carriertmp[ix]
			elif assignaciomasiva == 1:
				up_car = request.POST['carriermassive']	
			if up_deldt != '0':
				combined = up_deldt + ' ' + tmptime
				print combined
				oldot = ots_deliver.objects.get(pk=up_id)
				olddelivered = oldot.delivereddate
				print "Value for actual date %s" % olddelivered
				if olddelivered == None:
					ots_deliver.objects.filter(pk=up_id).update(idcarrier = up_car, delivereddate = combined)
			else:
				ots_deliver.objects.filter(pk=up_id).update(idcarrier = up_car)

    	        formset = deliver_form()
	        clidataini = ots_clients.objects.values('clientname').order_by('clientname').distinct()
	    	otdataini = ots.objects.values('ot').order_by('ot').distinct()
	    	dtini  = datetime.datetime.now()
	    	dtfi = datetime.datetime.now()
	    	detail = ots_deliver.objects.order_by('sentdate').all().filter(iddeliver=-1)
	    	extra = 0
	    	actualcli = ""
	    	actualot = ""
	    	rows = []
	    	action = ""
	    	car = carrier.objects.values('idcarrier', 'codcarrier','carriername')
	    	detailct = 0   
            	context = {
           		   'formset': formset,
			   'rows':rows,
			   'action': action,
			   'extra': 1,
			   'carrier': car,
			   'cliini': clidataini,
			   'otini': otdataini,
			   'dtini': dtini,
			   'dtfi': dtfi,
			   'dtentrega': dtentrega,
			   'actualot': actualot,
			   'actualcli': actualcli,
			   }

	elif request.POST['action'] == "reset":
    	    formset = deliver_form()
	    clidataini = ots_clients.objects.values('clientname').order_by('clientname').distinct()
	    otdataini = ots.objects.values('ot').order_by('ot').distinct()
	    dtini  = datetime.datetime.now()
	    dtfi = datetime.datetime.now()
	    detail = ots_deliver.objects.order_by('sentdate').all().filter(iddeliver=-1)
	    extra = 0
	    actualcli = ""
	    actualot = ""
	    rows = []
	    action = ""
	    car = carrier.objects.values('idcarrier', 'codcarrier','carriername')
	    detailct = 0   
            context = {
           'formset': formset,
	   'rows':rows,
           'action': action,
           'extra': 1,
           'carrier': car,
           'cliini': clidataini,
           'otini': otdataini,
           'dtini': dtini,
           'dtfi': dtfi,
           'dtentrega': dtentrega,
           'actualot': actualot,
           'actualcli': actualcli,
           }
	else:
    	    formset = deilver_form()
            context = {
           'formset': formset,
	   'rows':rows,
           'action': action,
           'extra': 1,
           'carrier': car,
           'cliini': clidataini,
           'otini': otdataini,
           'dtini': dtini,
           'dtfi': dtfi,
           'dtentrega': dtentrega,
           'actualot': actualot,
           'actualcli': actualcli,
           }
    else:    
    	    formset = deliver_form()
            context = {
           'formset': formset,
	   'rows':rows,
           'action': action,
           'extra': 1,
           'carrier': car,
           'cliini': clidataini,
           'otini': otdataini,
           'dtini': dtini,
           'dtfi': dtfi,
           'dtentrega': dtentrega,
           'actualot': actualot,
           'actualcli': actualcli,
           }

    return render(request, 'datacubes/deliver2.html', context)

@login_required(login_url='/login/')
def deliver2_vw(request):
#    clidataini = ots_clients.objects.order_by('clientname').all()
#    otdataini = ots.objects.order_by('ot').all()
    clidataini = ots_clients.objects.values('clientname').order_by('clientname').distinct()
    otdataini = ots.objects.values('ot').order_by('ot').distinct()
    dtini  = datetime.datetime.now()
    dtfi = datetime.datetime.now()
    detail = ots_deliver.objects.order_by('sentdate').all().filter(iddeliver=-1)
    extra = 0
    actualcli = ""
    actualot = ""
    if request.method == 'POST':
	if request.POST['action'] == "apply":
            form = ots_deliver_form(request.POST, request.FILES)
	    actualcli = request.POST['cliini']
	    actualot = request.POST['otini']
	    dtini_ = request.POST['dtini']
	    dtfi_ = request.POST['dtfi']
	    #print dtini_
	    #print dtfi_
	    extra = 1
	    dfini = datetime.datetime.strptime(dtini_, "%d/%m/%Y").date() 
	    dffi = datetime.datetime.strptime(dtfi_, "%d/%m/%Y").date() 
	    dtini = dfini
	    dtfi = dffi
	    #print dfini
	    #print dffi
	    if actualcli == "Tots" and actualot <> "Totes":
    	      detail = ots_deliver.objects.order_by('sentdate','ot','clientname').all().filter(sentdate__range=[str(dfini), str(dffi)], ot = actualot)
	    elif actualcli <> "Tots" and actualot == "Totes":
    	      detail = ots_deliver.objects.order_by('sentdate','ot','clientname').all().filter(sentdate__range=[str(dfini), str(dffi)], clientname = actualcli)
	    elif actualcli <> "Tots" and actualot <> "Totes":
    	      detail = ots_deliver.objects.order_by('sentdate','ot','clientname').all().filter(sentdate__range=[str(dfini), str(dffi)], clientname = actualcli, ot = actualot)
	    else:
    	      detail = ots_deliver.objects.order_by('sentdate','ot','clientname').all().filter(sentdate__range=[str(dfini), str(dffi)])
        elif request.POST['action'] == 'export': 
            form = ots_deliver_form(request.POST, request.FILES)
	    actualcli = request.POST['cliini']
	    actualot = request.POST['otini']
	    dtini_ = request.POST['dtini']
	    dtfi_ = request.POST['dtfi']
	    extra = 1
	    date_ini = parse(dtini_)
	    dfini= date_ini.strftime("%Y-%m-%d")
	    date_fi = parse(dtfi_)
	    dffi= date_fi.strftime("%Y-%m-%d")
	    dtini = date_ini
	    dtfi = date_fi
	    if actualcli == "Tots" and actualot <> "Totes":
    	      detail = ots_deliver.objects.order_by('sentdate').all().filter(sentdate__range=[str(dfini), str(dffi)], ot = actualot)
	    elif actualcli <> "Tots" and actualot == "Totes":
    	      detail = ots_deliver.objects.order_by('sentdate').all().filter(sentdate__range=[str(dfini), str(dffi)], clientname = actualcli)
	    elif actualcli <> "Tots" and actualot <> "Totes":
    	      detail = ots_deliver.objects.order_by('sentdate').all().filter(sentdate__range=[str(dfini), str(dffi)], clientname = actualcli, ot = actualot)
	    else:
    	      detail = ots_deliver.objects.order_by('sentdate').all().filter(sentdate__range=[str(dfini), str(dffi)])
	    response = HttpResponse(content_type='application/vnd.ms-excel')
	    response['Content-Disposition'] = 'attachment; filename=Report.xlsx'
	    xlsx_data = WriteToExcel(detail)
	    response.write(xlsx_data)
	    return response
	elif request.POST['action'] == 'reset':
            form = ots_deliver_form()
	    clidataini = ots_clients.objects.order_by('clientname').all()
	    otdataini = ots.objects.order_by('ot').all()
	    dtini  = datetime.datetime.now()
	    dtfi = datetime.datetime.now()
	    detail = ots_deliver.objects.order_by('sentdate').all().filter(iddeliver=-1)
	    extra = 0
	    actualcli = ""
	    actualot = ""
    else:
        form = ots_deliver_form()
	
    #print dtini
    #print dtfi
    context = {
        'form': form,
        'cliini': clidataini,
        'otini': otdataini,
	'dtini': dtini,
	'dtfi': dtfi,
	'detail': detail, 
	'extra': extra,
	'actualot': actualot,
	'actualcli': actualcli,
    }
    return render(request, 'datacubes/deliver.html', context)

def ots_deliver_vw(request):
    print request.user.id
    currentagent = agents.objects.values('agentcode').filter(user_id=request.user.id)
    if request.user.id == 1 or request.user.id == 2 or request.user.id == 12 or request.user.id == 8:
	print "Admin user"
    	otdataini = ots_deliver.objects.values('ot').order_by('ot').distinct()
    else:
	print "Guest user"
    	otdataini = ots_deliver.objects.values('ot').order_by('ot').filter(agent=currentagent).distinct()
    
    clidataini = ots_clients.objects.values('clientname').order_by('clientname').distinct()
    dtini  = datetime.datetime.now()
    dtfi = datetime.datetime.now()
    detail = ots_deliver.objects.order_by('sentdate').all().filter(iddeliver=-1)
    extra = 0
    actualcli = ""
    actualot = ""
    magatzem = "N/A"
    dtexpedicio = "N/A"
    transportista = "N/A"
    if request.method == 'POST':
	if (request.POST['action'] == "apply") or (request.POST['action'] == "del"):
	    print "Action to execute %s" % request.POST['action']
            form = ots_deliver_form(request.POST, request.FILES)
	    actualcli = request.POST['cliini']
	    actualot = request.POST['otini']
	    dtini_ = request.POST['dtini']
	    dtfi_ = request.POST['dtfi']
	    delot = request.POST.getlist('delot')
	    print delot
	    extra = 1
	    dfini = datetime.datetime.strptime(dtini_, "%d/%m/%Y").date() 
	    dffi = datetime.datetime.strptime(dtfi_, "%d/%m/%Y").date() 
	    dtini = dfini
	    dtfi = dffi
    	    v_clicod = ots_clients.objects.values('clicod').filter(clientname = actualcli)
	    #print dfini
	    #print dffi
	    ar = request.user.id
            print "user to find groups: %s" % ar	
	    tmpagent = agents.objects.filter(user_id=ar)
	    tmpagentgrp = agentrights.objects.select_related('idagent').select_related('idagentgroup').filter(idagent=tmpagent)
	    grps = 'null'
	    for ix in tmpagentgrp:
	        if grps == 'null':
		   groups = ix.idagentgroup.groupagentcode
	           grps = 'gul'
	        else:
		   groups = groups + ',' + ix.idagentgroup.groupagentcode

	    print groups
            if request.POST['action'] == "del":		
	   	for ix in range(0,len(delot)):
			print "I am going to del iddeliver's"
	    		try: 
				tmpdel = str(delot[ix]).replace(".","")
				print "Checkbox del status %s" % tmpdel
	        		if tmpdel:
		  			ots_deliver.objects.filter(pk=tmpdel).delete()
	    		except Exception as e:
				print e

	    if actualcli == "Tots" and actualot == "Totes":
    	       if request.user.id == 1 or request.user.id == 2 or request.user.id == 12 or request.user.id == 8:
    	         detail = ots_deliver.objects.select_related('idcarrier').order_by('sentdate','clientname','ot').all().filter(sentdate__range=[str(dfini), str(dffi)])
	       else:
    	         detail = ots_deliver.objects.select_related('idcarrier').order_by('sentdate','clientname','ot').all().filter(sentdate__range=[str(dfini), str(dffi)], agent__in = groups)
	    elif actualcli == "Tots" and actualot <> "Totes":
    	      detail = ots_deliver.objects.select_related('idcarrier').order_by('sentdate','clientname','ot').all().filter(ot = actualot)
	    elif actualcli <> "Tots" and actualot == "Totes":
    	       if request.user.id == 1 or request.user.id == 2 or request.user.id == 12 or request.user.id == 8:
    	          detail = ots_deliver.objects.select_related('idcarrier').order_by('sentdate','clientname','ot').all().filter(clicod = v_clicod, sentdate__range=[str(dfini), str(dffi)])
	       else:
    	          detail = ots_deliver.objects.select_related('idcarrier').order_by('sentdate','clientname','ot').all().filter(clicod = v_clicod, sentdate__range=[str(dfini), str(dffi)], agent__in = groups)
	    elif actualcli <> "Tots" and actualot <> "Totes":
    	      detail = ots_deliver.objects.select_related('idcarrier').order_by('sentdate','clientname','ot').all().filter(clicod = v_clicod, ot = actualot, sentdate__range=[str(dfini), str(dffi)])
	    else:
    	       if request.user.id == 1 or request.user.id == 2 or request.user.id == 12 or request.user.id == 8:
    	          detail = ots_deliver.objects.select_related('idcarrier').order_by('sentdate','clientname','ot').all().filter(sentdate__range=[str(dfini), str(dffi)])
	       else:
    	          detail = ots_deliver.objects.select_related('idcarrier').order_by('sentdate','clientname','ot').all().filter(sentdate__range=[str(dfini), str(dffi)], agent__in = groups)
        elif request.POST['action'] == 'export': 
            form = ots_deliver_form(request.POST, request.FILES)
	    actualcli = request.POST['cliini']
	    actualot = request.POST['otini']
	    dtini_ = request.POST['dtini']
	    dtfi_ = request.POST['dtfi']
	    #print dtini_
	    #print dtfi_
	    extra = 1
	    dfini = datetime.datetime.strptime(dtini_, "%d/%m/%Y").date() 
	    dffi = datetime.datetime.strptime(dtfi_, "%d/%m/%Y").date() 
	    dtini = dfini
	    dtfi = dffi
    	    v_clicod = ots_clients.objects.values('clicod').filter(clientname = actualcli)
	    #print dfini
	    #print dffi
	    if actualcli == "Tots" and actualot == "Totes":
    	      detail = ots_deliver.objects.select_related('idcarrier').order_by('sentdate','clientname','ot').all().filter(sentdate__range=[str(dfini), str(dffi)])
	    elif actualcli == "Tots" and actualot <> "Totes":
    	      detail = ots_deliver.objects.select_related('idcarrier').order_by('sentdate','clientname','ot').all().filter(ot = actualot)
	    elif actualcli <> "Tots" and actualot == "Totes":
    	      detail = ots_deliver.objects.select_related('idcarrier').order_by('sentdate','clientname','ot').all().filter(sentdate__range=[str(dfini), str(dffi)], clicod = v_clicod)
	    elif actualcli <> "Tots" and actualot <> "Totes":
    	      detail = ots_deliver.objects.select_related('idcarrier').order_by('sentdate','clientname','ot').all().filter(sentdate__range=[str(dfini), str(dffi)], clicod = v_clicod, ot = actualot)
	    else:
    	      detail = ots_deliver.objects.select_related('idcarrier').order_by('sentdate','clientname','ot').all().filter(sentdate__range=[str(dfini), str(dffi)])
	    response = HttpResponse(content_type='application/vnd.ms-excel')
	    response['Content-Disposition'] = 'attachment; filename=Report.xlsx'
	    xlsx_data = WriteToExcel(detail)
	    response.write(xlsx_data)
	    return response
	elif request.POST['action'] == 'reset':
            form = ots_deliver_form()
	    clidataini = ots_clients.objects.order_by('clientname').all()
	    otdataini = ots.objects.order_by('ot').all()
	    dtini  = datetime.datetime.now()
	    dtfi = datetime.datetime.now()
	    detail = ots_deliver.objects.order_by('sentdate').all().filter(iddeliver=-1)
	    extra = 0
	    actualcli = ""
	    actualot = ""
    else:
        form = ots_deliver_form()
	
    #print dtini
    #print dtfi
    context = {
        'form': form,
        'cliini': clidataini,
        'otini': otdataini,
	'dtini': dtini,
	'dtfi': dtfi,
	'detail': detail, 
	'extra': extra,
	'actualot': actualot,
	'actualcli': actualcli,
	'magatzem': magatzem,
	'dtexpedicio': dtexpedicio,
	'transportista': transportista,
    }
    return render(request, 'datacubes/ot_deliver.html', context)


def register_user(request):
    if request.method == 'POST':
        form = registeruser_form(request.POST, request.FILES)
        # Comprobamos si el formulario es valido
        if form.is_valid():
            # En caso de ser valido, obtenemos los datos del formulario.
            # form.cleaned_data obtiene los datos limpios y los pone en un
            # diccionario con pares clave/valor, donde clave es el nombre del campo
            # del formulario y el valor es el valor si existe.
            cleaned_data = form.cleaned_data
            username = cleaned_data.get('username')
            password = cleaned_data.get('password')
            email = cleaned_data.get('email')
            photo = cleaned_data.get('photo')
            # E instanciamos un objeto User, con el username y password
            user_model = User.objects.create_user(username=username, password=password)
            # Añadimos el email
            user_model.email = email
            # Y guardamos el objeto, esto guardara los datos en la db.
            user_model.save()
            # Ahora, creamos un objeto UserProfile, aunque no haya incluido
            # una imagen, ya quedara la referencia creada en la db.
            user_profile = userprofile()
            # Al campo user le asignamos el objeto user_model
            user_profile.user = user_model
            # y le asignamos la photo (el campo, permite datos null)
            user_profile.photo = photo
            # Por ultimo, guardamos tambien el objeto UserProfile
            user_profile.save()
            # Ahora, redireccionamos a la pagina accounts/gracias.html
            # Pero lo hacemos con un redirect.
            return redirect(reverse('datacubes.views.register_user_succesfull', kwargs={'username': username}))
    else:
        form = registeruser_form()
    context = {
        'form': form
    }
    return render(request, 'datacubes/register.html', context)

def register_user_succesfull(request, username):
    return render(request, 'datacubes/register_succesfull.html', {'username': username})

def user_profile(request, pk):
        usuprofile = get_object_or_404(userprofile.objects.select_related('user__username', 'user__email').only('user__username', 'user__email', 'photo'), user_id=pk) 
#        usuprofile = get_object_or_404(userprofile.objects.select_related('user__username', 'user__email').only('user__username', 'user__email', 'photo').get(user_id=pk), pk=pk)
	action = 1
	#print "============================================================="
	#print "Update user profile"
	#print "============================================================="
	#print action
	#print usuprofile.user.username
	#print usuprofile.user.email
	#print usuprofile.photo
	context = {
			'username': usuprofile.user.username, 
			'email':  usuprofile.user.email,
			'photo':  usuprofile.photo,
			'type': action,
		  }				
	return render(request, 'datacubes/user_detail.html', context)


def login_user(request):
    # Si el usuario esta ya logueado, lo redireccionamos a index_view
    if request.user.is_authenticated():
        return redirect(reverse('datacubes.views.index'))

    mensaje = ''
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
		usuid = User.objects.only('id').get(username=username)
        	usuprof = userprofile.objects.only('photo').get(user_id=usuid) 
		#print "userid", str(usuid)
		#print "userphoto", str(usuprof.photo)
                login(request, user)
		context = {
				'photo': usuprof.photo,
		}
                return redirect(reverse('datacubes.views.index'),context)
            else:
                # Redireccionar informando que la cuenta esta inactiva
                # Lo dejo como ejercicio al lector :)
                # pass
            	mensaje = 'User or password incorrect'
    	    	return render(request, 'datacubes/login_user.html', {'mensaje': mensaje})
	else:
            mensaje = 'User or password incorrect'
    	    return render(request, 'datacubes/login_user.html', {'mensaje': mensaje})
	
        mensaje = 'User or password incorrect'
    return render(request, 'datacubes/login_user.html', {'mensaje': mensaje})

def logout_user(request):
    logout(request)
    return redirect(reverse('datacubes.views.login_user'))

@login_required(login_url='/login/')
def edituser_email(request):
    if request.method == 'POST':
        form = usereditemail_form(request.POST, request=request)
        if form.is_valid():
            request.user.email = form.cleaned_data['email']
            request.user.save()
            messages.success(request, 'Email changed succesfull')
            return redirect(reverse('datacubes.views.index'))
    else:
        form = usereditemail_form(
            request=request,
            initial={'email': request.user.email})
    return render(request, 'datacubes/useredit_email.html', {'form': form})

# Añadir al final
@login_required(login_url='/login/')
def edituser_password(request):
    if request.method == 'POST':
        form = usereditpassword_form(request.POST)
        if form.is_valid():
            request.user.password = make_password(form.cleaned_data['password'])
            request.user.save()
            messages.success(request, 'Succesfull changed password.')
            messages.success(request, 'You indicate new password for user')
            return redirect(reverse('datacubes.views.index'))
    else:
        form = usereditpassword_form()
    return render(request, 'datacubes/useredit_password.html', {'form': form})

