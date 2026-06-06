import pandas as pd
import numpy as np


def compute_atr(df : pd.DataFrame, period : int = 20):
    high = df['High']
    low = df['Low']
    close = df['Close']
    # df = df.copy()
    prev_close = close.shift(1)
    
    first = high-low
    second = (high-prev_close).abs()
    third = (low-prev_close).abs()
    
    print(df.columns)
    tr = pd.concat([first,second,third],axis = 1).max(axis = 1)
    
    atr = tr.ewm(alpha = 1/period, adjust = False).mean()
    
    return atr
    
    
    
def compute_dochian(df : pd.DataFrame, period : int = 20):
    
    upper = df['High'].shift(1).rolling(period).max()
    lower = df['Low'].shift(1).rolling(period//2).min()
    
    mid = (upper + lower) / 2
    
    return pd.DataFrame({"upper" : upper, "lower" : lower, "mid" : mid})
    
    
    
def generate_signals(df : pd.DataFrame, period : int = 20):
    if isinstance(df.columns, pd.MultiIndex):
        df.columns= [col[0] for col in df.columns]
    df = df.copy()
    
    dochian = compute_dochian(df)
    
    df["upper"] = dochian['upper']
    df["lower"] = dochian['lower']
    
    df['atr']  = compute_atr(df)
    
    prev_close = df["Close"].shift(1)
    
    breakout = df["Close"] > df["upper"]
    df["entry_signal"] = (breakout & ~breakout.shift(1).fillna(False)).astype(int)
   
    breakdown = df["Close"] < df["lower"]
    df["exit_signal"] = (breakdown & ~breakdown.shift(1).fillna(False)).astype(int)  
    df["unit_size"] = 0.01 / df["atr"]
    
    return df