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
snake_pos = [100.0, 50.0]  # Use float positions for smooth movement
snake_body = [[100.0, 50.0], [80.0, 50.0], [60.0, 50.0]]  # Initial body positions (floating point)
snake_direction = "RIGHT"
speed = 10

def spawn_food():
    return [
        random.randint(0, (SCREEN_WIDTH // SNAKE_SIZE) - 1) * SNAKE_SIZE,
        random.randint(0, (SCREEN_HEIGHT // SNAKE_SIZE) - 1) * SNAKE_SIZE
    ]

food_pos = spawn_food()
food_spawn = True

score = 0
font = pygame.font.SysFont("Arial", 24)

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

    target_x, target_y = snake_pos[0], snake_pos[1]
    if snake_direction == "UP":
        target_y -= SNAKE_SIZE
    if snake_direction == "DOWN":
        target_y += SNAKE_SIZE
    if snake_direction == "LEFT":
        target_x -= SNAKE_SIZE
    if snake_direction == "RIGHT":
        target_x += SNAKE_SIZE

    snake_pos[0] += (target_x - snake_pos[0]) * 0.1
    snake_pos[1] += (target_y - snake_pos[1]) * 0.1

    snake_head_rect = pygame.Rect(round(snake_pos[0]), round(snake_pos[1]), SNAKE_SIZE, SNAKE_SIZE)

    if (
        snake_pos[0] < 0 or snake_pos[0] >= SCREEN_WIDTH or
        snake_pos[1] < 0 or snake_pos[1] >= SCREEN_HEIGHT
    ):
        print(f"Game Over! Final Score: {score}")
        game_over()

    snake_body.insert(0, [snake_pos[0], snake_pos[1]])

    food_rect = pygame.Rect(food_pos[0], food_pos[1], SNAKE_SIZE, SNAKE_SIZE)
    if snake_head_rect.colliderect(food_rect):
        speed += 1.5
        score += 1
        food_spawn = False
    else:
        snake_body.pop()

    if not food_spawn:
        food_pos = spawn_food()
        food_spawn = True

    for segment in snake_body[1:]:
        if snake_pos[0] == segment[0] and snake_pos[1] == segment[1]:
            print(f"Game Over! Final Score: {score}")
            game_over()

    screen.fill(BLACK)

    for segment in snake_body:
        pygame.draw.rect(screen, GREEN, pygame.Rect(segment[0], segment[1], SNAKE_SIZE, SNAKE_SIZE))

    pygame.draw.rect(screen, RED, pygame.Rect(food_pos[0], food_pos[1], SNAKE_SIZE, SNAKE_SIZE))

    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, [10, 10])  # Draw score at the top left

    pygame.display.flip()

    clock.tick(speed)

pygame.quit()
sys.exit()
