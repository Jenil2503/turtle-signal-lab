import numpy as np
import pandas as pd


def total_return(equity_curve : pd.DataFrame):
    first = equity_curve["portfolio_value"].iloc[0]
    last = equity_curve["portfolio_value"].iloc[-1]
    
    return (( last - first ) / first )*100


def max_drawdown(equity_curve : pd.DataFrame):
    
    values = equity_curve["portfolio_value"]
    
    rolling_max = values.cummax()
    
    drawdown = (values - rolling_max) / rolling_max
    
    return drawdown.min() * 100


def sharpe_ratio(equity_curve : pd.DataFrame, periods_per_year : int):
    
    returns = equity_curve["portfolio_value"].pct_change()
    
    mean_return = returns.mean()
    
    std_return = returns.std()
    
    if std_return == 0 or np.isnan(std_return):
        return 0.0
    
    sharpe = (mean_return / std_return) * np.sqrt(periods_per_year)
    
    return round(sharpe,2)