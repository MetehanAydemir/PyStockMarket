from tkinter import *

import psutil    
import os
import time

class controller:
    
    def __init__(self,master):
        self.frame= Frame(master)
        self.frame.pack()
                
        #---------isiHaritasi---------#        
        self.labelisi=Label(self.frame,text="Isı Haritasi")
        self.labelisi.grid(row=0,column=0, padx=10, pady=10)
        
        self.isiButton=Button(self.frame,text="Çalıştır", command=self.isirun)
        self.isiButton.grid(row=0,column=5)
        
        self.stateisi =Label(self.frame,bg='white',width=8,height=3)
        self.stateisi.grid(row=0,column=3, padx=10, pady=10)
        
        #---------bigtable---------#        
        self.labelbigtable=Label(self.frame,text="Big Table")
        self.labelbigtable.grid(row=1,column=0, padx=10, pady=10)
        
        self.bigtableButton=Button(self.frame,text="Çalıştır", command=self.bigrun)
        self.bigtableButton.grid(row=1,column=5)
        
        self.statebigtable =Label(self.frame,bg='white',width=8,height=3)
        self.statebigtable.grid(row=1,column=3, padx=10, pady=10)
        
        #---------Correlation---------#        
        self.labelCorrelation=Label(self.frame,text="Correlation")
        self.labelCorrelation.grid(row=2,column=0, padx=10, pady=10)
        
        self.CorrelationButton=Button(self.frame,text="Çalıştır", command=self.Corrun)
        self.CorrelationButton.grid(row=2,column=5)
        
        self.stateCorrelation =Label(self.frame,bg='white',width=8,height=3)
        self.stateCorrelation.grid(row=2,column=3, padx=10, pady=10)
        
        #---------Correlation Table---------#        
        self.labelCorrelationtable=Label(self.frame,text="Correlation Table")
        self.labelCorrelationtable.grid(row=3,column=0, padx=10, pady=10)
        
        self.CorrelationtableButton=Button(self.frame,text="Çalıştır", command=self.CorTabrun)
        self.CorrelationtableButton.grid(row=3,column=5)
        
        self.stateCorrelationtable =Label(self.frame,bg='white',width=8,height=3)
        self.stateCorrelationtable.grid(row=3,column=3, padx=10, pady=10)
        
        #---------Dramatikler---------#        
        self.labelDramatikler=Label(self.frame,text="Dramatikler")
        self.labelDramatikler.grid(row=4,column=0, padx=10, pady=10)
        
        self.DramatiklerButton=Button(self.frame,text="Çalıştır", command=self.Dramarun)
        self.DramatiklerButton.grid(row=4,column=5)
        
        self.stateDramatikler =Label(self.frame,bg='white',width=8,height=3)
        self.stateDramatikler.grid(row=4,column=3, padx=10, pady=10)
        
        #---------Live_price---------#        
        self.labelLive_price=Label(self.frame,text="Live price")
        self.labelLive_price.grid(row=5,column=0, padx=10, pady=10)
        
        self.Live_priceButton=Button(self.frame,text="Çalıştır", command=self.Liverun)
        self.Live_priceButton.grid(row=5,column=5)
        
        self.stateLive_price =Label(self.frame,bg='white',width=8,height=3)
        self.stateLive_price.grid(row=5,column=3, padx=10, pady=10)
        
        #---------Pricechannel---------#        
        self.labelPricechannel=Label(self.frame,text="Price channel")
        self.labelPricechannel.grid(row=6,column=0, padx=10, pady=10)
        
        self.PricechannelButton=Button(self.frame,text="Çalıştır", command=self.Pricerun)
        self.PricechannelButton.grid(row=6,column=5)
        
        self.statePricechannel =Label(self.frame,bg='white',width=8,height=3)
        self.statePricechannel.grid(row=6,column=3, padx=10, pady=10)
        
