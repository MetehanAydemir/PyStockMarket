# -*- coding: utf-8 -*-
"""
Created on Thu Jul 21 15:47:33 2022

@author: Admin
"""

import MetaTrader5 as mt
from datetime import datetime
import pandas as pd 
import pypyodbc as odbc
import time 



#Initilizing Meta trader
login =**********
Path='C:\\Program Files\\FinveoMNMT5Terminal\\terminal64.exe'
password ='**********'
server='FinveoMN-Live'
mt.initialize(Path)
mt.login(login,password,server)


#Sql connection and query
conn = odbc.connect("DRIVER={SQL Server};SERVER=**********\MSSQLSERVER2014;UID=adminfx ;PWD=*****; DATABASE=db_fxhaber;'Trusted_Connection=yes;")

imlec = conn.cursor()
imlec.execute('SELECT* FROM dbo.live_prices')
kullanicilar = imlec.fetchall()

    
#imlec.execute('''INSERT INTO db_denemeadmin.correlation (time,[close]) VALUES ('2022-08-21',18.155) ''')
#imlec.commit
for i in kullanicilar:
    print(i)
    
#imlec.execute('Delete FROM dbo.live_prices')
#imlec.commit()
pair=['AUDUSD','EURJPY','EURTRY','EURUSD','GBPJPY','GBPUSD','USDJPY','USDTRY','XAGUSD','XAUUSD']
counter=1
for i in pair:
    symbol=pd.DataFrame(mt.copy_rates_from(i,mt.TIMEFRAME_D1,datetime.now(),1))
    date = datetime.now()
    date = date.strftime('%Y-%m-%d %H:%M:%S')
    for row in symbol.itertuples(index=True):
        imlec.execute('''INSERT INTO dbo.live_prices VALUES({},'{}',{},{},{},'{}') '''.format(counter,i,getattr(row,"close"),getattr(row,"high"),getattr(row,"low"),date))
        imlec.commit()
        #print(counter,i,getattr(row,"close"),getattr(row,"high"),getattr(row,"low"),date)
    counter+=1

while True:
    imlec.execute('Delete FROM dbo.live_prices')
    imlec.commit()
    counter=1
    for i in pair:
        symbol=pd.DataFrame(mt.copy_rates_from(i,mt.TIMEFRAME_D1,datetime.now(),1))
        date = datetime.now()
        date = date.strftime('%Y-%m-%d %H:%M:%S')
        for row in symbol.itertuples(index=True):
            imlec.execute('''INSERT INTO dbo.live_prices VALUES({},'{}',{},{},{},'{}') '''.format(counter,i,getattr(row,"close"),getattr(row,"high"),getattr(row,"low"),date))
            imlec.commit()
            #print(counter,i,getattr(row,"close"),getattr(row,"high"),getattr(row,"low"),date)
        counter+=1
    for a in range(1800):
        counter2=0
        for i in pair:
            symbol=pd.DataFrame(mt.copy_rates_from(i,mt.TIMEFRAME_D1,datetime.now(),1))
            date = datetime.now()
            date = date.strftime('%Y-%m-%d %H:%M:%S')
            for row in symbol.itertuples(index=True):
                imlec.execute('''UPDATE dbo.live_prices SET closing_price={},updated_at='{}' WHERE pair='{}' '''.format(getattr(row,"close"),date,i))
                imlec.commit() 
                #print(counter,i,getattr(row,"close"),getattr(row,"high"),getattr(row,"low"),date)
        time.sleep(2)
    
    
