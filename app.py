import pandas as pd
import numpy as np
import yfinance as yf
import fastapi as api
from fastapi.middleware.cors import CORSMiddleware as cors
import signal_engine as se
import backtester as bt
import metrics
import pydantic as pyd
import math
from datetime import datetime, timedelta


date = datetime.today()
start_1d = (date - timedelta(days = 365*3)).strftime("%Y-%m-%d")
start_1h = (date - timedelta(days = 365+180)).strftime("%Y-%m-%d")
date = date.strftime("%Y-%m-%d")


app = api.FastAPI()
app.add_middleware(cors,allow_origins = ["*"],
                   allow_methods = ["*"],
                   allow_headers = ["*"])


class RunRequest(pyd.BaseModel):
    ticker : str
    interval : str
    

@app.post("/run")
def app_post(request : RunRequest):
    
    start = start_1h
    if(request.interval == "1d"): start = start_1d
    
    data = yf.download(request.ticker,start = start, end = date, interval = request.interval)
    
    if isinstance(data.columns, pd.MultiIndex):
        data.columns = data.columns.get_level_values(0)
    
    if data.empty:
        raise api.HTTPException(status_code = 404, detail = "Ticker Not Found")
    
    
    df = se.generate_signals(data)
    equity_curve = bt.run_backtest(df)
    trades = bt.get_trades(df)
    
    latest = df.iloc[-1]
    signal = "HOLD"
    if latest["entry_signal"] == 1:
        signal = "BUY"
    elif latest["exit_signal"] == 1:
        signal = "SELL"
    
    periods_map = {"1h": 1638, "1d": 252, "1wk": 52, "1mo": 12}
    periods = periods_map.get(request.interval, 252)
    
    tr = metrics.total_return(equity_curve)
    md = metrics.max_drawdown(equity_curve)
    sr = metrics.sharpe_ratio(equity_curve, periods)
    equity_curve = equity_curve.dropna()
    # equity_curve = equity_curve.fillna(0)
    trades = trades.fillna(0)
    tr = float(tr) if not np.isnan(tr) else 0.0
    md = float(md) if not np.isnan(md) else 0.0
    sr = float(sr) if not np.isnan(sr) else 0.0
    
    return {
        "signal" : signal,
        "equity_curve" : equity_curve.reset_index().to_dict(orient = "records"),
        "trades" : trades.to_dict(orient = "records"),
        "total_return" : tr,
        "max_drawdown" : md,
        "sharpe_ratio" : sr
    }
    
    