##-------------------Run Functions-----------------##
    def isirun(self):
      
        #---------isiHaritasi---------#
        isihartasi="C:/Users/Admin/Documents/Fx/dist/isiharitasi/isiharitasi.exe"
        os.startfile(isihartasi)                        
    def bigrun(self):
      
        #---------Bigtable---------#
        Bigtable="C:/Users/Admin/Documents/Fx/dist/isiharitasi/isiharitasi.exe"
        os.startfile(Bigtable)
    def Corrun(self):
      
        #---------Correlation---------#
        Correlation="C:/Users/Admin/Documents/Fx/dist/isiharitasi/isiharitasi.exe"
        os.startfile(Correlation)

    def CorTabrun(self):
      
        #---------Correlation---------#
        CorrelationTable="C:/Users/Admin/Documents/Fx/dist/isiharitasi/isiharitasi.exe"
        os.startfile(CorrelationTable)
    def Dramarun(self):
      
        #---------Dramatikler---------#
        Dramatikler="C:/Users/Admin/Documents/Fx/dist/isiharitasi/isiharitasi.exe"
        os.startfile(Dramatikler)
        
    def Liverun(self):
      
        #--------Live_price---------#
        Live_price="C:/Users/Admin/Documents/Fx/dist/isiharitasi/isiharitasi.exe"
        os.startfile(Live_price)
    
    def Pricerun(self):
      
        #--------Live_price---------#
        Pricechannel="C:/Users/Admin/Documents/Fx/dist/isiharitasi/isiharitasi.exe"
        os.startfile(Pricechannel)
        
    def state(self):
        #---------isiHaritasi---------#
        isiharitasicheck="isiharitasi.exe" in (p.name() for p in psutil.process_iter())
        
        if isiharitasicheck is True:
            filee="green"
        else:
            filee="white"
            try:
                self.Pricerun()
            except:
                pass
                
        
        self.stateisi.destroy()
        self.stateisi =Label(self.frame,bg=filee,width=10,height=3)
        self.stateisi.grid(row=0,column=3, padx=10, pady=10)
        
     
        #---------bigtable---------#
        bigtablecheck="bigtable.exe" in (p.name() for p in psutil.process_iter())
        
        if bigtablecheck is True:
            filee="green"
        else:
            filee="white"
       
        
        self.statebigtable.destroy()
        self.statebigtable =Label(self.frame,bg=filee,width=10,height=3)
        self.statebigtable.grid(row=1,column=3, padx=10, pady=10)
        
        #---------Correlation---------#
        Correlation="Correlation.exe" in (p.name() for p in psutil.process_iter())
        
        if Correlation is True:
            filee="green"
        else:
            filee="white"
       
        
        self.stateCorrelation.destroy()
        self.stateCorrelation =Label(self.frame,bg=filee,width=10,height=3)
        self.stateCorrelation.grid(row=2,column=3, padx=10, pady=10)
        
        #---------Correlationtable---------#
        Correlationtable="Correlation.exe" in (p.name() for p in psutil.process_iter())
        
        if Correlationtable is True:
            filee="green"
        else:
            filee="white"
       
        
        self.stateCorrelationtable.destroy()
        self.stateCorrelationtable =Label(self.frame,bg=filee,width=10,height=3)
        self.stateCorrelationtable.grid(row=3,column=3, padx=10, pady=10)
        
        #---------Dramatikler---------#
        Dramatikler="Dramatikler.exe" in (p.name() for p in psutil.process_iter())
        
        if Dramatikler is True:
            filee="green"
        else:
            filee="white"
       
        
        self.stateDramatikler.destroy()
        self.stateDramatikler =Label(self.frame,bg=filee,width=10,height=3)
        self.stateDramatikler.grid(row=4,column=3, padx=10, pady=10)
        
        #---------Live_price---------#
        Live_price="Live_price.exe" in (p.name() for p in psutil.process_iter())
        
        if Live_price is True:
            filee="green"
        else:
            filee="white"
       
        
        self.stateLive_price.destroy()
        self.stateLive_price =Label(self.frame,bg=filee,width=10,height=3)
        self.stateLive_price.grid(row=5,column=3, padx=10, pady=10)
        
        #---------Pricechannel---------#
        Pricechannel="Pricechannel.exe" in (p.name() for p in psutil.process_iter())
        
        if Pricechannel is True:
            filee="green"
        else:
            filee="white"

        
        self.statePricechannel.destroy()
        self.statePricechannel =Label(self.frame,bg=filee,width=10,height=3)
        self.statePricechannel.grid(row=6,column=3, padx=10, pady=10)
        
        
root =Tk()
b= controller(root)

while True:
    b.state()    
    
    root.update_idletasks()
    root.update()
    time.sleep(0.01)
