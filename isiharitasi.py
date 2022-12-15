#try methodu uygulanacak
import MetaTrader5 as mt
import pandas as pd
import numpy as np
from datetime import datetime
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
imlec.execute('SELECT* FROM dbo.KORELASYON')
kullanicilar = imlec.fetchall()
for i in kullanicilar:
    print(i)

Name=['AUD','CAD','CHF','EUR','GBP','USD','JPY']
symbols=[[1,'AUDCAD' ,'AUDCHF', 'EURAUD', 'GBPAUD', 'AUDUSD', 'AUDJPY'],
         ['AUDCAD',1,'CADCHF','EURCAD', 'GBPCAD', 'USDCAD', 'CADJPY'],
         ['AUDCHF','CADCHF',1,'EURCHF' ,'GBPCHF', 'USDCHF', 'CHFJPY'],
         ['EURAUD','EURCAD','EURCHF',1,'EURGBP' ,'EURUSD', 'EURJPY'],
         ['GBPAUD','GBPCAD','GBPCHF','EURGBP',1,'GBPUSD' ,'GBPJPY'],
         ['AUDUSD','USDCAD','USDCHF','EURUSD','GBPUSD' ,1,'USDJPY'],
         ['AUDJPY','CADJPY','CHFJPY','EURJPY','GBPJPY','USDJPY',1]]
symbols=pd.DataFrame(symbols,columns=Name, index=Name)

def sicaklikharita(symbols,counter0,contern):
        symbol = pd.DataFrame(mt.copy_rates_from(symbols,mt.TIMEFRAME_D1,datetime.now(),1))
        if (8*counter0)<contern:
            value=(symbol['open']-symbol['close'])/symbol['open']*100
            return value.item()
        else:
            if (8*counter0)== contern:
                return 88.0
            
            value=((1/symbol['open'])-(1/symbol['close']))/(1/symbol['open'])*100
            return value.item()
while True:
    counter0 = 0 
    counter00=0
    counter1 = 1 
    counter2 = 2 
    counter3 = 3 
    counter4 = 4 
    counter5 = 5 
    counter6 = 6 
    #imlec.execute('''DELETE FROM fx-admin.SicaklikH''')
    
    for row in symbols.itertuples(index=True):
            AUD=getattr(row, Name[0])
            CAD=getattr(row, Name[1])
            CHF=getattr(row, Name[2])
            EUR=getattr(row, Name[3])
            GBP=getattr(row, Name[4])
            USD=getattr(row, Name[5])
            JPY=getattr(row, Name[6])
            
            #imlec.execute('''INSERT INTO fx-admin.SicaklikH VALUES ('{}',{},{},{},{},{},{},{})'''.format(Name[counter0],sicaklikharita(AUD,counter0,counter00),sicaklikharita(CAD,counter0,counter1),sicaklikharita(CHF,counter0,counter2),sicaklikharita(EUR,counter0,counter3),sicaklikharita(GBP,counter0,counter4),sicaklikharita(USD,counter0,counter5),sicaklikharita(JPY,counter0,counter6)))

            imlec.execute('''UPDATE dbo.SicaklikH SET AUD={},CAD={},CHF={},EUR={},GBP={},USD={},JPY={} WHERE pair='{}' '''.format(sicaklikharita(AUD,counter0,counter00),sicaklikharita(CAD,counter0,counter1),sicaklikharita(CHF,counter0,counter2),sicaklikharita(EUR,counter0,counter3),sicaklikharita(GBP,counter0,counter4),sicaklikharita(USD,counter0,counter5),sicaklikharita(JPY,counter0,counter6),Name[counter0]))
            imlec.commit()
            counter0+=1
            counter00+=7
            counter1 += 7 
            counter2 += 7 
            counter3 += 7 
            counter4 += 7 
            counter5 += 7 
            counter6 += 7 
    
    time.sleep(1)
