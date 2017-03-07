# -*- coding: utf-8 -*-
import pyodbc
import json
import collections
from decimal import Decimal
import MySQLdb
import time
from datetime import datetime, date, time, timedelta

db = MySQLdb.connect(host="localhost",    # your host, usually localhost
                     user="root",         # your username
                     passwd="Jul020751",  # your password
                     db="dbregara",
		     charset='utf8')        # name of the data base


#conn = pyodbc.connect('DRIVER=ms-sql;SERVER=10.25.1.230;PORT=1433;DATABASE=DATO01EGAR;UID=guillem;PWD=Maig160551;TDS_Version=8.0;')
conn = pyodbc.connect('DRIVER=ms-sql;SERVER=10.111.11.211;PORT=1433;DATABASE=DATO01EGAR;UID=sa;PWD=Jul020751;TDS_Version=8.0;')

cur = conn.cursor()

cur.execute("""
                 select fsend, ot, codcli, cli, otname, codprod, clicom, delivered, quantity, nominal, location, machine, qytotalstorage, 
                 case when agent is null then 'Sense informar' else agent end as agent from tbinformes
            """)
 
rows = cur.fetchall()

rl = []
for r in rows:
    t = (r.fsend, r.ot, r.codcli, r.cli, r.otname, r.codprod, r.clicom, r.delivered, r.quantity, r.nominal, r.agent)
    print "========================================================================="
    print r.fsend 
    print r.ot 
    print r.codcli 
    print r.cli 
    print r.otname 
    print r.codprod 
    print r.clicom 
    print r.delivered 
    print r.quantity 
    print r.nominal
    print r.qytotalstorage
    print r.agent
    print "========================================================================="
    rl.append(t)

# you must create a Cursor object. It will let
#  you execute all the queries you need
    cur = db.cursor()

# Use all the SQL you like
    cur.execute("SELECT ot  FROM datacubes_ots_deliver where ot = '"+r.ot+"' and codproduct = '"+r.codprod+"' and clientcommand = '"+r.clicom+"' and sentdate ='"+r.fsend+"'")

    if cur.rowcount :
        print "Exist"
	curupd = db.cursor()
	upd = "UPDATE datacubes_ots_deliver SET sentdate = '"+r.fsend+"', deliverparcial = '"+str(r.delivered)+"', totaldeliver = '"+str(r.quantity)+"', nominalprovided = '"+str(r.nominal)+"', totalstorage = '"+str(r.qytotalstorage)+"', location = '"+r.location+"', machine = '"+ r.machine+"', agent = '"+r.agent+"' where ot = '"+r.ot+"' and codproduct = '"+r.codprod+"' and clientcommand = '"+r.clicom+"' and sentdate ='"+r.fsend+"'"
	print upd
	curupd.execute(upd)
	curupd.close()
	db.commit()
    else :
	print "Not exist"
	curins = db.cursor()
	ins = "INSERT INTO datacubes_ots_deliver (sentdate, ot, clientname, otname, codproduct, clientcommand, deliverparcial, totaldeliver, nominalprovided, user_id, delivereddate, idcarrier_id, totalstorage, location, machine, agent) VALUES ('"+r.fsend+"', '"+r.ot+"', '"+r.cli+"', '"+r.otname+"', '"+r.codprod+"','"+r.clicom+"', '" +str(r.delivered)+"','"+str(r.quantity)+"','"+str(r.nominal)+"', 1, '19990101 00:00:00', 1,'"+str(r.qytotalstorage)+"', '"+r.location+"', '"+r.machine+"', '"+r.agent+"')"
	print ins 
	curins.execute(ins) 
	curins.close()
	db.commit()
#j = json.dumps(rl)
#rf = '/resource/virtelix/regara/middleware/sync.json'
#f = open(rf,'w')
#print >> f, j

    cur.close()

curcli = db.cursor()
curots = db.cursor()

curcli.execute('DELETE FROM datacubes_ots_clients')
curcli.execute('alter table datacubes_ots_clients auto_increment = 1')
curcli.execute('insert into  datacubes_ots_clients (clientname) select distinct clientname from datacubes_ots_deliver')
curcli.close()
db.commit()

curots.execute('DELETE FROM datacubes_ots')
curots.execute('alter table datacubes_ots auto_increment = 1')
curots.execute('insert into  datacubes_ots (ot, otname) select distinct ot, otname from datacubes_ots_deliver')
curots.close()

db.commit()
db.close()
