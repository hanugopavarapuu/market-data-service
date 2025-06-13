from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.dependencies import get_db
from app.schemas.price import PricePoint
from app.services.price_service import fetch_and_store_latest

router = APIRouter(
    prefix="/prices",
    tags=["prices"]
)

@router.get("/latest", response_model=PricePoint)
def get_latest(symbol: str, db: Session = Depends(get_db)):
    try:
        pp = fetch_and_store_latest(symbol, db)
        return pp
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
