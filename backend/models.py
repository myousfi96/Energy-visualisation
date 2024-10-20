# backend/models.py

from sqlalchemy import Column, Integer, Float, DateTime, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class EnergyData(Base):
    __tablename__ = 'energy_data'

    id = Column(Integer, primary_key=True, index=True)
    date = Column(DateTime)
    region = Column(String)
    metric = Column(String)
    value = Column(Float)
    latitude = Column(Float)
    longitude = Column(Float)
