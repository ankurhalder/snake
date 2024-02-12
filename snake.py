import pygame
import time
import random

# Initialize pygame
pygame.init()

# Set display dimensions
width, height = 600, 400
block_size = 20

# Define colors
white = (255, 255, 255)
black = (0, 0, 0)
red = (213, 50, 80)
green = (0, 255, 0)
blue = (50, 153, 213)

# Create the display
display = pygame.display.set_mode((width, height))
pygame.display.set_caption("Snake Game")

# Set clock for controlling the game speed
clock = pygame.time.Clock()

# Set font for displaying score
font = pygame.font.SysFont(None, 25)


# Function to draw the snake
def snake(block_size, snake_list):
    for x in snake_list:
        pygame.draw.rect(display, green, [x[0], x[1], block_size, block_size])


# Function to display message
def message(msg, color):
    mesg = font.render(msg, True, color)
    display.blit(mesg, [width / 6, height / 3])


# Main function for the game
def gameLoop():
    game_over = False
    game_close = False

    # Initial position of the snake
    lead_x = width / 2
    lead_y = height / 2
    lead_x_change = 0
    lead_y_change = 0

    # Initial length of the snake
    snake_list = []
    snake_length = 1

    # Position of the food
    food_x = round(random.randrange(0, width - block_size) / block_size) * block_size
    food_y = round(random.randrange(0, height - block_size) / block_size) * block_size

    while not game_over:

        while game_close == True:
            display.fill(black)
            message("You Lost! Press Q to Quit or C to Play Again", red)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        gameLoop()

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    lead_x_change = -block_size
                    lead_y_change = 0
                elif event.key == pygame.K_RIGHT:
                    lead_x_change = block_size
                    lead_y_change = 0
                elif event.key == pygame.K_UP:
                    lead_y_change = -block_size
                    lead_x_change = 0
                elif event.key == pygame.K_DOWN:
                    lead_y_change = block_size
                    lead_x_change = 0

        # Update snake's position
        lead_x += lead_x_change
        lead_y += lead_y_change

        # Check if snake eats food
        if lead_x == food_x and lead_y == food_y:
            food_x = (
                round(random.randrange(0, width - block_size) / block_size) * block_size
            )
            food_y = (
                round(random.randrange(0, height - block_size) / block_size)
                * block_size
            )
            snake_length += 1

        # Game over conditions
        if lead_x >= width or lead_x < 0 or lead_y >= height or lead_y < 0:
            game_close = True
        for segment in snake_list[:-1]:
            if segment == [lead_x, lead_y]:
                game_close = True

        # Update snake's length
        snake_head = []
        snake_head.append(lead_x)
        snake_head.append(lead_y)
        snake_list.append(snake_head)
        if len(snake_list) > snake_length:
            del snake_list[0]

        # Fill the display with black color
        display.fill(black)

        # Draw the food
        pygame.draw.rect(display, blue, [food_x, food_y, block_size, block_size])

        # Draw the snake
        snake(block_size, snake_list)

        # Update the display
        pygame.display.update()

        # Set the speed of the game
        clock.tick(15)

    pygame.quit()
    quit()


gameLoop()
