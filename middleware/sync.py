#! /usr/bin/python
# -*- coding: utf-8 -*-
import pyodbc
import json
import collections
from decimal import Decimal
import MySQLdb
import time
from datetime import datetime, date, time, timedelta

db = MySQLdb.connect(host="localhost",    # your host, usually localhost
                     user="admregara",         # your username
                     passwd="RegarA_*",  # your password
                     db="dbregara",
                     charset='utf8')        # name of the data base


#conn = pyodbc.connect('DRIVER=ms-sql;SERVER=10.25.1.230;PORT=1433;DATABASE=DATO01EGAR;UID=guillem;PWD=Maig160551;TDS_Version=8.0;')
conn = pyodbc.connect('DRIVER=ms-sql;SERVER=10.111.11.211;PORT=1433;DATABASE=DATO01EGAR;UID=sa;PWD=Jul020751;TDS_Version=8.0;')

today2 = '2017-02-28'
week2 = '2016-01-01'
todaytmp = date.today()
dias2 = timedelta(days=15)
dias = timedelta(days=180)
week = todaytmp-dias
today = todaytmp+dias2

print ("START PROCESS ............................")

curupgrade = conn.cursor()

curupgrade.execute(""" DELETE FROM tbinformes """)

curupgrade.execute(""" 
insert into tbinformes (fsend,
ot,
codcli,
cli,
otname,
codprod,
clicom,
delivered,
quantity,
nominal,
location,
machine,
qytotalstorage,
agent,
enddate,
originaldate,
multiline,
autline)
SELECT e_corden.FENTREGA as fsend 
                      ,replace(ltrim(e_corden.codigo), '''', '''''') as ot
                      ,ltrim(e_corden.CODCLI) as codcli  
                      ,replace(ltrim(e_corden.nombre), '''', '''''') as cli 
                      ,replace(ltrim(e_corden.descrip), '''', '''''') as otname
                      ,replace(ltrim(e_corden.PRODUCTO), '''',  '''''') as codprod
                      ,e_corden.CAMPO1 as clicom
                      ,case
			when e_corden.ENVIADO is null then 0
			else e_corden.ENVIADO
		       end as delivered
                      ,case
			when e.CANTIDAD is null then 0
			else e.CANTIDAD
		       end as quantity
                      ,case
			when e_corden.CANTIDAD0 is null then 0
			else e_corden.CANTIDAD0
		       end as nominal
                      ,case
                          when e_corden.CAMPO3 is not null then REPLACE(e_corden.CAMPO3, '''', '''''')
                          else 'NO INFORMAT' 
                       end as location
                      ,eo.C44 AS machine
                      ,case 
			when e_corden.ENVIADO > 0 then (e_corden.ALMACENADO - e_corden.ENVIADO) 
		        else case
				when e_corden.ALMACENADO is null then 0
				else e_corden.ALMACENADO
			     end
		       end AS qytotalstorage
                      ,e_corden.REPRESEN
                      ,case 
                        when e_corden.FECFINAL is not null then e_corden.FECFINAL
                        else ''
                       end fechafin 
       ,e.FECHA as originaldate
       ,0
       ,0
FROM dato01EGAR.dbo.e_corden e_corden left join dato01EGAR.dbo.E_ENTREG e
  on e.CODIGO = e_corden.CODIGO 
 and e.CODCLI = e_corden.CODCLI right join (select e2.CODIGO, e2.CODCLI
from   E_CORDEN eo1 left join  E_ENTREG e2
  on   e2.CODIGO = eo1.CODIGO
 and   e2.CODCLI = eo1.CODCLI
where  (
	     (e2.CODIGO is not null) and
	     (LEN(e2.codigo) > 0)
	    )
group by e2.CODIGO, e2.CODCLI
having COUNT(*) = 1) e3
   on  e.CODCLI = e3.codcli
  and  e.CODIGO = e3.CODIGO left join dato01egar.dbo.E_EORDEN eo
                   on eo.CODIGO = e_corden.CODIGO
                  and eo.PAGINA = 0 
                 where e.cantidad > 5
                   and eo.C44 is not null
		   and LEN(e_corden.PRODUCTO) > 0
		   and e_corden.FENTREGA between '"""+str(week)+"""' and '"""+str(today)+"""'"""
)

