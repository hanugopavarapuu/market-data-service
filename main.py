from fastapi import FastAPI

app = FastAPI()

@app.get("/health")
def health_check():
    return {"status": "ok"}
from app.api.prices import router as prices_router
app.include_router(prices_router)
