import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import yfinance as yf
from nsepython import nse_eq
from app.config import CONFIG

def fetch_stock_metrics(ticker):
    stock = yf.Ticker(ticker)
    data = stock.history(period="1d") #to get today's data
    info = stock.info  #to get detailed data

    if data.empty:
        return{"error":f"No data for {ticker}"}
    latest = data.iloc[-1] #to get most latest line

    nse_symbol = ticker.replace(".NS", "") #toget NSE symbol
    try:
        nse_data = nse_eq(nse_symbol)
        upper_circuit = float(nse_data["pricebandupper"])
        lower_circuit = float(nse_data["pricebandlower"])
        ltp = float(nse_data["lastPrice"])

        if ltp >= upper_circuit:
            circuit_status = f"U@{upper_circuit}"
        elif ltp <= lower_circuit:
            circuit_status = f"L@{lower_circuit}"
        else:
            circuit_status = "---"
    except Exception:
        circuit_status = "N/A"


    result = {
        "ticker": ticker,
        "current_price": info.get("currentPrice"),
        "open_price": round(float(latest["Open"]), 2),
        "previous_close": round(info.get("previousClose"), 2),
        "day_high_low": (
            round(float(latest["High"]),2),
            round(float(latest["Low"]), 2)
        ),
        "52_week": (
            info.get("fiftyTwoWeekHigh"),
            info.get("fiftyTwoWeekLow")
        ),
        "circuit_status": circuit_status
    }
    return result

if __name__ == "__main__":
    for symbol in CONFIG["stocks_to_track"]:
        metrics = fetch_stock_metrics(symbol)
        print(metrics)