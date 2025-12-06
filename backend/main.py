from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import models, schemas
from database import engine, get_db

# 1. Create Tables automatically on startup
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# 2. Endpoint: Create a new Alert
@app.post("/alerts/", response_model=schemas.AlertResponse)
def create_alert(alert: schemas.AlertCreate, db: Session = Depends(get_db)):
    db_alert = models.WeatherAlert(**alert.dict())
    db.add(db_alert)
    db.commit()
    db.refresh(db_alert)
    return db_alert

# 3. Endpoint: List my Alerts
@app.get("/alerts/", response_model=List[schemas.AlertResponse])
def read_alerts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    alerts = db.query(models.WeatherAlert).offset(skip).limit(limit).all()
    return alerts

# 4. Endpoint: See the Triggered Logs
@app.get("/logs/", response_model=List[schemas.LogResponse])
def read_logs(skip: int = 0, limit: int = 50, db: Session = Depends(get_db)):
    # Return newest logs first
    logs = db.query(models.AlertLog).order_by(models.AlertLog.triggered_at.desc()).offset(skip).limit(limit).all()
    return logs

# 5. Health Check (Useful for Render)
@app.get("/")
def read_root():
    return {"status": "WeatherWatcher API is running"}