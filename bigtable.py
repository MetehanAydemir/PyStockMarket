import MetaTrader5 as mt
from datetime import datetime
import datetime as dt
import pandas as pd 
import pypyodbc as odbc
import time 
import numpy as np

login =**********
Path='C:\\Program Files\\FinveoMNMT5Terminal\\terminal64.exe'
password ='**********'
server='FinveoMN-Live'
mt.initialize(Path)
mt.login(login,password,server)

conn = odbc.connect("DRIVER={SQL Server};SERVER=**********\MSSQLSERVER2014;UID=adminfx ;PWD=*****; DATABASE=db_fxhaber;'Trusted_Connection=yes;")

imlec = conn.cursor()
imlec.execute('SELECT* FROM dbo.live_prices')
kullanicilar = imlec.fetchall()
for i in kullanicilar:
    print(i)


##-------------MA-------------
def ma(period, symbol,time_interval=mt.TIMEFRAME_D1):
    pos=pd.DataFrame(mt.copy_rates_from(symbol,time_interval,datetime.now(),(period+1)))
    pos['low']=pos['close'].rolling(period).sum()/period
    if pos['close'][period]< pos['low'][period-1]:    
        order="SELL"
    else:
        order="BUY"
    return pos['low'][period-1],order
##-------------RSI-------------
def avarage(obje):
    summ=0
    for s in range(len(obje)):
        summ=summ +obje[s]
    avg = summ/len(obje)
    return avg


def RSI(symbol,period=16,time_interval=mt.TIMEFRAME_D1):
    posit=[0]*14
    negit=[0]*14
    pos=pd.DataFrame(mt.copy_rates_from(symbol,time_interval,datetime.now(),(period)))
    pos['tick']=pos['close'].pct_change()
    pos['tick']=pos['tick'].dropna()
    counter1 =0
    counter2 =0 
    for s in range((len(pos['tick'])-1)):
        if pos['tick'][s] <0:
            negit[counter1]=pos['tick'][s]
            counter1+=1
        elif pos['tick'][s] >0:
            posit[counter2]=pos['tick'][s]
            counter2+=1
    avg_pos=avarage(posit)
    avg_neg=avarage(negit)
    RS=avg_pos/-avg_neg
    RSI=100-(100/(RS+1))
    if pos['low'][period-1]<0:
        NRS=-avg_pos/(((avg_neg*13) + pos['tick'][period-1])/14)
        NRSI = 100-(100/(NRS+1))
    else:
        NRS=(((avg_pos*13) + pos['tick'][period-1])/14)/-avg_neg
        NRSI = 100-(100/(1+NRS))
    
    
    
    if NRSI<30 and  RSI<NRSI:
        order="BUY"
    elif NRSI>70 and RSI>NRSI:
        order="SELL"
    else:
        order="NEUTRAL"
    return NRSI,order     
    
##--------MACD-------------

def MACD(symbol,period=100,time_interval=mt.TIMEFRAME_D1):
    global order
    pos=pd.DataFrame(mt.copy_rates_from(symbol,time_interval,datetime.now(),(period)))
    data=pd.DataFrame(mt.copy_rates_from(symbol,time_interval,datetime.now(),(period)))
    pos=pos['close']
    pos=pos.iloc[0:12].mean()
    exp1 = data['close'].ewm(span=12, adjust=False).mean()
    exp2 = data['close'].ewm(span=26, adjust=False).mean()
    data['MACD'] = exp1 - exp2
    data['Signal line'] = data['MACD'].ewm(span=9, adjust=False).mean()
    data=data[['close','MACD','Signal line']]
    signal = data['Signal line']
    macd = data['MACD']
    if macd[period-1]>0 and signal[period-1]<macd[period-1]:
        for i in range(1,8):
            if macd[period-i]<0:
                order="BUY"
            else: 
                order="NEUTRAL"
    elif macd[period-1]<0 and signal[period-1]>macd[period-1]:
        for i in range(1,8):
            if macd[period-i]>0:
                order="SELL"
            else: 
                order="NEUTRAL"
                
    else:
        order="NEUTRAL"
    
    return macd[period-1],order

##-------------ADX-------------

