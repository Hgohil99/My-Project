import yfinance as yf
from app.config import CONFIG

def fetch_stock_metrics(ticker):
    stock = yf.Ticker(ticker)
    data = stock.history(period="id") #to get today's data
    info = stock.info  #to get detailed data

    if data.empty:
        return{"error":f"No data for {ticker}"}
    latest = data.iloc[-1] #to get most latest line

    result = {
        "ticker": ticker,
        "current_price": info.get("currentPrice"),
        "open_price": latest["Open"],
        "previous_close": info.get("previousClose"),
        "day_high_low": (
            latest["High"],
            latest["Low"]
        ),
        "52_week": (
            info.get("fiftyTwoWeekHigh"),
            info.get("fiftyTwoWeekLow")
        ),
    }
    return result

if __name__ == "__main__":
    for symbol in CONFIG["stocks_to_track"]:
        metrics = fetch_stock_metrics(symbol)
        print(metrics)