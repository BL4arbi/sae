import pygame
import random
from collections import deque

pygame.init()

WIDTH, HEIGHT = 800, 600
NODE_SIZE = 20

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simulation Robot Aspirateur avec Pathfinding")
clock = pygame.time.Clock()

class Node:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.visited = False

    def get_pos(self):
        return self.x, self.y

cols = WIDTH // NODE_SIZE
rows = HEIGHT // NODE_SIZE

def create_grid():
    grid = [[Node(i, j) for j in range(rows)] for i in range(cols)]
    return grid

grid = create_grid()
start = grid[0][0]

walls = [(random.randint(0, cols-1), random.randint(0, rows-1)) for _ in range(100)]

visited_nodes = []
queue = deque([start])
future_path = list(queue)  # Initialize the future path with the start node

running = True
while running:
    screen.fill((255, 255, 255))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if random.randint(0, 10) == 0:
        wall_to_move = random.choice(walls)
        walls.remove(wall_to_move)
        x = random.randint(0, cols-1)
        y = random.randint(0, rows-1)
        walls.append((x, y))

    if queue:
        current_node = queue.popleft()
        x, y = current_node.get_pos()
        if (x, y) not in walls:
            current_node.visited = True
            visited_nodes.append(current_node)

            # Add unvisited neighbors to the queue
            if x > 0 and grid[x-1][y] not in queue and grid[x-1][y] not in visited_nodes and (x-1, y) not in walls:
                queue.append(grid[x-1][y])
            if x < cols - 1 and grid[x+1][y] not in queue and grid[x+1][y] not in visited_nodes and (x+1, y) not in walls:
                queue.append(grid[x+1][y])
            if y > 0 and grid[x][y-1] not in queue and grid[x][y-1] not in visited_nodes and (x, y-1) not in walls:
                queue.append(grid[x][y-1])
            if y < cols - 1 and grid[x][y+1] not in queue and grid[x][y+1] not in visited_nodes and (x, y+1) not in walls:
                queue.append(grid[x][y+1])

    future_path = list(queue)  # Update the future path with the nodes in the queue

    for wall in walls:
        x, y = wall
        pygame.draw.rect(screen, (0, 0, 0), (x * NODE_SIZE, y * NODE_SIZE, NODE_SIZE, NODE_SIZE))

    for node in visited_nodes:
        x, y = node.get_pos()
        pygame.draw.rect(screen, (0, 0, 255), (x * NODE_SIZE, y * NODE_SIZE, NODE_SIZE, NODE_SIZE))  # Blue for visited nodes

    for node in future_path:
        x, y = node.get_pos()
        pygame.draw.rect(screen, (0, 255, 0), (x * NODE_SIZE, y * NODE_SIZE, NODE_SIZE, NODE_SIZE))  # Green for future path

    if visited_nodes:
        # Red for the aspirateur
        x, y = visited_nodes[-1].get_pos()
        pygame.draw.rect(screen, (255, 0, 0), (x * NODE_SIZE, y * NODE_SIZE, NODE_SIZE, NODE_SIZE))

    pygame.display.flip()
    clock.tick(10)  # Adjust this value to slow down or speed up the animation

pygame.quit()
