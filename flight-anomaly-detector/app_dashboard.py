import streamlit as st
import pandas as pd
import sqlite3
import time
from config import DB_NAME

st.set_page_config(page_title="Flight Control Analytics", layout="wide")
st.title("Flight Path Telemetry Analytics")

# 1. Read Data from the DB (Runs cleanly once per refresh)
try:
    conn = sqlite3.connect(DB_NAME)
    df = pd.read_sql_query("SELECT * FROM telemetry ORDER BY timestamp DESC LIMIT 50", conn)
    conn.close()
except sqlite3.OperationalError:
    # Fallback if database file is momentarily locked by the mock generator
    df = pd.DataFrame()

# 2. Check if data exists and render layout objects exactly once
if not df.empty:
    latest = df.iloc[0]

    # Checks for Anomalies immediately
    if latest['anomaly_detected'] == 1:
        st.error(f"CRITICAL WARNING: Flight {latest['flight_id']} is experiencing anomalous telemetry!")
    else:
        st.success(f"Flight {latest['flight_id']} Systems Stable")

    # Metrics display (Declared cleanly outside of an infinite loop)
    col1, col2, col3 = st.columns(3)
    col1.metric("Current Altitude", f"{latest['altitude']} ft")
    col2.metric("Velocity", f"{round(latest['velocity'], 1)} kts")
    col3.metric("Heading", f"{int(latest['heading'])}°")

    # Historical Charts
    st.subheader("Altitude History (Last 50 ticks)")
    st.line_chart(df[::-1].set_index('timestamp')['altitude'])

    st.subheader("Velocity History")
    st.line_chart(df[::-1].set_index('timestamp')['velocity'])

else:
    st.info("Waiting for telemetry data stream to start...")

# 3. Streamlit's native approach to live refreshing:
# Pause for 1 second, then trigger a clean script rerun from the top
time.sleep(1)
st.rerun()
