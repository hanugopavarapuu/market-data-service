from fastapi import APIRouter, HTTPException, BackgroundTasks
from app.schemas.price import PricePoint, PollRequest

router = APIRouter(prefix="/prices")

@router.get("/latest", response_model=PricePoint)
def get_latest(symbol: str, provider: str = None):
    # TODO: Query DB or external provider
    return PricePoint(symbol=symbol, price=0.0, timestamp="1970-01-01T00:00:00Z", provider=provider)

@router.post("/poll", status_code=202)
def post_poll(req: PollRequest, bg: BackgroundTasks):
    job_id = "poll_123"  # TODO: generate dynamic ID & persist
    return {"job_id": job_id, "status": "accepted", "config": req.dict()}
