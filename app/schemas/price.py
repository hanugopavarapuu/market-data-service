from pydantic import BaseModel
from typing import List, Optional

class PricePoint(BaseModel):
    symbol: str
    price: float
    timestamp: str
    provider: Optional[str] = None

class PollRequest(BaseModel):
    symbols: List[str]
    interval: int
    provider: Optional[str]
