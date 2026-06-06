import { useState } from "react"
import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer} from "recharts"


export default function App() {

    const [ticker, setTicker] = useState("")
    const [interval, setInterval] = useState("1d")
    const [signal, setSignal] = useState("HOLD")
    const [equityCurve, setEquityCurve] = useState([])
    const [trades, setTrades] = useState([])
    const [totalreturn, setTotalreturn] = useState(null)
    const [maxdrawdown, setMaxdrawdown] = useState(null)
    const [sharperatio, setSharperatio] = useState(null)
    const [loading, setLoading] = useState(false)
    const [error, setError] = useState("")

    
    
    async function runBacktest(){
        setError("")
        setLoading(true)
        try{
        
        const response = await fetch("http://localhost:8000/run",{
            method: "POST",
            headers : {"Content-Type" : "application/json"},
            body : JSON.stringify({ticker, interval})
        })
    
        const data = await response.json()
        setSignal(data.signal)
        setEquityCurve(data.equity_curve)
        setTrades(data.trades)
        setTotalreturn(data.total_return)
        setMaxdrawdown(data.max_drawdown)
        setSharperatio(data.sharpe_ratio)
    } catch(e){
        setError("Something went wrong")
    } finally {
        setLoading(false)
    }
}
    return (
        <div className="app">

            <input
                type = "text"
                placeholder = "AAPL"
                value = {ticker}
                onChange = {(e) => setTicker(e.target.value)}
            />

            <select value={interval} onChange={(e) => setInterval(e.target.value)}>
                <option value = "1h">1h</option>
                <option value = "1d">1d</option>
                </select>


            <button onClick={runBacktest}>
               {loading ? "Running..." : "Run Backtest"}
                </button>

            {error && <p>{error}</p>}

            {totalreturn !== null &&(
                <>
                <div className="card">
                    <p>Total Return</p>
                    <p>{totalreturn}%</p>
                </div>
                <div className="card">
                    <p>Max Drawdown</p>
                    <p>{maxdrawdown}</p>
                </div>
                <div className="card">
                    <p>Sharpe Ratio</p>
                    <p>{sharperatio}</p>
                </div>
                <div className="card">
                    <p>Signal</p>
                    <p>{signal}</p>
                </div>
                </>
                )}

                {equityCurve.length > 0 && (
                    <ResponsiveContainer width = "100%" height={300}>
                        <LineChart data={equityCurve}>
                            <XAxis dataKey = "date"/>
                            <YAxis/>
                            <Tooltip/>
                            <Line dataKey= "portfolio_value" dot = {false}/>
                        </LineChart>
                    </ResponsiveContainer>
                )}

                {trades.length > 0 && (
                    <table>
                        <thead>
                            <tr>
                                <th>Entry Date</th>
                                <th>Exit Date</th>
                                <th>Entry Price</th>
                                <th>Exit Price</th>
                                <th>PnL</th>
                            </tr>
                        </thead>
                        <tbody>
                            {trades.map((trade, index) => (
                                <tr key={index}>
                                    <td>{trade.entry_date}</td>
                                    <td>{trade.exit_date}</td>
                                    <td>{trade.entry_price}</td>
                                    <td>{trade.exit_price}</td>
                                    <td>{trade.pnl}</td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                )}

        </div>

    )

}


