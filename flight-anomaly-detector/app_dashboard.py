import streamlit as st
import pandas as pd
import sqlite3
import time
from config import DB_NAME

st.set_page_config(page_title="Commercial Air Traffic Analytics", layout="wide")
st.title("Airspace Fleet Telemetry Center")

# Fetch all available data from the database
try:
    conn = sqlite3.connect(DB_NAME)
    df_global = pd.read_sql_query("SELECT * FROM telemetry ORDER BY timestamp DESC", conn)
    conn.close()
except sqlite3.OperationalError:
    df_global = pd.DataFrame()

if not df_global.empty:
    # 1. Interactive Fleet Selection Tool
    unique_flights = df_global['flight_id'].unique()
    selected_flight = st.sidebar.selectbox("Select Target Aircraft Monitor", unique_flights)

    # Filter data specifically targeting our dropdown choice
    df = df_global[df_global['flight_id'] == selected_flight].head(50)
    latest = df.iloc[0]

    # 2. Safety Diagnostics Warning UI
    if latest['anomaly_detected'] == 1:
        st.error(f"CRITICAL SYSTEM RADAR ALARM: {selected_flight} is registering anomalies!")
    else:
        st.success(f"Flight Tracker Diagnostic: {selected_flight} Operational Performance Stable")

    # 3. Dynamic Real-Time Key Performance Indicators (KPIs)
    col1, col2, col3 = st.columns(3)
    col1.metric("Live Selected Altitude", f"{int(latest['altitude'])} ft")
    col2.metric("Ground Track Velocity", f"{round(latest['velocity'], 1)} kts")
    col3.metric("Magnetic Heading Vector", f"{int(latest['heading'])}°")

    # 4. Flight Performance Trend Visualizations
    st.subheader(f"Altitude Profile History: {selected_flight}")
    st.line_chart(df[::-1].set_index('timestamp')['altitude'])

    st.subheader(f"Velocity Profile History: {selected_flight}")
    st.line_chart(df[::-1].set_index('timestamp')['velocity'])

else:
    st.info("System initializing. Waiting for the Database Logger node to capture telemetry packets...")

# Refresh control loops every 1 second
time.sleep(1)
st.rerun()