def ADX(symbol,period=100, interval: int=14,time_interval=mt.TIMEFRAME_D1):
    df=pd.DataFrame(mt.copy_rates_from(symbol,time_interval,datetime.now(),(period)))
    df['-DM'] = df['low'].shift(1) - df['low']
    df['+DM'] = df['high'] - df['high'].shift(1)
    
    df['+DM'] = np.where((df['+DM'] > df['-DM']) & (df['+DM']>0), df['+DM'], 0.0)
    df['-DM'] = np.where((df['-DM'] > df['+DM']) & (df['-DM']>0), df['-DM'], 0.0)
    
    df['TR_TMP1'] = df['high'] - df['low']
    df['TR_TMP2'] = np.abs(df['high'] - df['close'].shift(1))
    df['TR_TMP3'] = np.abs(df['low'] - df['close'].shift(1))
    df['TR'] = df[['TR_TMP1', 'TR_TMP2', 'TR_TMP3']].max(axis=1)
    
    df['TR'+str(interval)] = df['TR'].rolling(interval).sum()
    df['+DMI'+str(interval)] = df['+DM'].rolling(interval).sum()
    df['-DMI'+str(interval)] = df['-DM'].rolling(interval).sum()
    
    df['+DI'+str(interval)] = df['+DMI'+str(interval)] /   df['TR'+str(interval)]*100
    df['-DI'+str(interval)] = df['-DMI'+str(interval)] / df['TR'+str(interval)]*100
    df['DI'+str(interval)+'-'] = abs(df['+DI'+str(interval)] - df['-DI'+str(interval)])
    df['DI'+str(interval)] = df['+DI'+str(interval)] + df['-DI'+str(interval)]
    df['DX'] = (df['DI'+str(interval)+'-'] / df['DI'+str(interval)])*100
    
    df['ADX'+str(interval)] = df['DX'].rolling(interval).mean()
    df['ADX'+str(interval)] =   df['ADX'+str(interval)].fillna(df['ADX'+str(interval)].mean())
    
    del df['TR_TMP1'], df['TR_TMP2'], df['TR_TMP3'], df['TR'], df['TR'+str(interval)]
    del df['+DMI'+str(interval)], df['DI'+str(interval)+'-']
    del df['DI'+str(interval)], df['-DMI'+str(interval)]
    del df['+DI'+str(interval)], df['-DI'+str(interval)]
    del df['DX']
    del df['tick_volume']
    adxorder="NEUTRAL"
    return df['ADX14'][99],adxorder    
##------------STOCH---------------
def STOCH(symbol,period=17,time_interval=mt.TIMEFRAME_D1):
    
    pos=pd.DataFrame(mt.copy_rates_from(symbol,time_interval,datetime.now(),(period)))
    close=pos['close']
    lowest=pos['low'].rolling(14).min()
    highest=pos['high'].rolling(14).max()
    KK=(close-lowest)/(highest-lowest)*100
    DD=KK.rolling(3).mean()
    if KK[period-1]<80 and (KK[period-1] <DD[period-1]):
        for i in range(1,4):
            if KK[period-i]>80:
                order ="BUY"
            else:
                order="NEUTRAL"
    elif KK[period-1]>20 and KK[period-1] >DD[period-1]:
        
        for i in range(1,4):
            if KK[period-i]<20:
                order ="SELL"
            else:
                order="NEUTRAL"
    else:
        
        order = "NEUTRAL"
    return KK[period-1],order
##-------------Alligator------------
def Alligator(symbol,period=25,time_interval=mt.TIMEFRAME_D1):
    pos=pd.DataFrame(mt.copy_rates_from(symbol,time_interval,datetime.now(),(period)))
    values=[13,8],[8,5],[5,3]
    SMMA=[0]*3
    counter=0
    for p,s in values:
        sma1=((pos['high']+pos['low'])/2).rolling(p).mean()
        prevsum=sma1.shift(1).rolling(s).mean()*s
        SMMA[counter]=(prevsum-sma1.shift(1).rolling(s).mean()+(pos['high']+pos['low']).div(2))/s
        counter+=1
    if SMMA[1][period-1]>SMMA[0][period-1] and SMMA[2][period-1]>SMMA[1][period-1]:
        for counter in range(1,6):
            if SMMA[1][period-counter]< SMMA[0][period-counter]:
                Order='BUY'
            else: Order='NEUTRAL'
    elif SMMA[1][period-1]<SMMA[0][period-1] and SMMA[2][period-1]<SMMA[1][period-1]:
        for counter in range(1,6):
            if SMMA[1][period-counter]> SMMA[0][period-counter]:
                Order='SELL'
            else: Order='NEUTRAL'
    else:
        Order='NEUTRAL'
    return SMMA[0][period-1],Order
##-----------CCI------------------

