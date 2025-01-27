import pygame
import sys
import random

pygame.init()

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 400
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Snake Game")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

SNAKE_SIZE = 20
snake_pos = [100, 50]  # Initial position of the snake (x, y)
snake_body = [[100, 50], [80, 50], [60, 50]]  # Initial body
snake_direction = "RIGHT"
speed = 10

def spawn_food():
    return [
        random.randint(0, (SCREEN_WIDTH // SNAKE_SIZE) - 1) * SNAKE_SIZE,
        random.randint(0, (SCREEN_HEIGHT // SNAKE_SIZE) - 1) * SNAKE_SIZE
    ]

food_pos = spawn_food()
food_spawn = True

# Clock to control game speed
clock = pygame.time.Clock()

def game_over():
    pygame.quit()
    sys.exit()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP] and snake_direction != "DOWN":
        snake_direction = "UP"
    if keys[pygame.K_DOWN] and snake_direction != "UP":
        snake_direction = "DOWN"
    if keys[pygame.K_LEFT] and snake_direction != "RIGHT":
        snake_direction = "LEFT"
    if keys[pygame.K_RIGHT] and snake_direction != "LEFT":
        snake_direction = "RIGHT"

    if snake_direction == "UP":
        snake_pos[1] -= SNAKE_SIZE
    if snake_direction == "DOWN":
        snake_pos[1] += SNAKE_SIZE
    if snake_direction == "LEFT":
        snake_pos[0] -= SNAKE_SIZE
    if snake_direction == "RIGHT":
        snake_pos[0] += SNAKE_SIZE

    if (
        snake_pos[0] < 0 or snake_pos[0] >= SCREEN_WIDTH or
        snake_pos[1] < 0 or snake_pos[1] >= SCREEN_HEIGHT
    ):
        print("Game Over! The snake hit the wall.")
        game_over()

    snake_body.insert(0, list(snake_pos))

    snake_head_rect = pygame.Rect(snake_pos[0], snake_pos[1], SNAKE_SIZE, SNAKE_SIZE)
    food_rect = pygame.Rect(food_pos[0], food_pos[1], SNAKE_SIZE, SNAKE_SIZE)

    if snake_head_rect.colliderect(food_rect):
        print("Food eaten!")
        food_spawn = False
    else:
        snake_body.pop()

    if not food_spawn:
        food_pos = spawn_food()
        food_spawn = True

    for segment in snake_body[1:]:
        if snake_pos[0] == segment[0] and snake_pos[1] == segment[1]:
            print("Game Over! The snake collided with itself.")
            game_over()

    screen.fill(BLACK)

    for segment in snake_body:
        pygame.draw.rect(screen, GREEN, pygame.Rect(segment[0], segment[1], SNAKE_SIZE, SNAKE_SIZE))

    pygame.draw.rect(screen, RED, pygame.Rect(food_pos[0], food_pos[1], SNAKE_SIZE, SNAKE_SIZE))

    pygame.display.flip()

    clock.tick(speed)

pygame.quit()
sys.exit()
