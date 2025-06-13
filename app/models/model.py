from sqlalchemy import Column, String, Float, DateTime, Integer, JSON
from sqlalchemy.orm import declarative_base
Base = declarative_base()

class RawResponse(Base):
    __tablename__ = "raw_responses"
    id = Column(Integer, primary_key=True)
    symbol = Column(String, index=True)
    timestamp = Column(DateTime, index=True)
    raw = Column(JSON)

class PricePointModel(Base):
    __tablename__ = "price_points"
    id = Column(Integer, primary_key=True)
    symbol = Column(String, index=True)
    price = Column(Float)
    timestamp = Column(DateTime, index=True)
    provider = Column(String)