def CCI(symbol,period=100,time_interval=mt.TIMEFRAME_D1):
    df=pd.DataFrame(mt.copy_rates_from(symbol,time_interval,datetime.now(),(period)))
    df['TP'] = (df['high'] + df['low'] + df['close']) / 3 
    df['sma'] = df['TP'].rolling(20).mean()
    df['mad'] = df['TP'].rolling(20).apply(lambda x: pd.Series(x).mad())
    df['CCI'] = (df['TP'] - df['sma']) / (0.015 * df['mad']) 
    CCI=df['CCI']
    if CCI[period-1]<100:
        for i in range(1,8):
            if CCI[period-i]>100:
                ccorder="BUY"
            else:
                ccorder="NEUTRAL"
    elif CCI[period-1]>-100:
        for i in range(1,8):
            if CCI[period-i]<-100:
                ccorder="SELL"
            else:
                ccorder="NEUTRAL"
    else:
        ccorder = "NEUTRAL"
    return CCI[99],ccorder
##-------------Trend Following-------
def Trend(symbol,time_interval,period=80):
    pos=pd.DataFrame(mt.copy_rates_from(symbol,time_interval,datetime.now(),(period)))
    close=pos['close']
    ema=close.rolling(int(period/2)).mean()
    up=0
    down=0
    for p in range(len(close)):
        if close[p]>ema[p]:
            up+=1
        elif close[p]<ema[p]:
            down+=1
    if up>14:
        trend='UP'
    elif down>14:
        trend='DOWN'
    else:
        trend='NEUTRAL'
         
    return trend

##--------------Pivot---------------
def Pivot(symbol,time_interval,period=1):
    pos=pd.DataFrame(mt.copy_rates_from(symbol,time_interval,(datetime.now()-dt.timedelta(days=1)),(period)))
    P=(pos['high']+pos['close']+pos['low'])/3
    R1=P+(P-pos['low'])
    S1=P-(pos['high']-P)
    R2=P+(pos['high']-pos['low'])
    S2=P-(pos['high']-pos['low'])
    total=[P,R1,R2,S1,S2]
    return total


def technicalsig(symbols,time_interval):
    #prelist
    orders=["Buy", "Neutral", "Neutral", "Buy", "Neutral"]
    MA=["Buy", "Neutral", "Neutral", "Buy", "Neutral"]
    #Counters
    indis=0
    movs=0
    #Time format
    if time_interval==mt.TIMEFRAME_D1:
        time='D1'
    elif time_interval==mt.TIMEFRAME_H4:
        time='H4'
    elif time_interval==mt.TIMEFRAME_H1:
        time='H1'
    else:
        time='M15'
    #Indicators
    rsi,orders[0]=RSI(symbols,time_interval=time_interval)
    stoch,orders[1]=STOCH(symbols,time_interval=time_interval)
    macd,orders[2]=MACD(symbols,time_interval=time_interval)
    cci,orders[3]=CCI(symbols,time_interval=time_interval)
    gator,orders[4]=Alligator(symbols,time_interval=time_interval)
    
    
    
    for orde in orders:
        if orde == "BUY":
            indis+=1 
        elif orde == "SELL":
            indis-=1
    if indis==4:
        indisignal="STRONG BUY"
    elif indis==(-4):
        indisignal="STRONG SELL"
    elif indis==0:
        indisignal="NEUTRAL"
    elif indis>0:
        indisignal="BUY"
    else:
        indisignal="SELL"
           
    #Momentium Avarage
    ma10,MA[0]=ma(10,symbols,time_interval=time_interval)
    ma20,MA[1]=ma(20,symbols,time_interval=time_interval)
    ma50,MA[2]=ma(50,symbols,time_interval=time_interval)
    ma100,MA[3]=ma(100,symbols,time_interval=time_interval)
    ma200,MA[4]=ma(200,symbols,time_interval=time_interval)
                
    for ordem in MA:
        if ordem == "BUY":
            movs+=1 
        elif ordem == "SELL":
            movs-=1

    if movs>=4:
        masignal="STRONG BUY"
    elif movs<=(-4):
        masignal="STRONG SELL"
    elif movs==0:
        masignal="NEUTRAL"
    elif movs>0:
        masignal="BUY"
    else:
        masignal="SELL"

    trend=Trend(symbols,time_interval)            
               
    
    return symbols,MA,masignal,orders,indisignal,trend,time

