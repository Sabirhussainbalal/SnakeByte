import pygame
import random
import os

# Initialize Pygame and music
pygame.mixer.init()
pygame.mixer.music.load('Interstellar.mp3')
pygame.mixer.music.play(-1)  # Loop the music indefinitely

pygame.init()

# Set up display
screen_width = 850
screen_height = 500
gameWindow = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("My First Game: Snakes")
clock = pygame.time.Clock()
fps = 60

# Load and scale images
def load_and_scale_image(file_name, width, height):
    try:
        image = pygame.image.load(file_name)
        image = pygame.transform.scale(image, (width, height))
        return image
    except pygame.error as e:
        print(f"Unable to load image: {file_name}. Error: {e}")
        raise SystemExit(e)

welcome_img = load_and_scale_image('welcome.png', screen_width, screen_height)
current_img = load_and_scale_image('current.jpg', screen_width, screen_height)
game_over_img = load_and_scale_image('game_over.png', screen_width, screen_height)

# Colors
black = (0, 0, 0)
red = (250, 0, 0)
white = (250, 250, 250)

font = pygame.font.Font(None, 35)  # Font size for score display

def text_screen(text, color, x, y):
    screen_text = font.render(text, True, color)
    gameWindow.blit(screen_text, [x, y])

def show_welcome_screen():
    gameWindow.blit(welcome_img, (0, 0))  # Draw welcome image
    text_screen("Press Enter to Start", red, 5, 5)
    pygame.display.update()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    waiting = False
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    exit()

def get_highscore():
    try:
        with open("highscore.txt", "r") as f:
            return int(f.read())
    except (FileNotFoundError, ValueError):
        return 0

def save_highscore(score):
    with open("highscore.txt", "w") as f:
        f.write(str(score))

def game_loop():
    # Initialize snake parameters
    snake_x = 45
    snake_y = 45
    velocity_x = 0
    velocity_y = 0
    init_velocity = 3
    snake_size_x = 15
    snake_size_y = 15

    # Initialize food parameters
    food_x = random.randint(20, screen_width - 20)
    food_y = random.randint(20, screen_height - 20)
    food_size = 10

    # Initialize score and snake list
    score = 0
    highscore = get_highscore()
    snk_list = []
    snk_length = 1

    game_exit = False
    game_over = False

    while not game_exit:
        if game_over:
            gameWindow.blit(game_over_img, (0, 0))  # Draw game over image
            if score > highscore:
                save_highscore(score)
            text_screen(f"Score: {score}", red, 5, 5)
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_exit = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        return  # Restart the game by returning to the main loop
                    elif event.key == pygame.K_ESCAPE:
                        game_exit = True
        else:
            gameWindow.blit(current_img, (0, 0))  # Draw current image

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_exit = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        velocity_x = init_velocity
                        velocity_y = 0
                    elif event.key == pygame.K_LEFT:
                        velocity_x = -init_velocity
                        velocity_y = 0
                    elif event.key == pygame.K_UP:
                        velocity_y = -init_velocity
                        velocity_x = 0
                    elif event.key == pygame.K_DOWN:
                        velocity_y = init_velocity
                        velocity_x = 0

            snake_x += velocity_x
            snake_y += velocity_y

            # Check for collision with food
            if abs(snake_x - food_x) < snake_size_x and abs(snake_y - food_y) < snake_size_y:
                score += 1
                food_x = random.randint(20, screen_width - 20)
                food_y = random.randint(20, screen_height - 20)
                snk_length += 7

            # Update snake's position
            head = [snake_x, snake_y]
            snk_list.append(head)
            if len(snk_list) > snk_length:
                del snk_list[0]

            # Check for collisions
            if head in snk_list[:-1] or snake_x >= screen_width or snake_x < 0 or snake_y >= screen_height or snake_y < 0:
                game_over = True

            # Draw everything
            gameWindow.blit(current_img, (0, 0))  # Ensure current image is drawn first
            text_screen(f"Score: {score} | High Score: {highscore}", red, 5, 5)
            pygame.draw.rect(gameWindow, red, (food_x, food_y, food_size, food_size))  # Draw food

            # Draw snake
            for segment in snk_list:
                pygame.draw.rect(gameWindow, black, (segment[0], segment[1], snake_size_x, snake_size_y))

            pygame.display.update()
            clock.tick(fps)

while True:
    show_welcome_screen()
    game_loop()
