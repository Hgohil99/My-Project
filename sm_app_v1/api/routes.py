from fastapi import APIRouter
from app.fetcher import fetch_stock_metrics
from app.config import CONFIG
from fastapi import BackgroundTasks
from app.fetcher import fetch_stock_metrics, save_metrics_to_csv


router = APIRouter()

@router.get("/")
def homepage():
    return {"message": "Welcome to Stock Alert API"}


@router.get("/stocks")
def get_all_stocks():
    return [fetch_stock_metrics(t) for t in CONFIG["stocks_to_track"]]

@router.get("/alerts")
def get_circuit_alerts():
    """
    Returns only stocks hitting upper/lower circuits.
    """
    results = []
    for symbol in CONFIG["stocks_to_track"]:
        data = fetch_stock_metrics(symbol)
        if data.get("circuit_event") in ["Upper Circuit", "Lower Circuit"]:
            results.append(data)
    return results

@router.get("/summary")
def market_summary():
    """
    Returns a summary of stock movement across the watchlist.
    Groups into up, down, flat, and circuit.
    """
    summary = {
        "up": 0,
        "down": 0,
        "flat": 0,
        "on_circuit": 0
    }

    for symbol in CONFIG["stocks_to_track"]:
        data = fetch_stock_metrics(symbol)

        if data.get("circuit_event") in ["Upper Circuit", "Lower Circuit"]:
            summary["on_circuit"] += 1
        elif data["current_price"] > data["previous_close"]:
            summary["up"] += 1
        elif data["current_price"] < data["previous_close"]:
            summary["down"] += 1
        else:
            summary["flat"] += 1

    return summary


@router.get("/shareholding/{ticker}")
def get_shareholding(ticker: str):
    data = fetch_stock_metrics(ticker)
    shareholding = data.get("shareholding_pattern")

    if not shareholding:
        return {
            "ticker": ticker,
            "shareholding": "Not available or failed to fetch from source"
        }
    if shareholding == "N/A":
        return {
            "ticker": ticker,
            "shareholding": "Not available from Screener.in at this time"
        }

    return {
        "ticker": ticker,
        "shareholding": shareholding
    }

@router.post("/log/now")
def trigger_log(background_tasks: BackgroundTasks):
    """
    Manually triggers the stock snapshot and saves to CSV.
    """
    def run_snapshot():
        results = []
        for symbol in CONFIG["stocks_to_track"]:
            data = fetch_stock_metrics(symbol)
            results.append(data)
        save_metrics_to_csv(results)
        print("Manual snapshot saved to CSV.")

    background_tasks.add_task(run_snapshot)
    return {"message": "Snapshot task scheduled. CSV will be saved shortly."}