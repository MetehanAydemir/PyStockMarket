import talib
import MetaTrader5 as mt
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime
from datetime import date, timedelta
from plotly import io
import matplotlib.pyplot as plt
import matplotlib.dates as mpl_dates
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
imlec.execute('SELECT* FROM dbo.SicaklikH')
kullanicilar = imlec.fetchall()
for i in kullanicilar:
    print(i)

candle_names =[
    'CDLMARUBOZU',
    'CDLDOJI',
    'CDLHANGINGMAN',
    'CDLHAMMER']

def convertToBin(filename):
    #Convert digital data to binary format
    with open("C:/Users/MAPLE/Documents/Fx/candle/{}.png".format(filename),'rb') as file:
        binarydata = file.read()
        byte=bytearray(binarydata)
        return binarydata.hex()
#Reset         
imlec.execute('''DBCC CHECKIDENT ('Mumlar', RESEED,0)''')
imlec.execute('''DELETE FROM dbo.Mumlar''')
imlec.commit()
symbols=mt.symbols_get()
counter=0
period=15
print(len(symbols))

k=1
while k == 1:


    for symbol in symbols:
        
        if counter != 80:
            
            timeframe='D1'
            period=20
            pos = pd.DataFrame(mt.copy_rates_from_pos(symbol.name,mt.TIMEFRAME_D1,0,period))
            pos.time=pd.to_datetime(pos['time'],unit ='s')
            symbolname= "{}".format(symbol.name).replace(".eq","")
            #find missing dates
            alldays =set(pos.time[0]+timedelta(x) for x in range((pos.time[len(pos.time)-1]-pos.time[0]).days))
            missing=sorted(set(alldays)-set(pos.time))
            if len(alldays)<345 and symbol.name != "USDHKD":
                
                # create columns for each pattern
                for candle in candle_names:
                    if candle=='CDLMARUBOZU': candlename="MARUBOZU"
                    elif candle=='CDLDOJI':candlename= "DOJI"
                    elif candle=='CDLHANGINGMAN':candlename= "HANGINGMAN"
                    else:candlename= 'HAMMER'
                    # below is same as;
                    # pos["CDL3LINESTRIKE"] = talib.CDL3LINESTRIKE(op, hi, lo, cl)
                    pos[candle] = getattr(talib, candle)(pos.open, pos.high,pos.low, pos.close)
                    for count in range(period-2,period-1):
                        
                        if pos[candle][count]!=0:
                            fig = go.Figure(go.Candlestick(x=pos.time[period-10:period],
                                open=pos['open'][period-10:period],
                                high=pos['high'][period-10:period],
                                low=pos['low'][period-10:period],
                                close=pos['close'][period-10:period]))
                            fig.update_layout(height=400,width=400)
                            #For CHart Name
                            fig.add_annotation(x=pos.time[period-8], y=pos.high.max()*1.01,
                                                text=symbolname+", "+timeframe,
                                                showarrow=False,
                                                yshift=10,
                                                font=dict(family="MS UI Gothic",
                                                            size=20))
                            
                            fig.add_shape(type="rect",x0=pos.time[count]-timedelta(hours=12),y0=pos.low[count]*0.999,x1=pos.time[count]+timedelta(hours=12),y1=pos.high[count]*1.001)
                        
                            fig.update_xaxes(zerolinewidth=50)
                            fig.update_layout(xaxis_rangeslider_visible=False,plot_bgcolor="#212224",paper_bgcolor="#212224",
                                              font_color ="white" )
                            fig.update_xaxes(rangebreaks=[dict(values=missing)])
                        
                            #Add pointer for candle
                            fig.add_annotation(x=pos.time[count],y=(pos.high[count]*1.005), text= candlename,showarrow=False,arrowsize=1,arrowwidth=3, arrowcolor="blue",font=dict(size=15))
                            
                            #Grid option
                            fig.update_xaxes(showgrid=True,gridcolor='LightGray')
                            fig.update_yaxes(showgrid = True,gridcolor='LightGray')                        
                            
                            # Costumize line and fill colors 
                            cs=fig.data[0]
                            
                            cs.increasing.fillcolor = 'lime'
                            cs.increasing.line.color = 'black'
                            cs.decreasing.fillcolor = 'crimson'
                            cs.decreasing.line.color = 'black'
                            fig.write_image("C:/Users/MAPLE/Documents/Fx/candle/{}{}.png".format(candlename,symbolname))
                            imlec.execute('''INSERT INTO dbo.Mumlar VALUES ('{}','{}','{}',CONVERT(varbinary(max),'{}',2))'''.format(candlename,symbolname,timeframe,convertToBin(candlename+symbolname)))
                            imlec.commit()
                            
            counter+=1    
    k = 0
    time.sleep(6)