curupgrade.execute(""" 
insert into tbinformes (fsend,
ot,
codcli,
cli,
otname,
codprod,
clicom,
delivered,
quantity,
nominal,
location,
machine,
qytotalstorage,
agent,
enddate,
originaldate,
multiline,
autline)
SELECT e_corden.FENTREGA as fsend
                      ,replace(ltrim(e_corden.codigo), '''', '''''') as ot
                      ,ltrim(e_corden.CODCLI) as codcli
                      ,replace(ltrim(e_corden.nombre), '''', '''''') as cli
                      ,replace(ltrim(e_corden.descrip), '''', '''''') as otname
		      ,[DATO01EGAR].[dbo].[fnVirtSplit] (A.TEXTO,' ',1) AS codprod	
                      ,e_corden.CAMPO1 as clicom
                      ,case
                        when e_corden.ENVIADO is null then 0
                        else e_corden.ENVIADO
                       end as delivered
		      ,CAST(CAST([DATO01EGAR].[dbo].[fnVirtSplit] (A.TEXTO,' ',2) AS INT) AS DECIMAL(10,2)) as quantity		  
                      ,case
                        when e_corden.CANTIDAD0 is null then 0
                        else e_corden.CANTIDAD0
                       end as nominal
                      ,case
                          when e_corden.CAMPO3 is not null then REPLACE(e_corden.CAMPO3, '''', '''''')
                          else 'NO INFORMAT'
                       end as location
                      ,eo.C44 AS machine
                      ,case
                        when e_corden.ENVIADO > 0 then (e_corden.ALMACENADO - e_corden.ENVIADO)
                        else case
                                when e_corden.ALMACENADO is null then 0
                                else e_corden.ALMACENADO
                             end
                       end AS qytotalstorage
                      ,e_corden.REPRESEN
                      ,case
                        when e_corden.FECFINAL is not null then e_corden.FECFINAL
                        else ''
                       end fechafin
       ,e.FECHA as originaldate
       ,0
       ,0
FROM dato01EGAR.dbo.e_corden e_corden left join dato01EGAR.dbo.E_ENTREG e
  on e.CODIGO = e_corden.CODIGO
 and e.CODCLI = e_corden.CODCLI left join E_AORDEN A
  on   A.CODIGO = e_corden.CODIGO
right join (select e2.CODIGO, e2.CODCLI
from   E_CORDEN eo1 left join  E_ENTREG e2
  on   e2.CODIGO = eo1.CODIGO
 and   e2.CODCLI = eo1.CODCLI
where  (
	     (e2.CODIGO is not null) and
	     (LEN(e2.codigo) > 0)
	    )
group by e2.CODIGO, e2.CODCLI
having COUNT(*) = 1) e3
   on  e.CODCLI = e3.codcli
  and  e.CODIGO = e3.CODIGO left join dato01egar.dbo.E_EORDEN eo
                   on eo.CODIGO = e_corden.CODIGO
                  and eo.PAGINA = 0 
                 where e.cantidad > 5
                   and eo.C44 is not null
		   and LEN(e_corden.PRODUCTO) = 0
		   and a.LINEA = '00001' 
		   and e_corden.FENTREGA between '"""+str(week)+"""' and '"""+str(today)+"""'"""
)

