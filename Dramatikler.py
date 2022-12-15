
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from PIL import Image
import MetaTrader5 as mt
from datetime import datetime
import datetime as dt
import pandas as pd 
import pypyodbc as odbc
import time 
import numpy as np
import matplotlib.pyplot as plt
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
imlec.execute('SELECT* FROM dbo.live_prices')
kullanicilar = imlec.fetchall()
for i in kullanicilar:
    print(i)

def convertToBin(filename):
    #Convert digital data to binary format
    with open("./Workshop/chart/{}.png".format(filename),'rb') as file:
        binarydata = file.read()
        byte=bytearray(binarydata)
        return binarydata.hex()


true=0
while true ==0:
    symbols=mt.symbols_get()
    posit=[]
    negit=[]
    negval=[]
    posval=[]
    imlec.execute('''DBCC CHECKIDENT ('dramatikdegisim', RESEED,0)''')
    imlec.execute('''DELETE FROM dbo.dramatikdegisim''')
    imlec.commit()
    print(len(symbols))
    counter=0
    negc=0

    posc=0
    for s in symbols:
        if counter==95:
            break
        else:
            pos=pd.DataFrame(mt.copy_rates_from(s.name,mt.TIMEFRAME_H1,datetime.now(),2))
            if pos['close'][1]>pos['low'][0] and pos['close'][1]<pos['high'][0]:
                pass
            elif (pos['close'][1]-pos['high'][0])> (pos['low'][0]-pos['close'][1]):  
                value=(pos['close'][1]-pos['high'][0])/pos['high'][0]*100
                

                posval.append(value)
                posit.append(s.name)            
                
                
                posc+=1

            else:
                value=-(pos['low'][0]-pos['close'][1])/pos['low'][0]*100
                negval.append(value)
                negit.append(s.name)
                negc+=1
        counter+=1
    #Conver Dataframes
    negit=pd.DataFrame(negit)
    negval=pd.DataFrame(negval)
    posit=pd.DataFrame(posit)
    posval=pd.DataFrame(posval)
    #Concat to dataframes
    dusus=pd.concat([negit,negval],axis=1)
    artis=pd.concat([posit,posval],axis=1)
    #Columns Rename
    dusus.columns=['symbol','value']
    artis.columns=['symbol','value']

    artis=artis.sort_values(by='value',ascending=False)
    dusus=dusus.sort_values(by='value')
    artis=artis.reset_index(drop=True)
    dusus=dusus.reset_index(drop=True)
    print(artis,dusus)
    for i in range(0,20):
        if i >9:
            negframe=pd.DataFrame(mt.copy_rates_from(dusus['symbol'][i-10],mt.TIMEFRAME_M5,datetime.now(),20))

            figneg, axneg=plt.subplots()
            axneg.set_xticks([])
            axneg.set_yticks([])
            axneg.grid(False)
            axneg.plot(negframe['close'],color='#d74e65',linewidth=4.0)
        
            Canvasneg=FigureCanvas(figneg)
            Canvasneg.draw()

            width, height = figneg.get_size_inches() * figneg.get_dpi() 
            negimage = np.frombuffer(Canvasneg.tostring_rgb(), dtype='uint8').reshape(int(height),int(width),3)
            
            negcropim= negimage[38:250,60:382]
            #close windows;
            plt.close(figneg)
            #Image processing
            im = Image.fromarray(negimage)
            im=im.resize((212,90))
            im=im.crop((30,12,190,80))

            im.save("./Workshop/chart/{}.png".format(i))
            #date 
            dateneg = datetime.now()
            dateneg = dateneg.strftime('%Y-%m-%d %H:%M:%S')
            imlec.execute('''INSERT INTO dbo.dramatikdegisim VALUES ('{}',{},CONVERT(varbinary(max),'{}',2),'{}','{}')'''.format(dusus['symbol'][i-10],dusus['value'][i-10],convertToBin(i),"Negative",dateneg))
            imlec.commit()


        #--------------------------------------------------------------------------------------------#
        else:
            posframe=pd.DataFrame(mt.copy_rates_from(artis['symbol'][i],mt.TIMEFRAME_M5,datetime.now(),20))
        
        
            figpos, axpos=plt.subplots()
            axpos.set_xticks([])
            axpos.set_yticks([])
            axpos.grid(False)

            axpos.plot(posframe['close'],color='#51c586',linewidth=4.0)
        
            Canvaspos=FigureCanvas(figpos)
            Canvaspos.draw()

            width, height = figpos.get_size_inches() * figpos.get_dpi() 
            posimage = np.frombuffer(Canvaspos.tostring_rgb(), dtype='uint8').reshape(int(height),int(width),3)
            plt.close(figpos)
            #Image processing
            im = Image.fromarray(posimage)
            im=im.resize((212,90))
            im=im.crop((30,12,190,80))
            
            im.save("./Workshop/chart/{}.png".format(i))
            datepos = datetime.now()
            datepos = datepos.strftime('%Y-%m-%d %H:%M:%S')
            imlec.execute('''INSERT INTO dbo.dramatikdegisim VALUES ('{}',{},CONVERT(varbinary(max),'{}',2),'{}','{}')'''.format(artis['symbol'][i],artis['value'][i],convertToBin(i),"Positive",datepos))
            imlec.commit()
            true=1
