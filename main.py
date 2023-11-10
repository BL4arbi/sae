import numpy as np
from rplidar import RPLidar
import matplotlib.pyplot as plt

# Initialisation du LIDAR
PORT_NAME = 'COM3'
lidar = RPLidar(PORT_NAME)

# Paramètres pour la grille de mapping
MAX_RANGE_MM = 8000  # Portée maximale du LIDAR en millimètres (8 mètres)
GRID_RESOLUTION = 0.05  # Résolution de la grille (5 cm par cellule de grille)
GRID_SIZE = int((MAX_RANGE_MM / 1000) / GRID_RESOLUTION)  # Taille de la grille en cellules

# Configuration de l'affichage avec matplotlib
fig, ax = plt.subplots(figsize=(10, 10))
lidar_position = (GRID_SIZE // 2, GRID_SIZE // 2)  # Position du LIDAR au centre de la grille

# Fonction pour mettre à jour la grille avec les données du scan LIDAR
def update_grid(angles, distances, lidar_position):
    grid = np.full((GRID_SIZE, GRID_SIZE), 0.5)  # Initialisation de la grille avec des valeurs neutres
    for angle, distance in zip(angles, distances):
        if 0 < distance <= MAX_RANGE_MM:  # Filtrage des mesures valides
            # Conversion des coordonnées polaires (angle, distance) en coordonnées cartésiennes (x, y)
            # Les fonctions cos et sin sont utilisées pour cette conversion.
            # cos(angle) donne la projection sur l'axe des x, tandis que sin(angle) donne celle sur l'axe des y.
            x_mm = distance * np.cos(np.radians(angle))  # Conversion de l'angle en radians pour l'utiliser avec cos
            y_mm = distance * np.sin(np.radians(angle))  # Conversion de l'angle en radians pour l'utiliser avec sin

            # Conversion des coordonnées en millimètres en coordonnées de la grille
            x_cell = int(x_mm / (GRID_RESOLUTION * 1000)) + lidar_position[0]
            y_cell = int(y_mm / (GRID_RESOLUTION * 1000)) + lidar_position[1]

            # Vérification si les coordonnées sont dans les limites de la grille
            if (0 <= x_cell < GRID_SIZE) and (0 <= y_cell < GRID_SIZE):
                grid[x_cell, y_cell] = 1  # Marquage de la cellule comme occupée
    return grid

# Exécution du LIDAR et mise à jour de la grille avec les scans
try:
    print("Démarrage du LIDAR...")
    for scan in lidar.iter_scans():
        angles = np.array([item[1] for item in scan])  # Extraction des angles du scan
        distances = np.array([item[2] for item in scan])  # Extraction des distances du scan
        grid = update_grid(angles, distances, lidar_position)  # Mise à jour de la grille avec les nouvelles données
        ax.imshow(grid, cmap='hot', interpolation='nearest')  # Affichage de la grille
        ax.plot(lidar_position[1], lidar_position[0], 'bo')  # Marquage de la position du LIDAR
        plt.pause(0.1)  # Pause pour la mise à jour de l'affichage
        ax.clear()  # Effacement de l'affichage pour le prochain scan
finally:
    lidar.stop()
    lidar.disconnect()  # Arrêt du LIDAR et fermeture de la connexion
