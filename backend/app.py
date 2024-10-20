# backend/app.py

from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from models import Base, EnergyData
from typing import List
from datetime import datetime, timedelta
import pandas as pd
import random

app = FastAPI()

Base.metadata.create_all(bind=engine)

def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

def generate_synthetic_energy_data():
    print("Generating synthetic energy data...")
    regions = ['North America', 'Europe', 'Asia', 'South America', 'Africa', 'Australia']
    metrics = ['Power Output', 'Energy Consumption', 'Renewable Generation', 'CO2 Emissions']
    start_date = datetime.utcnow() - timedelta(days=30)
    dates = pd.date_range(start=start_date, periods=720, freq='H')  # 720 hours (~30 days)
    data = []

    for date in dates:
        for region in regions:
            latitude, longitude = get_region_coordinates(region)
            for metric in metrics:
                value = generate_metric_value(metric)
                data.append({
                    'date': date,
                    'region': region,
                    'metric': metric,
                    'value': value,
                    'latitude': latitude,
                    'longitude': longitude
                })

    return pd.DataFrame(data)

def get_region_coordinates(region):
    coordinates = {
        'North America': (54.5260, -105.2551),
        'Europe': (54.5260, 15.2551),
        'Asia': (34.0479, 100.6197),
        'South America': (-8.7832, -55.4915),
        'Africa': (8.7832, 34.5085),
        'Australia': (-25.2744, 133.7751)
    }
    return coordinates.get(region, (0.0, 0.0))

def generate_metric_value(metric):
    base_values = {
        'Power Output': random.uniform(1000, 5000),
        'Energy Consumption': random.uniform(800, 4500),
        'Renewable Generation': random.uniform(200, 3000),
        'CO2 Emissions': random.uniform(50, 1000)
    }
    return base_values.get(metric, 0.0) + random.gauss(0, 100)

@app.on_event("startup")
def load_data():
    db = SessionLocal()
    if not db.query(EnergyData).first():
        data = generate_synthetic_energy_data()
        data_records = data.to_dict(orient='records')
        print("Inserting synthetic data into the database...")
        for record in data_records:
            energy_data = EnergyData(
                date=record['date'],
                region=record['region'],
                metric=record['metric'],
                value=record['value'],
                latitude=record['latitude'],
                longitude=record['longitude']
            )
            db.add(energy_data)
        db.commit()
        print("Data insertion complete.")
    db.close()

@app.get("/energy_data/")
def get_energy_data(db: Session = Depends(get_db)):
    data = db.query(EnergyData).all()
    return data

@app.get("/energy_data/region/{region}")
def get_energy_data_by_region(region: str, db: Session = Depends(get_db)):
    data = db.query(EnergyData).filter(EnergyData.region == region).all()
    return data

@app.get("/regions/")
def get_regions(db: Session = Depends(get_db)):
    regions = db.query(EnergyData.region).distinct().all()
    regions = [r[0] for r in regions]
    return regions

@app.get("/metrics/")
def get_metrics(db: Session = Depends(get_db)):
    metrics = db.query(EnergyData.metric).distinct().all()
    metrics = [m[0] for m in metrics]
    return metrics
