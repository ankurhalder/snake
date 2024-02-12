import pygame
import time
import random

pygame.init()

width, height = 600, 400
block_size = 20

white = (255, 255, 255)
black = (0, 0, 0)
red = (213, 50, 80)
green = (0, 255, 0)
blue = (50, 153, 213)

display = pygame.display.set_mode((width, height))
pygame.display.set_caption("Snake Game")

clock = pygame.time.Clock()

font = pygame.font.SysFont(None, 25)


def snake(block_size, snake_list):
    for x in snake_list:
        pygame.draw.rect(display, green, [x[0], x[1], block_size, block_size])


def message(msg, color):
    mesg = font.render(msg, True, color)
    display.blit(mesg, [width / 6, height / 3])


def get_high_score():
    try:
        with open("highscore.txt", "r") as file:
            return int(file.read())
    except FileNotFoundError:
        return 0


def set_high_score(score):
    with open("highscore.txt", "w") as file:
        file.write(str(score))


def gameLoop():
    game_over = False
    game_close = False

    lead_x = width / 2
    lead_y = height / 2
    lead_x_change = 0
    lead_y_change = 0

    snake_list = []
    snake_length = 1

    food_x = round(random.randrange(0, width - block_size) / block_size) * block_size
    food_y = round(random.randrange(0, height - block_size) / block_size) * block_size

    score = 0
    high_score = get_high_score()

    health = 3

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

        lead_x += lead_x_change
        lead_y += lead_y_change

        if lead_x == food_x and lead_y == food_y:
            food_x = (
                round(random.randrange(0, width - block_size) / block_size) * block_size
            )
            food_y = (
                round(random.randrange(0, height - block_size) / block_size)
                * block_size
            )
            snake_length += 1
            score += 10

            if score > high_score:
                high_score = score
                set_high_score(high_score)

        if lead_x >= width or lead_x < 0 or lead_y >= height or lead_y < 0:
            health -= 1
            if health == 0:
                game_close = True
            else:
                lead_x = width / 2
                lead_y = height / 2
                snake_list = []
                snake_length = 1

        for segment in snake_list[:-1]:
            if segment == [lead_x, lead_y]:
                health -= 1
                if health == 0:
                    game_close = True
                else:
                    lead_x = width / 2
                    lead_y = height / 2
                    snake_list = []
                    snake_length = 1

        snake_head = []
        snake_head.append(lead_x)
        snake_head.append(lead_y)
        snake_list.append(snake_head)
        if len(snake_list) > snake_length:
            del snake_list[0]

        display.fill(black)
        pygame.draw.rect(display, blue, [food_x, food_y, block_size, block_size])

        snake(block_size, snake_list)

        score_text = font.render("Score: " + str(score), True, white)
        display.blit(score_text, [10, 10])

        high_score_text = font.render("High Score: " + str(high_score), True, white)
        display.blit(high_score_text, [width - 150, 10])

        health_text = font.render("Health: " + str(health), True, white)
        display.blit(health_text, [10, 30])

        pygame.display.update()

        clock.tick(15)

    pygame.quit()
    quit()


gameLoop()
