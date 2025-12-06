from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean
from sqlalchemy.sql import func
from database import Base

class WeatherAlert(Base):
    __tablename__ = "weather_alerts"

    id = Column(Integer, primary_key=True, index=True)
    city = Column(String, index=True)
    
    # Thresholds
    temperature_min = Column(Float, nullable=True) # Alert if temp drops below this
    temperature_max = Column(Float, nullable=True) # Alert if temp goes above this
    condition = Column(String, nullable=True)      # e.g., "Rain", "Snow"
    
    # Contact Info (In a real app, this would be Email/SMS)
    # For this demo, we just log it to the dashboard
    user_email = Column(String)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    is_active = Column(Boolean, default=True)

class AlertLog(Base):
    __tablename__ = "alert_logs"

    id = Column(Integer, primary_key=True, index=True)
    alert_id = Column(Integer) # Links back to the rule above
    city = Column(String)
    message = Column(String)   # "Alert! Temp is 35°C in London"
    triggered_at = Column(DateTime(timezone=True), server_default=func.now())