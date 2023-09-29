import pygame
from rplidar import RPLidar
import numpy as np


PORT_NAME = 'COM3' #changer le port com selon le pluge
lidar = RPLidar(PORT_NAME)


pygame.init()
width, height = 800, 800
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("LiDAR Data")



def display_lidar_data():
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

        for scan in lidar.iter_scans():
            win.fill((0, 0, 0))
            for (_, angle, distance) in scan:
                x = int(distance * np.cos(np.radians(angle)) / 10)
                y = int(distance * np.sin(np.radians(angle)) / 10)
                pygame.draw.circle(win, (255, 255, 255), (width // 2 + x, height // 2 - y), 2)

            pygame.display.update()

    lidar.stop()
    lidar.disconnect()
    pygame.quit()



display_lidar_data()