curupgrade.execute("""
 insert into tbinformes (fsend,
ot,
codcli,
cli,
otname,
codprod,
clicom,
delivered,
quantity,
nominal,
location,
machine,
qytotalstorage,
agent,
enddate,
originaldate,
multiline,
autline)

SELECT e.FECHA as fsend 
                      ,replace(ltrim(e_corden.codigo), '''', '''''') as ot
                      ,ltrim(e_corden.CODCLI) as codcli  
                      ,replace(ltrim(e_corden.nombre), '''', '''''') as cli 
                      ,replace(ltrim(e_corden.descrip), '''', '''''') as otname
                      ,replace(ltrim(e_corden.PRODUCTO), '''',  '''''') as codprod
                      ,e_corden.CAMPO1 as clicom
                      ,case 
			when e_corden.ENVIADO is null then 0
			else e_corden.ENVIADO
		       end as delivered
                      ,case
			when e.CANTIDAD is null then 0
			else e.CANTIDAD
		       end as quantity
                      ,case
			when e_corden.CANTIDAD0 is null then 0
			else e_corden.CANTIDAD0
                       end as nominal
                      ,case
                          when e_corden.CAMPO3 is not null then REPLACE(e_corden.CAMPO3, '''', '''''')
                          else 'NO INFORMAT' 
                       end as location
                      ,eo.C44 AS machine
                      ,case 
			when e_corden.ENVIADO > 0 then (e_corden.ALMACENADO - e_corden.ENVIADO) 
			else case
				when e_corden.ALMACENADO is null then 0
				else e_corden.ALMACENADO
			     end
		       end AS qytotalstorage
                      ,e_corden.REPRESEN
                      ,case 
                        when e_corden.FECFINAL is not null then e_corden.FECFINAL
                        else ''
                       end fechafin                     
	,e.FECHA as originaldate
        ,1
        ,e.autolinea
FROM dato01EGAR.dbo.e_corden e_corden left join dato01EGAR.dbo.E_ENTREG e
  on e.CODIGO = e_corden.CODIGO 
 and e.CODCLI = e_corden.CODCLI right join (select e2.CODIGO, e2.CODCLI
from   E_CORDEN eo1 left join  E_ENTREG e2
  on   e2.CODIGO = eo1.CODIGO
 and   e2.CODCLI = eo1.CODCLI
where  (
	     (e2.CODIGO is not null) and
	     (LEN(e2.codigo) > 0)
	    )
group by e2.CODIGO, e2.CODCLI
having COUNT(*) > 1) e3
   on  e.CODCLI = e3.codcli
  and  e.CODIGO = e3.CODIGO left join dato01egar.dbo.E_EORDEN eo
                   on eo.CODIGO = e_corden.CODIGO
                  and eo.PAGINA = 0                                            
                 where e.cantidad > 0
                   and e.linea <> '001'           
                   and eo.C44 is not null
		   and e.fecha between  '"""+str(week)+"""' and '"""+str(today)+"""'"""
)

curupgrade.close()
conn.commit()

cur = conn.cursor()

cur.execute("""
                 select fsend, ot, codcli, cli, otname, codprod, clicom, delivered, quantity, nominal, location, machine, qytotalstorage, 
                 case when agent is null then 'Sense informar' else agent end as agent, enddate, originaldate, multiline, autline, codcli from tbinformes
            """)
 
rows = cur.fetchall()

rl = []
for r in rows:
    t = (r.fsend, r.ot, r.codcli, r.cli, r.otname, r.codprod, r.clicom, r.delivered, r.quantity, r.nominal, r.agent)
    print "========================================================================="
    print r.fsend 
    print r.ot 
    print "========================================================================="
    rl.append(t)

# you must create a Cursor object. It will let
#  you execute all the queries you need
    curmy = db.cursor()
    curupd = db.cursor()
    curins = db.cursor()

