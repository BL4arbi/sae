import pygame
import random
from queue import PriorityQueue

# Initialisation de pygame.
pygame.init()

# Dimensions de l'écran.
WIDTH, HEIGHT = 800, 600

# Taille des nœuds de la grille.
NODE_SIZE = 20

# Création de l'écran et d'une horloge pour gérer le framerate.
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simulation Robot Aspirateur avec Pathfinding")
clock = pygame.time.Clock()


class Node:
    """Représente un nœud sur la grille."""
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.neighbors = []
        self.g = float('inf')
        self.f = float('inf')
        self.previous = None

    def get_pos(self):
        """Retourne la position du nœud."""
        return self.x, self.y

    def add_neighbors(self, grid):
        """Ajoute les nœuds voisins à la liste des voisins."""
        if self.x > 0:
            self.neighbors.append(grid[self.x-1][self.y])
        if self.x < len(grid) - 1:
            self.neighbors.append(grid[self.x+1][self.y])
        if self.y > 0:
            self.neighbors.append(grid[self.x][self.y-1])
        if self.y < len(grid[0]) - 1:
            self.neighbors.append(grid[self.x][self.y+1])

    def __lt__(self, other):
        """Rend cette classe sortable en fonction de la valeur de f."""
        return self.f < other.f

def heuristic(node1, node2):
    """Calcule une heuristique (distance Manhattan) entre deux nœuds."""
    x1, y1 = node1.get_pos()
    x2, y2 = node2.get_pos()
    return abs(x1 - x2) + abs(y1 - y2)


def a_star(start, end):
    """Implémentation de l'algorithme A* pour trouver le chemin le plus court entre deux nœuds."""
    open_set = PriorityQueue()
    open_set.put((0, start))
    came_from = {}
    start.g = 0
    start.f = heuristic(start, end)
    open_set_hash = {start}

    while not open_set.empty():
        current = open_set.get()[1]
        open_set_hash.remove(current)

        if current == end:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            return path

        for neighbor in current.neighbors:
            temp_g = current.g + 1
            if temp_g < neighbor.g:
                came_from[neighbor] = current
                neighbor.g = temp_g
                neighbor.f = temp_g + heuristic(neighbor, end)
                if neighbor not in open_set_hash:
                    open_set.put((neighbor.f, neighbor))
                    open_set_hash.add(neighbor)

    return []

cols = WIDTH // NODE_SIZE
rows = HEIGHT // NODE_SIZE

def create_grid():
    """grille avec des nœuds et leurs voisins"""
    grid = [[Node(i, j) for j in range(rows)] for i in range(cols)]
    for i in range(cols):
        for j in range(rows):
            grid[i][j].add_neighbors(grid)
    return grid

# Initialisation de la grille, des positions de départ et d'arrivée, et des obstacles.
grid = create_grid()
start = (0, 0)
end = (cols - 1, rows - 1)

walls = [random.choice([(random.randint(0, cols-1), random.randint(0, rows-1)) for _ in range(100)])]

path = a_star(grid[start[0]][start[1]], grid[end[0]][end[1]])
current_pos = start

# main en gros
running = True
while running:
    screen.fill((255, 255, 255))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if random.randint(0, 10) == 0:  # Augmentation de la fréquence de déplacement des obstacles pas au point
        wall_to_move = random.choice(walls)
        walls.remove(wall_to_move)
        x = random.randint(0, cols-1)
        y = random.randint(0, rows-1)
        walls.append((x, y))

        grid = create_grid()  # Recréer la grille en fonction des nouveaux obstacles marche pas mal
        for wall in walls:
            x, y = wall
            grid[x][y].neighbors = []

        path = a_star(grid[current_pos[0]][current_pos[1]], grid[end[0]][end[1]])

    # draw tout
    for wall in walls:
        x, y = wall
        pygame.draw.rect(screen, (0, 0, 0), (x*NODE_SIZE, y*NODE_SIZE, NODE_SIZE, NODE_SIZE))

    for node in path:
        x, y = node.get_pos()
        pygame.draw.rect(screen, (0, 255, 0), (x*NODE_SIZE, y*NODE_SIZE, NODE_SIZE, NODE_SIZE))

    pygame.draw.rect(screen, (255, 0, 0), (current_pos[0]*NODE_SIZE, current_pos[1]*NODE_SIZE, NODE_SIZE, NODE_SIZE))
    pygame.draw.rect(screen, (0, 0, 255), (end[0]*NODE_SIZE, end[1]*NODE_SIZE, NODE_SIZE, NODE_SIZE))

    # regarde les node pour se déplacer
    if path and len(path) > 1:
        next_node = path[-2]
        next_pos = next_node.get_pos()
        if next_pos not in walls:
            current_pos = next_pos
            path = a_star(grid[current_pos[0]][current_pos[1]], grid[end[0]][end[1]])

    pygame.display.flip()
    clock.tick(5)

pygame.quit()
