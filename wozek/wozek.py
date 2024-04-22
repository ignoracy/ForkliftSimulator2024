import pygame
import sys
import random
import os

# Initialize Pygame
pygame.init()

# Constants
TILE_SIZE = 96  # Size of a square tile in pixels
GRID_WIDTH, GRID_HEIGHT = 16, 8  # Grid dimensions
SCREEN_WIDTH, SCREEN_HEIGHT = GRID_WIDTH * TILE_SIZE, GRID_HEIGHT * TILE_SIZE
FPS = 60  # Frames per second

# Setup display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Forklift Game')

# Clock
clock = pygame.time.Clock()

# Function to load and scale images
def load_image(name, scale=None):
    """Loads an image and optionally scales it."""
    image = pygame.image.load(name).convert_alpha()
    if scale:
        image = pygame.transform.scale(image, scale)
    return image

# Placeholder for images (will be loaded after video mode set)
forklift_image_full = None
freight_images_full = None

# Game variables
forklift_pos = [7, 3]  # Adjusted starting position of the forklift
carrying_freight = False
carried_freight = None
freight_positions = {}  # Dictionary to keep track of freight positions and types

# Load images
def load_images():
    global forklift_image_full, freight_images_full
    forklift_image_full = load_image('forklift.png', (TILE_SIZE, TILE_SIZE))
    freight_images_full = {
        'clothes': load_image('clothes.png', (TILE_SIZE, TILE_SIZE)),
        'fruit': load_image('fruit.png', (TILE_SIZE, TILE_SIZE)),
        'nuclear_waste': load_image('nuclear_waste.png', (TILE_SIZE, TILE_SIZE)),
        'car_parts': load_image('car_parts.png', (TILE_SIZE, TILE_SIZE)),
    }

# Initialize or reset game elements
def init_game():
    freight_positions.clear()
    load_images()  # Ensure images are loaded after video mode set
    reset_truck_bed_freight()

# Reset freight on the truck bed
def reset_truck_bed_freight():
    types = list(freight_images_full.keys())
    for x in range(12, 16):
        freight_positions[(x, 0)] = random.choice(types)

# Drawing functions
def draw_board():
    screen.fill((255, 255, 255))
    for x in range(GRID_WIDTH):
        for y in range(GRID_HEIGHT):
            pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE), 1)

def draw_truck_bed_and_racks():
    for x in range(12, 16):
        pygame.draw.rect(screen, (0, 0, 255), (x * TILE_SIZE, 0, TILE_SIZE, TILE_SIZE))
    for y in range(5, 8):
        for x in range(GRID_WIDTH):
            pygame.draw.rect(screen, (165, 42, 42), (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))

def draw_forklift_and_freight():
    x, y = forklift_pos
    if carrying_freight:
        # Draw smaller images when carrying freight
        small_size = (TILE_SIZE // 2, TILE_SIZE // 2)
        forklift_small = pygame.transform.scale(forklift_image_full, small_size)
        freight_small = pygame.transform.scale(freight_images_full[carried_freight], small_size)
        screen.blit(forklift_small, (x * TILE_SIZE, y * TILE_SIZE + TILE_SIZE // 2))
        screen.blit(freight_small, (x * TILE_SIZE + TILE_SIZE // 2, y * TILE_SIZE))
    else:
        screen.blit(forklift_image_full, (x * TILE_SIZE, y * TILE_SIZE))

def draw_freight():
    for (x, y), freight_type in freight_positions.items():
        screen.blit(freight_images_full[freight_type], (x * TILE_SIZE, y * TILE_SIZE))

# Game mechanics
def move_forklift(dx, dy):
    global forklift_pos
    new_pos = [forklift_pos[0] + dx, forklift_pos[1] + dy]
    if 0 <= new_pos[0] < GRID_WIDTH and 0 <= new_pos[1] < GRID_HEIGHT:
        forklift_pos = new_pos

def handle_freight():
    global carrying_freight, carried_freight, freight_positions
    pos_tuple = tuple(forklift_pos)
    if carrying_freight:
        if pos_tuple not in freight_positions:
            freight_positions[pos_tuple] = carried_freight
            carrying_freight = False
            carried_freight = None
    else:
        if pos_tuple in freight_positions:
            carried_freight = freight_positions.pop(pos_tuple)
            carrying_freight = True

# Main game loop
def game_loop():
    init_game()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    move_forklift(-1, 0)
                elif event.key == pygame.K_RIGHT:
                    move_forklift(1, 0)
                elif event.key == pygame.K_UP:
                    move_forklift(0, -1)
                elif event.key == pygame.K_DOWN:
                    move_forklift(0, 1)
                elif event.key == pygame.K_SPACE:
                    handle_freight()
                elif event.key == pygame.K_r:
                    reset_truck_bed_freight()

        draw_board()
        draw_truck_bed_and_racks()
        draw_freight()
        draw_forklift_and_freight()
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

game_loop()
