import pygame
import time
import random
import os

pygame.init()

screen_info = pygame.display.Info()
width, height = screen_info.current_w, screen_info.current_h

block_size = 20

white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (50, 153, 213)

display = pygame.display.set_mode((width, height), pygame.FULLSCREEN)
pygame.display.set_caption("Snake Game")

clock = pygame.time.Clock()

font = pygame.font.SysFont(None, 25)


def snake(block_size, snake_list):
    for x in snake_list:
        pygame.draw.rect(display, green, [x[0], x[1], block_size, block_size])


def message(msg, color, y_displace=0):
    mesg = font.render(msg, True, color)
    text_rect = mesg.get_rect(center=(width / 2, height / 2 + y_displace))
    display.blit(mesg, text_rect)


def get_high_score():
    try:
        with open("highscore.txt", "r") as file:
            return int(file.read())
    except FileNotFoundError:
        return 0


def set_high_score(score):
    with open("highscore.txt", "w") as file:
        file.write(str(score))


def homePage():
    home_page = True

    button_texts = ["Start Game", "Reset Best Score", "Quit Game"]
    selected_button_index = 0

    while home_page:
        display.fill(black)
        message("Snake Game By Ankur Halder", white, -150)

        button_rects = []
        for i, text in enumerate(button_texts):
            button_rect = pygame.Rect(
                width / 2 - 100, height / 2 - 50 + i * 60, 200, 50
            )
            button_rects.append(button_rect)

            if i == selected_button_index:
                pygame.draw.rect(display, green, button_rect)
            else:
                pygame.draw.rect(display, white, button_rect)

            message(text, black, -35 + i * 60)

        best_score_text = font.render(
            "Best Score: " + str(get_high_score()), True, white
        )
        display.blit(best_score_text, [width - 150, 10])

        message("Navigate with arrow keys and Enter or E to select", white, 180)
        message(
            "To visit more projects like this, go to ankurhalder.github.io",
            white,
            height // 2 - 180,
        )

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected_button_index = (selected_button_index - 1) % len(
                        button_texts
                    )
                elif event.key == pygame.K_DOWN:
                    selected_button_index = (selected_button_index + 1) % len(
                        button_texts
                    )
                elif event.key == pygame.K_RETURN or event.key == pygame.K_e:
                    if selected_button_index == 0:
                        home_page = False
                        gameLoop()
                    elif selected_button_index == 1:
                        set_high_score(0)
                    elif selected_button_index == 2:
                        pygame.quit()
                        quit()

        pygame.display.update()
        clock.tick(15)


def gameOver(score):
    game_over = True

    button_texts = ["Play Again", "Reset Best Score", "Quit"]
    selected_button_index = 0

    while game_over:
        display.fill(black)
        message("Snake Game By Ankur Halder", white, -height // 2 + 50)

        button_rects = []
        for i, text in enumerate(button_texts):
            button_rect = pygame.Rect(
                width / 2 - 100, height / 2 - 50 + i * 60, 200, 50
            )
            button_rects.append(button_rect)

            if i == selected_button_index:
                pygame.draw.rect(display, green, button_rect)
            else:
                pygame.draw.rect(display, white, button_rect)

            text_surface = font.render(text, True, black)
            text_rect = text_surface.get_rect(center=button_rect.center)
            display.blit(text_surface, text_rect)

        best_score_text = font.render(
            "Best Score: " + str(get_high_score()), True, white
        )
        display.blit(best_score_text, [width - 150, 10])

        message(
            "Navigate with arrow keys and Enter or E to select",
            white,
            height // 2 - 180,
        )
        message(
            "To visit more projects like this, go to ankurhalder.github.io",
            white,
            height // 2 - 140,
        )

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected_button_index = (selected_button_index - 1) % len(
                        button_texts
                    )
                elif event.key == pygame.K_DOWN:
                    selected_button_index = (selected_button_index + 1) % len(
                        button_texts
                    )
                elif event.key == pygame.K_RETURN or event.key == pygame.K_e:
                    if selected_button_index == 0:
                        gameLoop()
                    elif selected_button_index == 1:
                        set_high_score(0)
                    elif selected_button_index == 2:
                        pygame.quit()
                        quit()

        pygame.display.update()
        clock.tick(15)


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
            gameOver(score)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
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
            score += 10
            if score > high_score:
                high_score = score
                set_high_score(high_score)
            snake_length += 1

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

        health_box_size = 20
        health_x = 10
        health_y = 30

        for i in range(health):
            pygame.draw.rect(
                display,
                red,
                [
                    health_x + i * (health_box_size + 5),
                    health_y,
                    health_box_size,
                    health_box_size,
                ],
            )

        pygame.display.update()

        clock.tick(15)

    pygame.quit()
    quit()


homePage()
