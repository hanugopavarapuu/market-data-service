# consumer/ma_consumer.py

import json
from confluent_kafka import Consumer
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from datetime import datetime

from app.models import PricePointModel, SymbolAverageModel  # import your ORM models
from app.core.config import settings

# 1) Configure DB session
engine = create_engine(settings.database_url)
SessionLocal = sessionmaker(bind=engine)

# 2) Configure Kafka consumer
consumer = Consumer({
    "bootstrap.servers": "kafka:9092",
    "group.id": "ma-consumer-group",
    "auto.offset.reset": "earliest",
})
consumer.subscribe(["price-events"])

def calculate_ma(prices):
    return sum(prices) / len(prices)

def run_consumer():
    db = SessionLocal()
    try:
        while True:
            msg = consumer.poll(1.0)
            if msg and not msg.error():
                data = json.loads(msg.value().decode())
                symbol = data["symbol"]

                # fetch last 5 prices
                rows = (
                    db.query(PricePointModel)
                      .filter(PricePointModel.symbol == symbol)
                      .order_by(PricePointModel.timestamp.desc())
                      .limit(5)
                      .all()
                )
                prices = [row.price for row in rows]
                if len(prices) < 5:
                    continue  # wait until you have 5 points

                ma = calculate_ma(prices)

                # upsert into symbol_averages
                avg = (
                    db.query(SymbolAverageModel)
                      .filter(SymbolAverageModel.symbol == symbol)
                      .one_or_none()
                )
                if avg:
                    avg.avg = ma
                    avg.timestamp = datetime.utcnow()
                else:
                    avg = SymbolAverageModel(
                        symbol=symbol,
                        avg=ma,
                        timestamp=datetime.utcnow()
                    )
                    db.add(avg)
                db.commit()
    finally:
        consumer.close()
        db.close()

if __name__ == "__main__":
    run_consumer()
