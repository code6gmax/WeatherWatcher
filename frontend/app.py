import streamlit as st
import requests
import os
import pandas as pd
from datetime import datetime

# 1. Configuration
# We get the URL of our Backend (FastAPI) from the environment
# If running locally, it defaults to localhost:8000
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

st.set_page_config(page_title="WeatherWatcher", page_icon="⛈️")

st.title("⛈️ Hyper-Local Weather Watcher")
st.write(f"Connected to Backend: `{BACKEND_URL}`")

# --- SECTION 1: CREATE ALERT ---
st.header("1. Create New Alert Rule")
col1, col2 = st.columns(2)

with col1:
    city = st.text_input("City Name", "London")
    email = st.text_input("Your Email (For Logs)", "user@example.com")

with col2:
    min_temp = st.number_input("Alert if Below (°C)", value=None, placeholder="e.g. 0")
    max_temp = st.number_input("Alert if Above (°C)", value=None, placeholder="e.g. 30")

if st.button("Create Alert"):
    payload = {
        "city": city,
        "user_email": email,
        "temperature_min": min_temp,
        "temperature_max": max_temp
    }
    try:
        res = requests.post(f"{BACKEND_URL}/alerts/", json=payload)
        if res.status_code == 200:
            st.success(f"✅ Tracking started for {city}!")
        else:
            st.error(f"Error: {res.text}")
    except Exception as e:
        st.error(f"Connection Failed: {e}")

st.divider()

# --- SECTION 2: ACTIVE ALERTS ---
st.header("2. Currently Active Rules")
if st.button("Refresh Rules"):
    try:
        res = requests.get(f"{BACKEND_URL}/alerts/")
        if res.status_code == 200:
            alerts = res.json()
            if alerts:
                # Convert to DataFrame for a nice table
                df = pd.DataFrame(alerts)
                # Select only useful columns to display
                display_cols = ["id", "city", "temperature_max", "temperature_min", "user_email", "created_at"]
                st.dataframe(df[display_cols])
            else:
                st.info("No active alerts found.")
    except Exception as e:
        st.error(f"Could not fetch alerts: {e}")

st.divider()

# --- SECTION 3: ALERT LOGS (HISTORY) ---
st.header("3. Triggered Logs (History)")
st.caption("The background worker checks weather every 15 mins. If a rule is broken, it appears here.")

if st.button("Refresh Logs"):
    try:
        res = requests.get(f"{BACKEND_URL}/logs/")
        if res.status_code == 200:
            logs = res.json()
            if logs:
                df = pd.DataFrame(logs)
                st.dataframe(df)
            else:
                st.info("No alerts triggered yet. The weather is safe!")
    except Exception as e:
        st.error(f"Could not fetch logs: {e}")