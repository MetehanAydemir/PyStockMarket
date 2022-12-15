import MetaTrader5 as mt
import pandas as pd
import numpy as np
from datetime import datetime
from sklearn.preprocessing import MinMaxScaler
import pypyodbc as odbc
from time import sleep

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
imlec.execute('SELECT* FROM dbo.SicaklikH')
kullanicilar = imlec.fetchall()
for i in kullanicilar:
    print(i)

symbols = np.chararray(10,itemsize=10,unicode=True)
symbols[0]='EURUSD'
symbols[1]='AUDUSD'
symbols[2]='CHFJPY'
symbols[3]='EURJPY'
symbols[4]='GBPJPY'
symbols[5]='GBPUSD'
symbols[6]='USDCAD'
symbols[7]='USDCHF'
symbols[8]='USDJPY'
symbols[9]='USDSEK'

for s in symbols:
    imlec.execute('''DELETE FROM adminfx.{}'''.format(s))
    imlec.commit()
def first(symbols,x):
    First = 0
    while First ==0: 
        for s in range(len(symbols)):
            pos=pd.DataFrame(mt.copy_rates_from(symbols[s],x,datetime.now(),70))
            pos['time']=pd.to_datetime(pos['time'],unit ='s')
            pos = pos[['close','time']]
            if x is mt.TIMEFRAME_D1:
                pos['time_interval']='D1'
                counter=1
                unitt='D'
            elif x is mt.TIMEFRAME_H4:
                pos['time_interval']='H4'
                counter=80
                unitt='s'
            elif x is mt.TIMEFRAME_H1:
                pos['time_interval']='H1'
                counter=160
                unitt='s'
            elif x is mt.TIMEFRAME_M15:
                pos['time_interval']='M15'
                counter=250
                unitt='s'
            for b in range(s+1,(s+len(symbols))):
                try:
                    a =b%(len(symbols))
                    posp=pd.DataFrame(mt.copy_rates_from(symbols[a],x,datetime.now(),70))
                    posp['time']=pd.to_datetime(posp['time'],unit ='s')
                    posp.rename(columns={'close': symbols[a]},inplace=True)
                    posp= posp[['time',symbols[a]]]
                    c =pos.min()
                    d = pos.max()
                    minmaxsc=MinMaxScaler(feature_range=(c['close'],d['close']))
                    Posp=posp.set_index('time')
                    posp.loc[:,symbols[a]]=minmaxsc.fit_transform(Posp,)
                    
                    pos =pos.merge(posp,how='left')
                except:
                    print("row is skipped")
            for row in pos.itertuples(index=True):
                try:
                    ass=getattr(row, "time")
                #if x is mt.TIMEFRAME_D1:
                #    ass = np.datetime64(ass,unitt)
                
                    imlec.execute('''INSERT INTO adminfx.{} VALUES ({},{},'{}','{}',{},{},{},{},{},{},{},{},{})'''.format(symbols[s],counter,
                                                                                                                          getattr(row, "close"),
                                                                                                                          ass,getattr(row, "time_interval"),
                                                                                                                          getattr(row,symbols[((s+1)%10)]),
                                                                                                                          getattr(row,symbols[((s+2)%10)]),
                                                                                                                          getattr(row,symbols[((s+3)%10)]),
                                                                                                                          getattr(row,symbols[((s+4)%10)]),
                                                                                                                          getattr(row,symbols[((s+5)%10)]),
                                                                                                                          getattr(row,symbols[((s+6)%10)]),
                                                                                                                          getattr(row,symbols[((s+7)%10)]),
                                                                                                                          getattr(row,symbols[((s+8)%10)]),
                                                                                                                          getattr(row,symbols[((s+9)%10)])))
                    imlec.commit()
                except:
                    print("Nan")
                counter+=1
        First = 1 
