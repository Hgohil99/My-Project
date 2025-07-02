from fastapi import APIRouter
from app.fetcher import fetch_stock_metrics
from app.config import CONFIG

router = APIRouter()

@router.get("/")
def homepage():
    return {"message": "Welcome to Stock Alert API"}


@router.get("/stocks")
def get_all_stocks():
    return [fetch_stock_metrics(t) for t in CONFIG["stocks_to_track"]]

@router.get("/stocks/{ticker}")
def get_stock(ticker: str):
    return fetch_stock_metrics(ticker)
