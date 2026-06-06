import pandas as pd
import numpy as np


def run_backtest(df : pd.DataFrame, initial_capital : int = 1000000, risk_per_trade = 0.1):
    df = df.copy()
    cash = initial_capital
    position = 0
    entry_price = None
    equity_curve = []
    df["next_open"] = df["Open"].shift(-1)
    portfolio_value = 0
    for i,row in df.iterrows():
        
        
        if((row["entry_signal"] == 1) and (position == 0) and (row["next_open"] > 0)):
            portfolio_value = cash + (position * row["Close"])
            equity_curve.append({"date" : i , "portfolio_value" : portfolio_value})
            shares = row['unit_size']*cash*risk_per_trade
            cost = shares * row['next_open']
            
            if(cost > cash): continue
            cash = cash-cost
            position = shares
            entry_price = row["next_open"]
            
            
        if((row["exit_signal"] == 1) and (position != 0)):
            portfolio_value = cash + (position * row["Close"])
            equity_curve.append({"date" : i , "portfolio_value" : portfolio_value})
            cash += position * row["next_open"]
            position = 0
            entry_price = None
            
    return pd.DataFrame(equity_curve).set_index("date")




def get_trades(df : pd.DataFrame):
    
    df = df.copy()
    trades = []
    entry_price = 0
    entry_date = 0
    shares = 0
    df["next_open"] = df["Open"].shift(-1)
    
    for i,row in df.iterrows():
        
        if((shares == 0) and (row["entry_signal"] == 1)):
            entry_price = row["next_open"]
            entry_date = i 
            shares = row["unit_size"]*1000000
            
        if((shares != 0) and (row["exit_signal"] == 1)):
            exit_price = row["next_open"]
            pnl = (exit_price - entry_price) * shares
            trades.append({"entry_date" : entry_date, "exit_date" : i, 
                           "entry_price" : entry_price,"exit_price" : exit_price,
                           "pnl" : pnl})
            entry_price = 0
            entry_date = 0
            shares = 0
            
    return pd.DataFrame(trades)
    