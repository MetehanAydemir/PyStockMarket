int Max_candles = 150;
//Pivot Text
MqlRates Rateh1[];
//Pivot
MqlRates Rates[];

void OnInit()
  {
//--- Otomatik kaydırılmayı devre dışı bırak
   ChartSetInteger(0,CHART_AUTOSCROLL,false);
//--- Çizelgenin sağ kıyısının kaydırılmasını ayarla
   ChartSetInteger(0,CHART_SHIFT,true);
//--- Mum çizelgesini göster
   ChartSetInteger(0,CHART_MODE,CHART_CANDLES);
   
   ChartSetInteger(0,CHART_COLOR_GRID,false);
   
   ChartSetInteger(0,CHART_SCALE,2);
   ChartSetDouble(0,CHART_SHIFT_SIZE,0.12);
   
   GenerateTrainingData();
   Print("Uzman Danışmanın hazırlanması tamamlandı");
   
  }
  double avg_close_inperiod(int start,int end){
      double values = 0;
      for (int i =start; i< end; i++) values +=Rateh1[i].close;
      return values/(end-start);
      
      }   
void OnTick()
  {

   
   
   int Candlesonchart=ChartGetInteger(0,CHART_FIRST_VISIBLE_BAR,0);
   double P;
   double R1;
   double R2;
   double S1;
   double S2;
   datetime TimeFrame;
   
   //Pivot point calculation

   ArraySetAsSeries(Rates,true);
   
   CopyRates(_Symbol,PERIOD_D1,0,2,Rates);
   
   P = ( Rates[1].close + Rates[1].open + Rates[1].low+Rates[1].high)/4;
   R1= (P+(P-Rates[1].low));
   R2= (P+(Rates[1].high-Rates[1].low));
   S1= (P-(Rates[1].high-P));
   S2= (P-(Rates[1].high-Rates[1].low));
   TimeFrame=(Rates[0].time+86400);
   
   //Pivot
   ObjectCreate(0,"P",OBJ_TREND,0,Rates[0].time,P,TimeFrame,P);
   ObjectSetInteger(0,"P",OBJPROP_COLOR,clrYellow);
   ObjectSetInteger(0,"P",OBJPROP_RAY_RIGHT,true); 
   //Resistance1
   ObjectCreate(0,"R1",OBJ_TREND,0,Rates[0].time,R1,TimeFrame,R1);
   ObjectSetInteger(0,"R1",OBJPROP_COLOR,clrAqua);
   ObjectSetInteger(0,"R1",OBJPROP_RAY_RIGHT,true); 
   //Resistance2
   ObjectCreate(0,"R2",OBJ_TREND,0,Rates[0].time,R2,TimeFrame,R2);
   ObjectSetInteger(0,"R2",OBJPROP_COLOR,clrRed);
   ObjectSetInteger(0,"R2",OBJPROP_RAY_RIGHT,true); 
   //Support1
   ObjectCreate(0,"S1",OBJ_TREND,0,Rates[0].time,S1,TimeFrame,S1);
   ObjectSetInteger(0,"S1",OBJPROP_COLOR,clrViolet);
   ObjectSetInteger(0,"S1",OBJPROP_RAY_RIGHT,true); 
   //Support2
   ObjectCreate(0,"S2",OBJ_TREND,0,Rates[0].time,S2,TimeFrame,S2);
   ObjectSetInteger(0,"S2",OBJPROP_COLOR,clrMagenta);
   ObjectSetInteger(0,"S2",OBJPROP_RAY_RIGHT,true); 
   
   
   
   //Pivot Texts
   
   datetime Textpos;
  
   ArraySetAsSeries(Rateh1,true);
   CopyRates(_Symbol,PERIOD_H1,0,Max_candles,Rateh1);
   Textpos=(Rateh1[0].time+3600);
   ObjectCreate(0,"PivotText",OBJ_TEXT,0,Textpos,P);
   ObjectSetString(0,"PivotText",OBJPROP_TEXT,"P");
   ObjectSetInteger(0,"PivotText",OBJPROP_FONTSIZE,12); 
   ObjectSetInteger(0,"PivotText",OBJPROP_COLOR,clrYellow); 
   ObjectSetInteger(0,"PivotText",OBJPROP_COLOR,clrYellow);  
   
   ObjectCreate(0,"S1Text",OBJ_TEXT,0,Textpos,S1);
   ObjectSetString(0,"S1Text",OBJPROP_TEXT,"S1");
   ObjectSetInteger(0,"S1Text",OBJPROP_FONTSIZE,12); 
   ObjectSetInteger(0,"S1Text",OBJPROP_COLOR,clrYellow); 
   ObjectSetInteger(0,"S1Text",OBJPROP_COLOR,clrYellow); 
   
   ObjectCreate(0,"S2Text",OBJ_TEXT,0,Textpos,S2);
   ObjectSetString(0,"S2Text",OBJPROP_TEXT,"S2");
   ObjectSetInteger(0,"S2Text",OBJPROP_FONTSIZE,12); 
   ObjectSetInteger(0,"S2Text",OBJPROP_COLOR,clrYellow); 
   ObjectSetInteger(0,"S2Text",OBJPROP_COLOR,clrYellow); 
   
   ObjectCreate(0,"R1Text",OBJ_TEXT,0,Textpos,R1);
   ObjectSetString(0,"R1Text",OBJPROP_TEXT,"R1");
   ObjectSetInteger(0,"R1Text",OBJPROP_FONTSIZE,12); 
   ObjectSetInteger(0,"R1Text",OBJPROP_COLOR,clrYellow); 
   ObjectSetInteger(0,"R1Text",OBJPROP_COLOR,clrYellow); 
   
   ObjectCreate(0,"R2Text",OBJ_TEXT,0,Textpos,R2);
   ObjectSetString(0,"R2Text",OBJPROP_TEXT,"R2");
   ObjectSetInteger(0,"R2Text",OBJPROP_FONTSIZE,12); 
   ObjectSetInteger(0,"R2Text",OBJPROP_COLOR,clrYellow); 
   ObjectSetInteger(0,"R2Text",OBJPROP_COLOR,clrYellow); 
   
   
 
   
   //Price Channel
    
   double High[];
   double Lowe[];
   
   long HighestF;
   long HighestS;
   long LowestF;
   CopyHigh(_Symbol,_Period,0,Max_candles,High);
   CopyLow(_Symbol,_Period,0,Max_candles,Lowe);
   ArraySetAsSeries(High,true);
   ArraySetAsSeries(Lowe,true);
   double avg_first = avg_close_inperiod(Max_candles/2,Max_candles);
   double avg_second= avg_close_inperiod(0,Max_candles/2);
   if(avg_first>avg_second)
     {

   HighestF= ArrayMaximum(High,(Max_candles/2),Max_candles);
   LowestF = ArrayMinimum(Lowe,((Max_candles/4)),(HighestF));
   HighestS= ArrayMaximum(High,0,LowestF);
     }
   else
     {
   HighestF= ArrayMaximum(High,(Max_candles/6),Max_candles/2);
   HighestS= ArrayMaximum(High,Max_candles/2,Max_candles);
   LowestF = ArrayMinimum(Lowe,(Max_candles/6),Max_candles);
     }
     

   MqlRates Priceinfo[];
   
  
   
   ArraySetAsSeries(Priceinfo,true);
   int Data =CopyRates(_Symbol,_Period,0,Max_candles,Priceinfo);
   ObjectDelete(_Symbol,"SimpleHigh");
   
   ObjectCreate(0,"SimpleHigh",OBJ_CHANNEL,0,Priceinfo[HighestF].time,Priceinfo[HighestF].high,Priceinfo[HighestS].time,Priceinfo[HighestS].high,Priceinfo[LowestF].time,Priceinfo[LowestF].low);
   ObjectSetDouble(0,"SimpleHigh",OBJPROP_DEVIATION,true);
   ObjectSetInteger(0,"SimpleHigh",OBJPROP_FILL,false);
   ObjectSetInteger(0,"SimpleHigh",OBJPROP_RAY_RIGHT,true); 
   ObjectSetInteger(0,"SimpleHigh",OBJPROP_RAY_LEFT,true); 
   ObjectSetInteger(0,"SimpleHigh",OBJPROP_COLOR,clrLime);
   ObjectSetInteger(0,"SimpleHigh",OBJPROP_WIDTH,2);
   
   ChartScreenShot(0,"Post",1050,660,ALIGN_CENTER);
   GenerateTrainingData();
  }
/*  void GenerateTrainingData()
  {
//--- Operation with the left chart edge

   for(int pos=16; pos<pictures; pos+=1)
     {
      //--- Scroll the chart to the left edge
      ChartNavigate(0,CHART_BEGIN,pos);

      //--- Give the user time to look at the new part of the chart
      Sleep(10);

      //--- Prepare a text to show on the chart and a file name
      string name = Symbol() + " " + IntegerToString(pos + 1) + ".PNG";

      //--- Save the chart screenshot in a file in the terminal_directory\MQL5\Files\
      if(ChartScreenShot(0,name,WIDTH,HEIGHT,ALIGN_LEFT))
        {
         Print("Screenshot saved as ",name);
         Comment(name);
        }

     }
  }*/
  
//+------------------------------------------------------------------+
void GenerateTrainingData(){
string name = Symbol() + " "  + ".PNG";

ChartScreenShot(0,name,1050,660,ALIGN_LEFT);}