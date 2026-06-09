import sqlite3
import json
import paho.mqtt.client as mqtt
from config import DB_NAME

MQTT_BROKER = "localhost"
MQTT_PORT = 1883
MQTT_TOPIC = "aviation/telemetry"

def on_message(client, userdata, msg):
    """Listens to the broker and logs rows into the datbase"""

    try:
        data = json.loads(msg.payload.decode())

        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()

        cursor.execute('''
                       INSERT INTO telemetry (timestamp, flight_id, altitude, velocity, heading, anomaly_detected)
                       VALUES (?, ?, ?, ?, ?, ?)
                       ''', (data["timestamp"], data["flight_id"], data["altitude"], data["velocity"], data["heading"], data["anomaly_detected"]))
        
        conn.commit()
        conn.close()
        print(f"Logged to SQLite DB -> Flight: {data['flight_id']} | Alt: {data['altitude']}ft")


    except sqlite3.OperationalError:
        print("Database temporarily locked by reading dashboard process. Skipping tick safely...")
    except Exception as e:
        print(f"Logging error encountered: {e}")


#Ingestion consumer node
# Run Ingestion Consumer Node
client = mqtt.Client(callback_api_version=mqtt.CallbackAPIVersion.VERSION2)
client.on_message = on_message
client.connect(MQTT_BROKER, MQTT_PORT, 60)
client.subscribe(MQTT_TOPIC)

print("Database Logger Node is active. Listening for flight telemetry stream...")
try:
    client.loop_forever() # Dedicated processing loop
except KeyboardInterrupt:
    print("\nDatabase logger shutting down cleanly.")