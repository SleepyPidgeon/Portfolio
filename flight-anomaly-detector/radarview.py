import pygame
import math
import sys
import json
import paho.mqtt.client as mqtt

#Pygame initialization, window size
pygame.init()
width, height = 600, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Flight Radar Tracker")
clock = pygame.time.Clock()

#Colors for radar (RGB)
background = (10, 15, 10)
radar_green = (0, 200, 0)
critical_red = (255, 0, 0)
white = (255, 255, 255)

#Radar should track multiple planes at once
#Format: {flight_id: {x, y, heading, velocity, altitude, anomaly_detected}}
air_traffic = {}

def on_message(client, userdata, msg):
    """Callback is executed every time a flight publishes telemetry data."""
    try:
        payload = json.loads(msg.payload.decode())
        flight_id = payload["flight_id"]

        #A new flight entering the airspace will have its position initialized in the center for now
        if flight_id not in air_traffic:
            air_traffic[flight_id] = {
                "x": float(width // 2),
                "y": float(height // 2),
                "heading": payload["heading"],
                "velocity": payload["velocity"],
                "altitude": payload["altitude"],
                "anomaly_detected": payload["anomaly_detected"]
            }

        else:
            #Update flight positioning/info that occurs in game loop
            air_traffic[flight_id]["heading"] = payload["heading"]
            air_traffic[flight_id]["velocity"] = payload["velocity"]
            air_traffic[flight_id]["altitude"] = payload["altitude"]
            air_traffic[flight_id]["anomaly_detected"] = payload["anomaly_detected"]

    except Exception as e:
        print(f"Error parsing incoming telemetry data: {e}")

#MQTT Client Network Thread
MQTT_BROKER = "localhost"
MQTT_PORT = 1883
MQTT_TOPIC = "aviation/telemetry"

mqtt_client = mqtt.Client(callback_api_version=mqtt.CallbackAPIVersion.VERSION2)
mqtt_client.on_message = on_message
mqtt_client.connect(MQTT_BROKER, MQTT_PORT, 60)
mqtt_client.subscribe(MQTT_TOPIC)
mqtt_client.loop_start()


running = True
flash_state = False
flash_timer = 0

while running:
    screen.fill(background)

    #Handles window close
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    #Drawing standard radar rings
    for radius in [100, 200, 280]:
        pygame.draw.circle(screen, (0,50,0), (width//2, height//2), radius, 1)

        global_anomaly_active = False

        #Draws and updates every flight in the tracking database
    for flight_id, aircraft in air_traffic.items():
        #Physics udpate based on vector geometry
        rad = math.radians(aircraft["heading"] - 90)
        speed_factor = aircraft["velocity"] * 0.005

        aircraft["x"] += speed_factor * math.cos(rad)
        aircraft["y"] += speed_factor * math.sin(rad)

        #Screen wrap-around
        aircraft["x"] %= width
        aircraft["y"] %= height

        #Determine target color
        if aircraft["anomaly_detected"] ==1:
            global_anomaly_active = True
            if pygame.time.get_ticks() - flash_timer > 200:
                flash_state = not flash_state
                flash_timer = pygame.time.get_ticks()
            color = critical_red if flash_state else white
        else:
            color = radar_green

        #Render plane position dot
        pos = (int(aircraft["x"]), int(aircraft["y"]))
        pygame.draw.circle(screen, color, pos, 8)

        #Plane Tag text next to blip
        font_tag = pygame.font.Font(None, 18)
        tag_txt = font_tag.render(f"{flight_id} ({int(aircraft['altitude'])}ft)", True, color)
        screen.blit(tag_txt, (pos[0] + 12, pos[1] - 6))

    #Master Airspace Alarm Notification UI
    if global_anomaly_active:
        pygame.draw.rect(screen, critical_red, (10, 10, width - 20, height - 20), 4)
        font = pygame.font.Font(None, 36)
        text = font.render("CRITICAL AIRSPACE ANOMALY ALERT", True, critical_red)
        screen.blit(text, (width//2 - 210, 30))

    pygame.display.flip()
    clock.tick(30) #30 FPS Execution

#Shutdown protocol
pygame.quit()
mqtt_client.loop_stop()
mqtt_client.disconnect()
sys.exit()