def Second(symbols,x):
    Second = 0
    while Second ==0: 
        for s in range(len(symbols)):
            pos=pd.DataFrame(mt.copy_rates_from(symbols[s],x,datetime.now(),70))
            pos['time']=pd.to_datetime(pos['time'],unit ='s')
            pos = pos[['close','time']]
            if x is mt.TIMEFRAME_D1:
                counter=1
                counter1=0 
                pos['time_interval']='D1'
                imlec.execute('''DELETE FROM adminfx.{}  WHERE id=1'''.format(symbols[s]))
                imlec.commit()
                unitt='D'

            elif x is mt.TIMEFRAME_H4:
                pos['time_interval']='H4'
                counter=80
                counter1=79 
                imlec.execute('''DELETE FROM adminfx.{}  WHERE id=80'''.format(symbols[s]))
                imlec.commit()
                unitt='s'

            elif x is mt.TIMEFRAME_H1:
                pos['time_interval']='H1'
                counter=160
                counter1=159
                imlec.execute('''DELETE FROM adminfx.{}  WHERE id=160'''.format(symbols[s]))
                imlec.commit()
                unitt='s'
            elif x is mt.TIMEFRAME_M15:
                pos['time_interval']='M15'
                imlec.execute('''DELETE FROM adminfx.{}  WHERE id=250'''.format(symbols[s]))
                imlec.commit()
                counter=250
                counter1=249
                unitt='s'
            for b in range(s+1,(s+len(symbols))):
                a =b%(len(symbols))
                posp=pd.DataFrame(mt.copy_rates_from(symbols[a],x,datetime.now(),70))
                posp['time']=pd.to_datetime(posp['time'],unit ='s')
                posp.rename(columns={'close': symbols[a]},inplace=True)
                posp= posp[['time',symbols[a]]]
                c =pos.min()
                d = pos.max()
                minmaxsc=MinMaxScaler(feature_range=(c['close'],d['close']))
                Posp=posp.set_index('time')
                posp.loc[:,symbols[a]]=minmaxsc.fit_transform(Posp,)
                
                pos =pos.merge(posp,how='left')
            for conter in range(counter,(counter+70)):
                imlec.execute('''UPDATE adminfx.{} SET id={} WHERE id={} '''.format(symbols[s],conter,(conter+1)))
                imlec.commit()  
            for row in pos.itertuples(index=True):
                ass=getattr(row, "time")
            
                if counter1 == 69 or counter1 == 149 or counter1 == 229 or counter1 == 309:
                    try:    
                        imlec.execute('''INSERT INTO adminfx.{} VALUES ({},{},'{}','{}',{},{},{},{},{},{},{},{},{})'''.format(symbols[s],(counter1),
                                                                                                                          getattr(row, "close"),
                                                                                                                          ass,getattr(row, "time_interval"),
                                                                                                                          getattr(row,symbols[((s+1)%10)]),
                                                                                                                          getattr(row,symbols[((s+2)%10)]),
                                                                                                                          getattr(row,symbols[((s+3)%10)]),
                                                                                                                          getattr(row,symbols[((s+4)%10)]),
                                                                                                                          getattr(row,symbols[((s+5)%10)]),
                                                                                                                          getattr(row,symbols[((s+6)%10)]),
                                                                                                                          getattr(row,symbols[((s+7)%10)]),
                                                                                                                          getattr(row,symbols[((s+8)%10)]),
                                                                                                                          getattr(row,symbols[((s+9)%10)])))
                        imlec.commit()
                    except:
                        print("NaN")
                counter1+=1
        Second = 1 
first(symbols, mt.TIMEFRAME_D1)
first(symbols, mt.TIMEFRAME_H4)
first(symbols, mt.TIMEFRAME_H1)
first(symbols, mt.TIMEFRAME_M15)




while True:
    Second(symbols, mt.TIMEFRAME_D1)
    for s in range(1,7):
        Second(symbols, mt.TIMEFRAME_H4)
        for t in range(1,5):
            Second(symbols, mt.TIMEFRAME_H1)
            for d in range(1,5):
                Second(symbols, mt.TIMEFRAME_M15)
                sleep(200)