# Use all the SQL you like
    vmulti = r.multiline
    if vmulti == 1:
    	curmy.execute("SELECT ot  FROM datacubes_ots_deliver where ot = '"+r.ot+"' and codproduct = '"+r.codprod+"' and clientcommand = '"+r.clicom+"' and autline ='"+str(r.autline)+"'")
    elif vmulti == 0:
    	curmy.execute("SELECT ot  FROM datacubes_ots_deliver where ot = '"+r.ot+"' and codproduct = '"+r.codprod+"' and clientcommand = '"+r.clicom+"' and originaldate ='"+str(r.originaldate)+"'")

    if curmy.rowcount :
        print "Exist"
	if vmulti == 0:
		upd = "UPDATE datacubes_ots_deliver SET sentdate = '"+r.fsend+"', deliverparcial = '"+str(r.delivered)+"', totaldeliver = '"+str(r.quantity)+"', nominalprovided = '"+str(r.nominal)+"', totalstorage = '"+str(r.qytotalstorage)+"', location = '"+r.location+"', machine = '"+ r.machine+"', agent = '"+r.agent+"', enddate = '"+ str(r.enddate)+"', clicod = '" + r.codcli + "' where ot = '"+r.ot+"' and codproduct = '"+r.codprod+"' and clientcommand = '"+r.clicom+"' and originaldate ='"+str(r.originaldate)+"'"
		print upd
	elif vmulti == 1:
		upd = "UPDATE datacubes_ots_deliver SET sentdate = '"+r.fsend+"', deliverparcial = '"+str(r.delivered)+"', totaldeliver = '"+str(r.quantity)+"', nominalprovided = '"+str(r.nominal)+"', totalstorage = '"+str(r.qytotalstorage)+"', location = '"+r.location+"', machine = '"+ r.machine+"', agent = '"+r.agent+"', enddate = '"+ str(r.enddate)+"', autline = '"+str(r.autline)+"', clicod = '" + r.codcli + "' where ot = '"+r.ot+"' and codproduct = '"+r.codprod+"' and clientcommand = '"+r.clicom+"' and autline ="+str(r.autline)+""
		print upd
	try:
	   curupd.execute(upd)
	   db.commit()
        except MySQLdb.Error, e:
           db.rollback()
           try:
               print "MySQL Error [%d]: %s" % (e.args[0], e.args[1])
           except IndexError:
               print "MySQL Error: %s" % str(e)
    else :
        print "Not exist"
	ins = "INSERT INTO datacubes_ots_deliver (sentdate, ot, clientname, otname, codproduct, clientcommand, deliverparcial, totaldeliver, nominalprovided, user_id, delivereddate, idcarrier_id, totalstorage, location, machine, agent, enddate,originaldate, autline, clicod) VALUES ('"+r.fsend+"', '"+r.ot+"', '"+r.cli+"', '"+r.otname+"', '"+r.codprod+"','"+r.clicom+"', '" +str(r.delivered)+"','"+str(r.quantity)+"','"+str(r.nominal)+"', 1, '', 25,'"+str(r.qytotalstorage)+"', '"+r.location+"', '"+r.machine+"', '"+r.agent+"', '"+str(r.enddate)+"', '"+str(r.originaldate)+"', "+str(r.autline)+",'" + r.codcli + "')"
        print ins
	try:
	   curins.execute(ins) 
	   db.commit()
        except MySQLdb.Error, e:
           db.rollback()
           try:
              print "MySQL Error [%d]: %s" % (e.args[0], e.args[1])
           except IndexError:
              print "MySQL Error: %s" % str(e)

curcli = db.cursor()
curots = db.cursor()

curcli.execute('DELETE FROM datacubes_ots_clients')
curcli.execute('alter table datacubes_ots_clients auto_increment = 1')
curcli.execute('insert into  datacubes_ots_clients (clientname, clicod) select distinct ltrim(clientname), clicod from datacubes_ots_deliver where clientname is not null and clicod is not null')
db.commit()

curots.execute('DELETE FROM datacubes_ots')
curots.execute('alter table datacubes_ots auto_increment = 1')
curots.execute('insert into  datacubes_ots (ot, otname) select distinct ot, otname from datacubes_ots_deliver')

db.commit()
db.close()

conn.commit()
conn.close()

print ("END PROCESS ............................")
