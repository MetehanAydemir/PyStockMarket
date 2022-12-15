import pypyodbc as odbc
import base64
from datetime import datetime
from time import sleep


#Sql connection and query
conn = odbc.connect("DRIVER={SQL Server};SERVER=**********\MSSQLSERVER2014;UID=adminfx ;PWD=*****; DATABASE=db_fxhaber;'Trusted_Connection=yes;")

imlec.execute('SELECT* FROM dbo.Chart_Images')
kullanicilar = imlec.fetchall()
for i in kullanicilar:
    print(i)
    
def convertToBin(filename):
    #Convert digital data to binary format
    with open("C:/Users/Admin/AppData/Roaming/MetaQuotes/Terminal/D0E8209F77C8CF37AD8BF550E51FF075/MQL5/Files/"+filename,'rb') as file:
        binarydata = file.read()
        byte=bytearray(binarydata)
        return byte.hex()
        

def convertToBase(filename):
    #Convert digital data to base64 format
    with open("C:/Users/Admin/AppData/Roaming/MetaQuotes/Terminal/D0E8209F77C8CF37AD8BF550E51FF075/MQL5/Files/"+filename, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
        return encoded_string.decode("utf-8")
    
liste=['AUDUSD.png','EURJPY.png','EURTRY.png','EURUSD.png','GBPJPY.png','GBPUSD.png','USDJPY.png','USDTRY.png','XAGUSD.png','XAUUSD.png']
pair=['AUDUSD','EURJPY','EURTRY','EURUSD','GBPJPY','GBPUSD','USDJPY','USDTRY','XAGUSD','XAUUSD']

while True:
    counter = 0 
    for symbol in liste:
        print(symbol)
    
        date = datetime.now()
        date = date.strftime('%Y-%m-%d %H:%M:%S')
        #dbo.Chart_Images
        imlec.execute('''UPDATE dbo.Chart_Images SET Dosya=CONVERT(varbinary(max),'{}',2) ,Update_Date='{}' WHERE Pair='{}' '''.format(convertToBin(symbol),date,pair[counter]))
        imlec.commit() 
        counter+=1
    sleep(1800)