def technicalvalue(symbols,time_interval):
    #prelist
    orders=["Buy", "Neutral", "Neutral", "Buy", "Neutral"]
    MA=["Buy", "Neutral", "Neutral", "Buy", "Neutral"]
    #Counters
    indis=0
    movs=0
    #Time format
    if time_interval==mt.TIMEFRAME_D1:
        time='D1'
    elif time_interval==mt.TIMEFRAME_H4:
        time='H4'
    elif time_interval==mt.TIMEFRAME_H1:
        time='H1'
    else:
        time='M15'
    #Indicators
    orders[0],rsi=RSI(symbols,time_interval=time_interval)
    orders[1],stoch=STOCH(symbols,time_interval=time_interval)
    orders[2],macd=MACD(symbols,time_interval=time_interval)
    orders[3],cci=CCI(symbols,time_interval=time_interval)
    orders[4],gator=Alligator(symbols,time_interval=time_interval)

    #Momentium Avarage
    MA[0],ma10=ma(10,symbols,time_interval=time_interval)
    MA[1],ma20=ma(20,symbols,time_interval=time_interval)
    MA[2],ma50=ma(50,symbols,time_interval=time_interval)
    MA[3],ma100=ma(100,symbols,time_interval=time_interval)
    MA[4],ma200=ma(200,symbols,time_interval=time_interval)  
    
    #Pivot
    pivot=Pivot(symbols,time_interval)
    return symbols,MA,orders,pivot,time

symbols=['AUDUSD','EURJPY','EURTRY','EURUSD','GBPJPY','GBPUSD','USDJPY',
         'USDTRY','CRUDE_U','XAGUSD','XAUUSD']
timess=[mt.TIMEFRAME_D1,mt.TIMEFRAME_H4,mt.TIMEFRAME_H1,mt.TIMEFRAME_M15]

First=1
while First==1:
#Indicators signal
    imlec.execute('''DELETE FROM dbo.technical_indicators''')                   
    imlec.commit()
    counterr=0
    for timer in timess:
        for symbol in symbols:
            
            date = datetime.now()
            date = date.strftime('%Y-%m-%d %H:%M:%S')
            parite,MA,masignal,orders,indisignal,trend,time=technicalsig(symbol,timer)
            imlec.execute('''INSERT INTO dbo.technical_indicators VALUES('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}')'''.format(counterr,parite,MA[0],MA[1],MA[2],MA[3],MA[4],masignal,
                                                                                                                                                                    orders[0], orders[1],orders[2],orders[3],orders[4],indisignal,trend,time,date))
            imlec.commit()
            counterr+=1
            
#Indicators Values        
    imlec.execute('''DELETE FROM dbo.technical_indicators_values''')                   
    imlec.commit()
    counter=0
    for timer in timess:
        for symbol in symbols:
        
            date = datetime.now()
            date = date.strftime('%Y-%m-%d %H:%M:%S')
            parite,MA,orders,pivot,time=technicalvalue(symbol,timer)
            imlec.execute('''INSERT INTO dbo.technical_indicators_values VALUES({},'{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}')'''.format(counter,parite,MA[0],MA[1],MA[2],MA[3],MA[4],
                                                                                                                                                                    orders[0], orders[1],orders[2],orders[3],orders[4],float(pivot[4]),float(pivot[3]),float(pivot[0]),float(pivot[1]),float(pivot[2]),time,date))
            imlec.commit()
            counter+=1
    First=0
Second=1
while Second==1:    
#Indicators signal
    counterr=0
    for timer in timess:
        for symbol in symbols:
            
            date = datetime.now()
            date = date.strftime('%Y-%m-%d %H:%M:%S')
            parite,MA,masignal,orders,indisignal,time=technicalsig(symbol,timer)
            imlec.execute('''UPDATE dbo.technical_indicators SET ma10='{}',ma20='{}',ma50='{}',ma100='{}',ma200='{}',ma_signal='{}',rsi='{}',stoch='{}',macd='{}',alligator='{}',cci='{}',indicator_signal='{}',updated_at='{}' WHERE id={} '''.format(MA[0],MA[1],MA[2],MA[3],MA[4],masignal,
                                                                                                                                                                                                                                            orders[0], orders[1],orders[2],orders[3],orders[4],indisignal,trend,date,counterr))
            imlec.commit()
            counterr+=1
#Indicators Values        
    counter=0
    for timer in timess:
        for symbol in symbols:
        
            date = datetime.now()
            date = date.strftime('%Y-%m-%d %H:%M:%S')
            parite,MA,orders,pivot,time=technicalvalue(symbol,timer)
            imlec.execute('''UPDATE dbo.technical_indicators_values SET ma10='{}',ma20='{}',ma50='{}',ma100='{}',ma200='{}',rsi='{}',stoch='{}',macd='{}',alligator='{}',cci='{}',s2='{}',s1='{}',[pivot]='{}',r1='{}',r2='{}',updated_at='{}' WHERE id={} '''.format(MA[0],MA[1],MA[2],MA[3],MA[4],
                                                                                                                                                                                                                                            orders[0], orders[1],orders[2],orders[3],orders[4],float(pivot[4]),float(pivot[3]),float(pivot[0]),float(pivot[1]),float(pivot[2]),date,counter))
            imlec.commit()
            counter+=1
    time.sleep(450)
    