while True:
    symbols=mt.symbols_get()
    counter=0
    period=15
    print(datetime.now())
    for symbol in symbols:
        
        if counter != 80:
            
            timeframe='D1'
            period=20
            pos = pd.DataFrame(mt.copy_rates_from_pos(symbol.name,mt.TIMEFRAME_D1,0,period))
            pos.time=pd.to_datetime(pos['time'],unit ='s')
            symbolname= "{}".format(symbol.name).replace(".eq","")
            #find missing dates
            alldays =set(pos.time[0]+timedelta(x) for x in range((pos.time[len(pos.time)-1]-pos.time[0]).days))
            missing=sorted(set(alldays)-set(pos.time))
            if len(alldays)<345 and symbol.name != "USDHKD":
                
                # create columns for each pattern
                for candle in candle_names:
                    if candle=='CDLMARUBOZU': candlename="MARUBOZU"
                    elif candle=='CDLDOJI':candlename= "DOJI"
                    elif candle=='CDLHANGINGMAN':candlename= "HANGINGMAN"
                    else:candlename= 'HAMMER'
                    # below is same as;
                    # pos["CDL3LINESTRIKE"] = talib.CDL3LINESTRIKE(op, hi, lo, cl)
                    pos[candle] = getattr(talib, candle)(pos.open, pos.high,pos.low, pos.close)
                    for count in range(period-3,period-1):
                        
                        if pos[candle][count]!=0:
                            fig = go.Figure(go.Candlestick(x=pos.time[period-10:period],
                                open=pos['open'][period-10:period],
                                high=pos['high'][period-10:period],
                                low=pos['low'][period-10:period],
                                close=pos['close'][period-10:period]))
                            fig.update_layout(height=400,width=400)
                            #For CHart Name
                            fig.add_annotation(x=pos.time[period-8], y=pos.high.max()*1.01,
                                                text=symbolname+", "+timeframe,
                                                showarrow=False,
                                                yshift=10,
                                                font=dict(family="MS UI Gothic",
                                                            size=20))
                            
                            fig.add_shape(type="rect",x0=pos.time[count]-timedelta(hours=12),y0=pos.low[count]*0.999,x1=pos.time[count]+timedelta(hours=12),y1=pos.high[count]*1.001)
                        
                            fig.update_xaxes(zerolinewidth=50)
                            fig.update_layout(xaxis_rangeslider_visible=False,plot_bgcolor="#212224",paper_bgcolor="#212224",font_color="white")
                            fig.update_xaxes(rangebreaks=[dict(values=missing)])
                        
                            #Add pointer for candle
                            fig.add_annotation(x=pos.time[count],y=(pos.high[count]*1.005), text= candlename,showarrow=False,arrowsize=1,arrowwidth=3, arrowcolor="blue",font=dict(size=15))
                            
                            #Grid option
                            fig.update_xaxes(showgrid=True,gridcolor='LightGray')
                            fig.update_yaxes(showgrid = True,gridcolor='LightGray')
            
                            # Costumize line and fill colors 
                            cs=fig.data[0]
                            
                            cs.increasing.fillcolor = 'lime'
                            cs.increasing.line.color = 'black'
                            cs.decreasing.fillcolor = 'crimson'
                            cs.decreasing.line.color = 'black'
                            fig.write_image("C:/Users/MAPLE/Documents/Fx/candle/{}{}.png".format(candlename,symbolname))
                            imlec.execute('''UPDATE dbo.Mumlar SET image = CONVERT(varbinary(max),'{}',2)) WHERE  symbol = '{}' '''.format(convertToBin(candlename+symbolname),candlename))
                            imlec.commit()
            counter+=1  
    time.sleep(3600)
