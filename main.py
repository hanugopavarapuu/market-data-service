from fastapi import FastAPI
from app.api.prices import router as prices_router


app = FastAPI()

@app.get("/health")
def health_check():
    return {"status": "ok"}
app.include_router(prices_router)
