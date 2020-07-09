import pygame
import inspect, os, sys
import random


pygame.init()

if getattr(sys, "frozen", False):
    # frozen
    DIRECTORY = os.path.dirname(sys.executable)
    IMAGES = DIRECTORY
else:
    DIRECTORY = os.path.dirname(os.path.abspath(__file__))
    IMAGES = os.path.join(DIRECTORY, "images")

print("\n\n" + IMAGES + "\n\n")
SMALL_FONT = pygame.font.SysFont("comicsansms", 25)
MEDIUM_FONT = pygame.font.SysFont("comicsansms", 50)
LARGE_FONT = pygame.font.SysFont("comicsansms", 80)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)

DISPLAY_X = 800
DISPLAY_Y = 600

gameDisplay = pygame.display.set_mode((DISPLAY_X, DISPLAY_Y))
pygame.display.set_caption("Snake")

snake_img = pygame.image.load(os.path.join(IMAGES, "snake.png"))
apple_img = pygame.image.load(os.path.join(IMAGES, "apple.png"))
direction = "right"

clock = pygame.time.Clock()

FPS = 30
BLOCK_SIZE = 20
APPLE_SIZE = 20
SNAKE_SPEED = BLOCK_SIZE
START_LENGTH = 10
GROWTH_RATE = 5


def text_objects(text, color, font):
    textSurface = font.render(text, True, color)
    return textSurface, textSurface.get_rect()


def message_to_screen(msg, color, font, y_displace=0):
    textSurface, textRect = text_objects(msg, color, font)
    textRect.center = (DISPLAY_X / 2, DISPLAY_Y / 2 + y_displace)
    gameDisplay.blit(textSurface, textRect)


def score(score):
    text = SMALL_FONT.render("Score: " + str(score), True, YELLOW)
    gameDisplay.blit(text, [0, 0])


def apple_gen():
    apple_x = round(random.randrange(0, DISPLAY_X - APPLE_SIZE))
    apple_y = round(random.randrange(0, DISPLAY_Y - APPLE_SIZE))
    return apple_x, apple_y


def draw_snake(snake):
    if direction == "up":
        head = pygame.transform.rotate(snake_img, 0)
    if direction == "right":
        head = pygame.transform.rotate(snake_img, 270)
    if direction == "down":
        head = pygame.transform.rotate(snake_img, 180)
    if direction == "left":
        head = pygame.transform.rotate(snake_img, 90)
    gameDisplay.blit(head, (snake[-1][0], snake[-1][1]))
    for pos in snake[:-1]:
        pygame.draw.rect(
            gameDisplay, GREEN, [pos[0], pos[1], BLOCK_SIZE, BLOCK_SIZE]
        )


def game_intro():
    intro = True

    while intro:
        gameDisplay.fill(BLACK)
        message_to_screen("Welcome to Snake!", GREEN, LARGE_FONT, -100)
        message_to_screen(
            "Control the snake with the arrow keys.", YELLOW, SMALL_FONT, -20
        )
        message_to_screen(
            "The objective of the game is to eat apples.",
            YELLOW,
            SMALL_FONT,
            10,
        )
        message_to_screen(
            "The more apples you eat, the longer you get.",
            YELLOW,
            SMALL_FONT,
            40,
        )
        message_to_screen(
            "If you run into yourself or the edges you die.",
            YELLOW,
            SMALL_FONT,
            70,
        )
        message_to_screen("Press c to start!", WHITE, SMALL_FONT, 180)
        pygame.display.update()
        clock.tick(5)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    intro = False


def pause():
    paused = True
    message_to_screen("PAUSED", YELLOW, LARGE_FONT, -100)
    message_to_screen(
        "Press C to continue, or Q to quit.", WHITE, SMALL_FONT, 25
    )
    pygame.display.update()
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    paused = False

                elif event.key == pygame.K_q:
                    pygame.quit()
                    quit()

        # gameDisplay.fill(BLACK)
        clock.tick(5)


def gameLoop():
    global direction
    direction = "right"
    gameExit = False
    gameOver = False

    snake = []
    snake_length = START_LENGTH

    lead_x = DISPLAY_X / 2
    lead_y = DISPLAY_Y / 2

    lead_dx = SNAKE_SPEED
    lead_dy = 0

    apple_x, apple_y = apple_gen()

    while not gameExit:
        clock.tick(FPS)
        if gameOver == True:
            message_to_screen("GAME OVER!", RED, LARGE_FONT, y_displace=-50)
            message_to_screen(
                "Press C to play again or Q to quit.",
                WHITE,
                SMALL_FONT,
                y_displace=50,
            )
            pygame.display.update()

        while gameOver == True:
            # gameDisplay.fill(BLACK)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    gameOver = False
                    gameExit = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        gameExit = True
                        gameOver = False
                    elif event.key == pygame.K_c:
                        gameLoop()

        # EVENT HANDLER
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameExit = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT or event.key == pygame.K_h:
                    if not direction == "right":
                        direction = "left"
                        lead_dx = -SNAKE_SPEED
                        lead_dy = 0
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_l:
                    if not direction == "left":
                        direction = "right"
                        lead_dx = SNAKE_SPEED
                        lead_dy = 0
                elif event.key == pygame.K_UP or event.key == pygame.K_k:
                    if not direction == "down":
                        direction = "up"
                        lead_dy = -SNAKE_SPEED
                        lead_dx = 0
                elif event.key == pygame.K_DOWN or event.key == pygame.K_r:
                    if not direction == "up":
                        direction = "down"
                        lead_dy = SNAKE_SPEED
                        lead_dx = 0
                elif event.key == pygame.K_p:
                    pause()

        if (
            lead_x >= DISPLAY_X
            or lead_x < 0
            or lead_y >= DISPLAY_Y
            or lead_y < 0
        ):
            gameOver = True

        lead_x += lead_dx
        lead_y += lead_dy

        # GRAPHICS
        gameDisplay.fill(BLACK)

        gameDisplay.blit(apple_img, (apple_x, apple_y))
        snakeHead = []
        snakeHead.append(lead_x)
        snakeHead.append(lead_y)
        if len(snake) >= snake_length:
            del snake[0]

        if len(snake) > 1 and snakeHead in snake[:-1]:
            gameOver = True

        snake.append(snakeHead)
        draw_snake(snake)
        score((snake_length - START_LENGTH) // GROWTH_RATE)
        pygame.display.update()

        intersects_x = (apple_x <= lead_x <= apple_x + APPLE_SIZE) or (
            apple_x <= lead_x + BLOCK_SIZE <= apple_x + APPLE_SIZE
        )
        intersects_y = (apple_y <= lead_y <= apple_y + APPLE_SIZE) or (
            apple_y <= lead_y + BLOCK_SIZE < apple_y + APPLE_SIZE
        )

        if intersects_x and intersects_y:
            snake_length += GROWTH_RATE
            apple_x, apple_y = apple_gen()

    # QUIT
    pygame.quit()
    quit()


game_intro()
gameLoop()
