import os, httpx
from datetime import datetime

class AlphaVantageProvider:
    BASE_URL = "https://www.alphavantage.co/query"

    def __init__(self, api_key: str):
        self.api_key = api_key

    def fetch_latest(self, symbol: str):
        resp = httpx.get(self.BASE_URL, params={
            "function": "GLOBAL_QUOTE", "symbol": symbol, "apikey": self.api_key
        })
        data = resp.json().get("Global Quote", {})
        price = float(data.get("05. price", 0))
        timestamp = datetime.utcnow().isoformat() + "Z"
        return {"symbol": symbol, "price": price, "timestamp": timestamp, "provider": "alpha_vantage", "raw": data}
