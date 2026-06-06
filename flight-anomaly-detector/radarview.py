import pygame
import sqlite3
import math
import sys
from config import DB_NAME

#Pygame initialization, window size
pygame.init()
width, height = 600, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Flight Radar")
clock = pygame.time.Clock()

#Colors for radar (RGB)
background = (10, 15, 10)
radar_green = (0, 200, 0)
critical_red = (255, 0, 0)
white = (255, 255, 255)

#Starting position of plane
plane_x, plane_y = width//2, height//2


def get_latest_telemetry():
    """Fetch the most recent row from the database."""
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("SELECT heading, velocity, anomaly_detected, altitude from telemetry ORDER BY timestamp DESC LIMIT 1")
        row = cursor.fetchone()
        conn.close()
        return row
    except sqlite3.OperationalError:
        #This is to avoid a crash if the DB is locked by the generator
        return None
    
running = True
flash_state = False
flash_timer = 0

while running:
    screen.fill(background)

    #Handle window close
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    #Rings to make the radar look cool
    for radius in [100, 200, 280]:
        pygame.draw.circle(screen, (0,50,0), (width//2, height//2), radius, 1)

    data = get_latest_telemetry()

    if data:
        heading, velocity, anomaly, altitude = data

        #Using data we update the position and speed of the plane
        # Compass heading is converted to radians for trig functions
        rad = math.radians(heading-90)
        speed_factor = velocity *0.005  #This is scaled down for the screen display

        plane_x += speed_factor * math.cos(rad)
        plane_y += speed_factor * math.sin(rad)

        #This keeps the plane on screen, meaning the edges wrap
        plane_x %= width
        plane_y %= height

        #Anomaly visuals
        if anomaly == 1:
            #Red flash effect intervals in ms
            if pygame.time.get_ticks() - flash_timer > 200:
                flash_state = not flash_state
                flash_timer = pygame.time.get_ticks()

            color = critical_red if flash_state else white
            #Warning Box
            pygame.draw.rect(screen, critical_red, (10,10, width-20, height - 20), 4)

            font = pygame.font.Font(None, 36)
            text = font.render("ANOMALY DETECTED! PULL UP! PULL UP!", True, critical_red)
            screen.blit(text, (width//2 - 190, 30))

        else:
            color = radar_green

        #Plane blip
        pygame.draw.circle(screen, color, (int(plane_x), int(plane_y)), 8)

        #Text readouts on radar screen
        font = pygame.font.Font(None, 24)
        alt_txt = font.render(f"ALT: {altitude} FT", True, color)
        hdg_txt = font.render(f"HDG: {int(heading)}°", True, color)
        screen.blit(alt_txt, (20, height-50))
        screen.blit(hdg_txt, (20, height -30))

    pygame.display.flip()
    clock.tick(30) #30 FPS

pygame.quit()
sys.exit()