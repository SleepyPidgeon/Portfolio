import sqlite3
import time
import random
from config import DB_NAME


def generate_mock_telemetry():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    flight_id = "AA-781"
    altitude = 35000
    velocity = 460.0
    heading = 180.0

    print(f"Starting live telemetry stream for {flight_id}. Press ctrl+c to stop stream.")

    try:
        while True:
            #Simulating normal fluctuations
            altitude += random.randint(-100, 100)
            velocity += random.uniform(-2.0, 2.0)
            heading = (heading + random.uniform(-1.0, 1.0))%360

            #Random Anomaly
            anomaly = 0
            if random.random() < 0.01:
                anomaly = 1
                #Simulating drop in altitude
                altitude -= random.randint(2000, 5000)
                print(f"\n ANOMALY INJECTED FOR {flight_id}")

            timestamp = time.time()

            #Inserts data in SQLite
            cursor.execute('''
                           INSERT INTO telemetry (timestamp, flight_id, altitude, velocity, heading, anomaly_detected)
                           VALUES (?, ?, ?, ?, ?, ?)
                           ''', (timestamp, flight_id, altitude, velocity, heading, anomaly))
            
            conn.commit()

            print(f"Logged -> Altitude: {altitude}ft | Velocity: {round(velocity, 1)}kts | Anomaly: {anomaly}", end="\r")

            #Wait 1 second before next tick
            time.sleep(1)


    except KeyboardInterrupt:
        print("\nTelemetry stream stopped by user.")
    finally:
        conn.close()

if __name__ == "__main__":
    generate_mock_telemetry()