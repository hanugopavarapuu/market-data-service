# app/services/price_service.py

import json
from datetime import datetime
from confluent_kafka import Producer
from sqlalchemy.orm import Session

from app.models import RawResponse, PricePointModel
from app.services.provider import AlphaVantageProvider
from app.core.config import settings

# initialize Kafka producer once
_kafka_producer = Producer({"bootstrap.servers": "kafka:9092"})

def fetch_and_store_latest(symbol: str, db: Session):
    # 1) fetch from Alpha Vantage
    provider = AlphaVantageProvider(settings.alpha_vantage_key)
    result = provider.fetch_latest(symbol)

    # 2) persist raw response
    raw = RawResponse(
        symbol=result["symbol"],
        timestamp=datetime.fromisoformat(result["timestamp"].rstrip("Z")),
        raw=result["raw"],
    )
    db.add(raw)
    db.commit()
    db.refresh(raw)

    # 3) persist parsed price point
    price_point = PricePointModel(
        symbol=result["symbol"],
        price=result["price"],
        timestamp=datetime.fromisoformat(result["timestamp"].rstrip("Z")),
        provider=result["provider"],
    )
    db.add(price_point)
    db.commit()
    db.refresh(price_point)

    # —–––––––––––––––––––––––––––––––––––––
    # 4) PRODUCE to Kafka (drop in your 5.2 logic here)
    message = {
        "symbol": price_point.symbol,
        "price": price_point.price,
        "timestamp": price_point.timestamp.isoformat() + "Z",
        "source": price_point.provider,
        "raw_response_id": raw.id,
    }
    _kafka_producer.produce(
        topic="price-events",
        value=json.dumps(message).encode("utf-8")
    )
    _kafka_producer.flush()
    # —–––––––––––––––––––––––––––––––––––––

    return price_point