while True:
    symbols=mt.symbols_get()
    posit=[]
    negit=[]
    negval=[]
    posval=[]

    print(len(symbols))
    counter=0
    negc=0

    posc=0
    for s in symbols:
        if counter==95:
            break
        else:
            pos=pd.DataFrame(mt.copy_rates_from(s.name,mt.TIMEFRAME_H1,datetime.now(),2))
            if pos['close'][1]>pos['low'][0] and pos['close'][1]<pos['high'][0]:
                pass
            elif (pos['close'][1]-pos['high'][0])> (pos['low'][0]-pos['close'][1]):  
                value=(pos['close'][1]-pos['high'][0])/pos['high'][0]*100
                

                posval.append(value)
                posit.append(s.name)            
                
                
                posc+=1

            else:
                value=-(pos['low'][0]-pos['close'][1])/pos['low'][0]*100
                negval.append(value)
                negit.append(s.name)
                negc+=1
        counter+=1
    #Conver Dataframes
    negit=pd.DataFrame(negit)
    negval=pd.DataFrame(negval)
    posit=pd.DataFrame(posit)
    posval=pd.DataFrame(posval)
    #Concat to dataframes
    dusus=pd.concat([negit,negval],axis=1)
    artis=pd.concat([posit,posval],axis=1)
    #Columns Rename
    dusus.columns=['symbol','value']
    artis.columns=['symbol','value']

    artis=artis.sort_values(by='value',ascending=False)
    dusus=dusus.sort_values(by='value')

    artis=artis.reset_index(drop=True)
    dusus=dusus.reset_index(drop=True)
    
    for i in range(0,20):
        if i >9:
            negframe=pd.DataFrame(mt.copy_rates_from(dusus['symbol'][i-10],mt.TIMEFRAME_M5,datetime.now(),20))

            figneg, axneg=plt.subplots()
            axneg.set_xticks([])
            axneg.set_yticks([])
            axneg.grid(False)
            axneg.plot(negframe['close'],color='#d74e65',linewidth=4.0)
        
            Canvasneg=FigureCanvas(figneg)
            Canvasneg.draw()

            width, height = figneg.get_size_inches() * figneg.get_dpi() 
            negimage = np.frombuffer(Canvasneg.tostring_rgb(), dtype='uint8').reshape(int(height),int(width),3)
            
            #negcropim= negimage[38:250,60:382]
            #close windows;
            plt.close(figneg)
            im = Image.fromarray(negimage)
            
            im=im.resize((212,90))
            im=im.crop((30,12,190,80))
            im.save("./Workshop/chart/{}.png".format(i))
            #date 
            dateneg = datetime.now()
            dateneg = dateneg.strftime('%Y-%m-%d %H:%M:%S')
            imlec.execute('''UPDATE dbo.dramatikdegisim SET symbol= '{}',change= {},image= CONVERT(varbinary(max),'{}',2),update_date= '{}' WHERE id={}'''.format(dusus['symbol'][i-10],dusus['value'][i-10],convertToBin(i),dateneg,(i+1)))
            imlec.commit()

        #--------------------------------------------------------------------------------------------#
        else:
            posframe=pd.DataFrame(mt.copy_rates_from(artis['symbol'][i],mt.TIMEFRAME_M5,datetime.now(),20))
        
        
            figpos, axpos=plt.subplots()
            axpos.set_xticks([])
            axpos.set_yticks([])
            axpos.grid(False)

            axpos.plot(posframe['close'],color='#51c586',linewidth=4.0)
        
            Canvaspos=FigureCanvas(figpos)
            Canvaspos.draw()

            width, height = figpos.get_size_inches() * figpos.get_dpi() 
            posimage = np.frombuffer(Canvaspos.tostring_rgb(), dtype='uint8').reshape(int(height),int(width),3)
            plt.close(figpos)
            #poscropim= posimage[38:250,60:382]
            im = Image.fromarray(posimage)
            im=im.resize((212,90))
            im=im.crop((30,12,190,80))

            im.save("./Workshop/chart/{}.png".format(i))
            datepos = datetime.now()
            datepos = datepos.strftime('%Y-%m-%d %H:%M:%S')
            imlec.execute('''UPDATE dbo.dramatikdegisim SET symbol= '{}',change= {},image= CONVERT(varbinary(max),'{}',2),update_date= '{}' WHERE id={}'''.format(artis['symbol'][i],artis['value'][i],convertToBin(i),datepos,(i+1)))
            imlec.commit()
    sleep(1800)
