import sys
import os
import requests
import time 
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import yfinance as yf
from nsepython import nse_eq 
from app.config import CONFIG
from bs4 import BeautifulSoup
import time
#to get share holding pattern i have to setup selenium for headerless browser
def get_shareholding_from_screener(symbol):
    try:
        url = f"https://www.screener.in/company/{symbol}/consolidated/"
        headers = {
            "User-Agent": "Mozilla/5.0",
            "Accept-Language": "en-US,en;q=0.9"
        }

        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")

        # Look for the table under the "Shareholding Pattern" heading
        section = soup.find("h2", string="Shareholding Pattern")
        if not section:
            raise ValueError("Shareholding section not found")

        table = section.find_next("table")
        rows = table.find_all("tr")

        shareholding = {}
        for row in rows:
            cols = row.find_all("td")
            if len(cols) == 2:
                key = cols[0].text.strip()
                val = cols[1].text.strip()
                if "%" in val:
                    shareholding[key] = val

        return {
            "Promoter": shareholding.get("Promoters", "N/A"),
            "FII": shareholding.get("Foreign Institutions", "N/A"),
            "DII": shareholding.get("Domestic Institutions", "N/A"),
            "Public": shareholding.get("Public", "N/A")
        }

    except Exception as e:
        print(f"Error scraping Screener for {symbol}: {e}")
        return "N/A"

    
def fetch_stock_metrics(ticker):
    stock = yf.Ticker(ticker)
    data = stock.history(period="1d") #to get today's data
    info = stock.info  #to get detailed data

    if data.empty:
        return{"error":f"No data for {ticker}"}
    latest = data.iloc[-1] #to get most latest line

    nse_symbol = ticker.replace(".NS", "") #toget NSE symbol
    shareholding = get_shareholding_from_screener(nse_symbol)

    try:
        nse_data = nse_eq(nse_symbol)
        upper_circuit = float(nse_data["priceInfo"]["upperCP"])
        lower_circuit = float(nse_data["priceInfo"]["lowerCP"])
        ltp = float(nse_data["priceInfo"]["lastPrice"])

        if ltp >= upper_circuit:
            circuit_status = f"U@{upper_circuit}"
        elif ltp <= lower_circuit:
            circuit_status = f"L@{lower_circuit}"
        else:
            circuit_status = "---"
    except Exception as e:
        print(f"Error parsing NSE data for {ticker}: {e}")
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
        "circuit_status": circuit_status,
        "shareholding_pattern": shareholding
    }
    return result

if __name__ == "__main__":
    for symbol in CONFIG["stocks_to_track"]:
        metrics = fetch_stock_metrics(symbol)
        print(metrics)