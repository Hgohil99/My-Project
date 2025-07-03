import sys
import os
import requests
import time 
import csv 
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import yfinance as yf
from nsepython import nse_eq 
from app.config import CONFIG
from bs4 import BeautifulSoup
from datetime import datetime
#to get share holding pattern need to setup selenium for headerless browser
def get_shareholding_from_screener(symbol):
    try:
        url = f"https://www.screener.in/company/{symbol}/consolidated/"
        headers = {
            "User-Agent": "Mozilla/5.0",
            "Accept-Language": "en-US,en;q=0.9"
        }

        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")

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

        price_info = nse_data.get("priceInfo")
        if not price_info:
            raise ValueError(f"Missing 'priceInfo' in NSE data for {ticker}")

        upper_circuit = float(price_info["upperCP"])
        lower_circuit = float(price_info["lowerCP"])
        ltp = float(price_info["lastPrice"])

        if ltp >= upper_circuit:
            circuit_status = f"U@{upper_circuit}"
        elif ltp <= lower_circuit:
            circuit_status = f"L@{lower_circuit}"
        else:
            circuit_status = "---"

    except Exception as e:
        print(f"Error parsing NSE data for {ticker}: {e}")
        circuit_status = "N/A"


    if circuit_status.startswith("U@"):
        circuit_event = "Upper Hit"
    elif circuit_status.startswith("L@"):
        circuit_event = "Lower Hit"
    elif circuit_status == "N/A":
        circuit_event = "Unavailable"
    else:
        circuit_event = "Normal"

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
        "shareholding_pattern": shareholding,
        "circuit_event": circuit_event
    }
    return result

def save_metrics_to_csv(metrics_list):
    date_str = datetime.now().strftime("%Y-%m-%d")
    folder_path = r"D:\Hardik\Coding\My Project\sm_app_v1\StockLogs" 
    os.makedirs(folder_path, exist_ok=True)
    file_path = os.path.join(folder_path, f"sm_metrics_{date_str}.csv")

    with open(file_path, mode="w", newline='', encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow([
            "Ticker", "Current Price", "Open Price", "Previous Close",
            "Day High", "Day Low", "52W High", "52W Low",
            "Circuit Status", "Circuit Event",
            "Promoter Holding", "FII Holding", "DII Holding", "Public Holding"
        ])

        for m in metrics_list:
            sh = m["shareholding_pattern"] if isinstance(m["shareholding_pattern"], dict) else {}
            writer.writerow([
                m["ticker"], m["current_price"], m["open_price"], m["previous_close"],
                m["day_high_low"][0], m["day_high_low"][1],
                m["52_week"][0], m["52_week"][1],
                m["circuit_status"], m["circuit_event"],
                sh.get("Promoter", "N/A"), sh.get("FII", "N/A"),
                sh.get("DII", "N/A"), sh.get("Public", "N/A")
            ])

if __name__ == "__main__":
    result = []
    for symbol in CONFIG["stocks_to_track"]:
        metrics = fetch_stock_metrics(symbol)
        print(metrics)
        result.append(metrics)
    save_metrics_to_csv(result)