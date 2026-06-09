import asyncio
import json
import random
import time
import paho.mqtt.client as mqtt

#MQTT Config
MQTT_BROKER = "localhost"
MQTT_PORT = 1883
MQTT_TOPIC = "aviation/telemetry"

#Initialize MQTT Client
mqtt_client = mqtt.Client(callback_api_version=mqtt.CallbackAPIVersion.VERSION2)
mqtt_client.connect(MQTT_BROKER, MQTT_PORT, 60)
mqtt_client.loop_start()

#List of mock flights in airspace
FLIGHTS = [
    {"id": "AA-780", "alt": 35000, "vel": 460.0, "hdg": 180.0},
    {"id": "UA-241", "alt": 32000, "vel": 440.0, "hdg": 90.0},
    {"id": "DL-915", "alt": 28000, "vel": 415.0, "hdg": 270.0},
    {"id": "SW-4401", "alt": 38000, "vel": 475.0, "hdg": 45.0}
]

async def simulate_aircraft(aircraft):
    flight_id = aircraft["id"]
    altitude = aircraft["alt"]
    velocity = aircraft["vel"]
    heading = aircraft["hdg"]

    while True:
        #Kinematic Updates
        altitude += random.randint(-50,50)
        altitude = max(2000, min(altitude, 43000)) #Realisitc bounds
        velocity += random.uniform(-1.0, 1.0)
        heading = (heading + random.uniform(-0.5, 0.5))%360

        #Anomaly injection
        anomaly = 0
        if random.random() < 0.01:
            anomaly = 1
            altitude -= random.randint(1500, 3000)
            print(f"\n ALERT: Anomaly detected on Flight: {flight_id}!")

            #JSON String for data package
            payload = {
                "timestamp": time.time(),
                "flight_id": flight_id,
                "altitude": int(altitude),
                "velocity": round(velocity, 1),
                "heading": round(heading, 1),
                "anomaly_detected": anomaly
            }

            #Broadcast Telemetry to MQTT Broker
            mqtt_client.publish(MQTT_TOPIC, json.dumps(payload))

            #Streams the logs cleanly to console
            print(f"[{flight_id}] Alt: {payload['altitude']}ft | Hdg: {payload['heading']}° | Vel: {payload['velocity']}kts")

            #1 second interval for broadcasts
            await asyncio.sleep(1)

async def main():
    print(f"Starting commercial aircraft simulation...")
    #All aircraft simulations ran concurrently
    tasks = [simulate_aircraft(flight) for flight in FLIGHTS]
    await asyncio.gather(*tasks)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nSimulation stopped by user.")
        mqtt_client.loop_stop()
        mqtt_client.disconnect()
