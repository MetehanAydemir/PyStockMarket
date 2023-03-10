#include <Trade/Trade.mqh>

input double Lots = 1;

CTrade trade;

int lastBreakout=0;

int OnInit()
  {
 Print("Merhaba sisteme girdiniz");
   return(INIT_SUCCEEDED);
  }
//+------------------------------------------------------------------+
//| Expert deinitialization function                                 |
//+------------------------------------------------------------------+
void OnDeinit(const int reason)
  {
 Print("Cikis basarili");
  }
//+------------------------------------------------------------------+
//| Expert tick function                                             |
//+------------------------------------------------------------------+
void OnTick()
  {
   double high =iHigh(_Symbol,PERIOD_CURRENT,1);
   high =NormalizeDouble(high,_Digits);
   
   double low =iLow(_Symbol,PERIOD_CURRENT,1);
   low = NormalizeDouble(low,_Digits);
   
   double bid =SymbolInfoDouble(_Symbol,SYMBOL_BID);
   
   if(lastBreakout <= 0 && bid > high){
      Print(__FUNCTION__," > Buy Signal...");
      lastBreakout =1;
      
    trade.Buy(Lots,_Symbol,0,low);
   }else if(lastBreakout >=0 && bid<low){
    Print(__FUNCTION__," > Sell Signal...");
    lastBreakout = -1;
    
    
    trade.Sell(Lots,_Symbol,0,high);
    
   }
   for(int i =PositionsTotal()-1;i>=0;i--){
      ulong posTicket = PositionGetTicket(i);
      CPositionInfo pos;
      if(pos.SelectByTicket(posTicket)){
         if(pos.PositionType()==POSITION_TYPE_BUY){
            if(low>pos.StopLoss()){
            trade.PositionModify(pos.Ticket(),low,pos.TakeProfit());}
         }else if(pos.PositionType()== POSITION_TYPE_SELL){
            if(high< pos.StopLoss()){
               trade.PositionModify(pos.Ticket(),high,pos.TakeProfit());}
         }
         }
   }
   
   Comment("\nBid",bid,"\nHigh",high,"\nLow",low);
  }
//+------------------------------------------------------------------+
