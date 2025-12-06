from celery import Celery
import requests
import os
from sqlalchemy.orm import Session
from database import SessionLocal
from models import WeatherAlert, AlertLog
import datetime

# 1. Setup Celery
# It needs a "Broker" (Redis) to receive tasks.
redis_url = os.getenv("REDIS_URL", "redis://localhost:6379/0")
celery_app = Celery("weather_worker", broker=redis_url)

# 2. Configure the Beat (The Schedule)
# This tells Celery: "Run the check_weather task every 15 minutes"
celery_app.conf.beat_schedule = {
    'check-weather-every-15-mins': {
        'task': 'tasks.check_weather',
        'schedule': 900.0, # 900 seconds = 15 minutes
    },
}

# 3. The Actual Task
@celery_app.task
def check_weather():
    print(f"Running Weather Check at {datetime.datetime.now()}")
    db: Session = SessionLocal()
    
    try:
        # Get all active alerts
        alerts = db.query(WeatherAlert).filter(WeatherAlert.is_active == True).all()
        
        for alert in alerts:
            # A. Get Lat/Lon for the city (Open-Meteo needs coords, not names)
            geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={alert.city}&count=1&language=en&format=json"
            geo_res = requests.get(geo_url).json()
            
            if not geo_res.get("results"):
                continue # City not found, skip
                
            lat = geo_res["results"][0]["latitude"]
            lon = geo_res["results"][0]["longitude"]
            
            # B. Get Real Weather
            weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
            weather_res = requests.get(weather_url).json()
            current_temp = weather_res["current_weather"]["temperature"]
            
            # C. Check Conditions
            triggered = False
            msg = ""
            
            if alert.temperature_max and current_temp > alert.temperature_max:
                triggered = True
                msg = f"HOT ALERT: {alert.city} is {current_temp}°C (Above {alert.temperature_max}°C)"
            
            elif alert.temperature_min and current_temp < alert.temperature_min:
                triggered = True
                msg = f"COLD ALERT: {alert.city} is {current_temp}°C (Below {alert.temperature_min}°C)"

            # D. If Triggered, Save to Log
            if triggered:
                print(f"!!! TRIGGERED: {msg}")
                new_log = AlertLog(alert_id=alert.id, city=alert.city, message=msg)
                db.add(new_log)
                db.commit()
                
    except Exception as e:
        print(f"Error checking weather: {e}")
    finally:
        db.close()