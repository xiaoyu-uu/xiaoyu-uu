import pygame
import random
from sys import exit

# Initialize pygame
pygame.init()
back = pygame.image.load('images/background.webp')
cardBox = pygame.image.load('images/box.png')
cardBox = pygame.transform.scale(cardBox, (380, 60))
cardAll = [pygame.image.load(f'images/card{n}.webp') for n in range(1, 8)]
new_size = (50, 50)
for i in range(7):
    cardAll[i] = pygame.transform.scale(cardAll[i], new_size)

# Set window size
canvas = pygame.display.set_mode((400, 700))
pygame.display.set_caption('鱻了个鱻')

# Global variables
matrix = [[0 for _ in range(7)] for _ in range(11)]  # 11 rows
start_game = False
game_mode = None
game_time = 20  # Set timer for 20 seconds
start_ticks = None  # To track the start time
score = 0  # Initialize score
last_refresh_time = 0  # Track last refresh time
high_scores = {'easy': [], 'hard': []}  # High score records
game_over = False  # Track if the game is over

# Function to initialize the game map based on the mode
def gameMapInit(mode):
    global matrix, last_refresh_time
    row_count = 4 if mode == 'easy' else 7  # 4 rows for easy, 7 for hard
    for i in range(row_count):
        for j in range(7):
            matrix[i][j] = random.randint(1, 7)  # Fill with valid cards
    last_refresh_time = pygame.time.get_ticks()  # Initialize last refresh time

# Function to handle events
def handleEvent():
    global start_game, game_mode, score
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif e.type == pygame.MOUSEBUTTONDOWN:
            x, y = e.pos
            if not start_game:
                # Check for mode selection
                if 100 <= x <= 300 and 250 <= y <= 300:  # Easy mode
                    game_mode = 'easy'
                    global start_ticks  # Declare start_ticks as global
                    start_ticks = pygame.time.get_ticks()  # Initialize start time
                    start_game = True
                    gameMapInit(game_mode)
                elif 100 <= x <= 300 and 350 <= y <= 400:  # Hard mode
                    game_mode = 'hard'
                    start_ticks = pygame.time.get_ticks()  # Initialize start time
                    start_game = True
                    gameMapInit(game_mode)
            else:
                # Check if the restart button is clicked
                if 10 <= x <= 90 and 10 <= y <= 50:  # Restart button area
                    reset_game()
                    gameMapInit(game_mode)
                # Check if the main menu button is clicked
                elif 310 <= x <= 390 and 10 <= y <= 50:  # Main menu button area
                    reset_game()
                else:
                    for i in range(11):
                        for j in range(7):
                            if (25 + j * 50) <= x <= (25 + j * 50 + 50) and (50 + i * 50) <= y <= (50 + i * 50 + 50):
                                if matrix[i][j] != 0:
                                    move_card_to_box(i, j)
                                    break

# Function to move a card to the box
def move_card_to_box(i, j):
    global matrix, score
    # Find the first empty slot in the last row (11th row)
    for k in range(7):
        if matrix[10][k] == 0:  # 11th row index is 10
            matrix[10][k] = matrix[i][j]
            matrix[i][j] = 0
            check_and_remove_cards(10, k)
            check_game_over()  # Check if game over after moving a card
            break

# Function to check and remove cards
def check_and_remove_cards(row, col):
    global matrix, score
    # Check for card elimination
    card_id = matrix[row][col]
    if col > 0 and matrix[row][col - 1] == card_id:
        matrix[row][col] = 0
        matrix[row][col - 1] = 0
        score += 1  # Increment score
    elif col < 6 and matrix[row][col + 1] == card_id:
        matrix[row][col] = 0
        matrix[row][col + 1] = 0
        score += 1  # Increment score

# Function to check if the game is over
def check_game_over():
    global start_game, game_over
    # Check if the last row is full
    if all(matrix[10][k] != 0 for k in range(7)):
        record_high_score(score)  # Record the score before ending
        start_game = False
        game_over = True  # Set game over status
        reset_score()  # Reset score when game ends

# Function to reset the score
def reset_score():
    global score
    score = 0  # Reset score when game ends

# Function to record high scores
def record_high_score(score):
    if game_mode and score > 0:  # Only record if score is greater than 0
        if score not in high_scores[game_mode]:  # Prevent duplicates
            high_scores[game_mode].append(score)
            high_scores[game_mode].sort(reverse=True)  # Sort in descending order
            if len(high_scores[game_mode]) > 5:  # Keep only top 5 scores
                high_scores[game_mode] = high_scores[game_mode][:5]

# Function to reset the game state
def reset_game():
    global start_game, matrix, game_mode, score, game_over
    start_game = False
    game_mode = None
    reset_score()  # Reset score
    game_over = False  # Reset game over status
    matrix = [[0 for _ in range(7)] for _ in range(11)]  # Reset the matrix

# Function to draw the mode selection
def drawModeSelection():
    font = pygame.font.Font(None, 48)
    easy_text = font.render('EASY', True, (0, 0, 0))
    hard_text = font.render('HARD', True, (0, 0, 0))
    canvas.blit(easy_text, (150, 250))
    canvas.blit(hard_text, (150, 350))
    title = pygame.image.load('images/title.png')
    title = pygame.transform.scale(title, (400, 300))
    canvas.blit(title, (10, 50))

# Function to draw the buttons
def drawButtons():
    # Restart Button
    restart_button = pygame.Rect(10, 10, 80, 40)
    pygame.draw.rect(canvas, (255, 0, 0), restart_button)
    font = pygame.font.Font(None, 24)
    restart_text = font.render('RESTART', True, (255, 255, 255))
    restart_rect = restart_text.get_rect(center=restart_button.center)
    canvas.blit(restart_text, restart_rect)

    # Main Menu Button
    main_menu_button = pygame.Rect(310, 10, 80, 40)
    pygame.draw.rect(canvas, (0, 0, 255), main_menu_button)
    menu_text = font.render('MENU', True, (255, 255, 255))
    menu_rect = menu_text.get_rect(center=main_menu_button.center)
    canvas.blit(menu_text, menu_rect)

# Function to draw the cards on the screen
def drawCards():
    x = 25
    y = 50
    for i in range(11):
        x = 25
        for j in range(7):
            card_id = matrix[i][j]
            if card_id != 0:
                canvas.blit(cardAll[card_id - 1], (x, y))
            x += 50
        y += 50

# Function to draw the game over screen
def drawGameOver():
    canvas.fill((255, 255, 255))  # Clear screen for game over
    font = pygame.font.Font(None, 48)
    text = font.render('GAME OVER', True, (255, 0, 0))
    text_rect = text.get_rect(center=(200, 250))
    canvas.blit(text, text_rect)

    instructions_text = font.render('Click to return', True, (0, 0, 0))
    instructions_rect = instructions_text.get_rect(center=(200, 350))
    canvas.blit(instructions_text, instructions_rect)

    drawHighScores()  # Draw high scores

# Function to draw the timer
def drawTimer():
    elapsed_time = (pygame.time.get_ticks() - start_ticks) // 1000  # Calculate elapsed time
    remaining_time = max(0, game_time - elapsed_time)  # Calculate remaining time
    font = pygame.font.Font(None, 36)
    timer_text = font.render(f'Time Left: {remaining_time}s', True, (0, 0, 0))
    canvas.blit(timer_text, (10, 620))  # Position at the bottom
    return remaining_time  # Return remaining time for checks

# Function to draw the score
def drawScore():
    font = pygame.font.Font(None, 36)
    score_text = font.render(f'Score: {score}', True, (0, 0, 0))
    canvas.blit(score_text, (300, 620))  # Position at the bottom right

# Function to draw high scores
def drawHighScores():
    font = pygame.font.Font(None, 36)
    mode_text = f'{game_mode.capitalize()} Mode High Scores'
    mode_surface = font.render(mode_text, True, (0, 0, 0))
    canvas.blit(mode_surface, (100, 450))
    for idx, s in enumerate(high_scores[game_mode][:5]):
        score_surface = font.render(f'{idx + 1}. {s}', True, (0, 0, 0))
        canvas.blit(score_surface, (150, 490 + idx * 30))

# Main game loop
while True:
    canvas.fill((255, 255, 255))  # Fill background with white
    canvas.blit(back, (0, 0))  # Draw background

    if not start_game:
        drawModeSelection()  # Draw mode selection
    else:
        drawCards()
        canvas.blit(cardBox, (10, 550))
        for k in range(7):
            if matrix[10][k] != 0:
                canvas.blit(cardAll[matrix[10][k] - 1], (10 + k * 50, 550))

        drawButtons()  # Draw the buttons
        remaining_time = drawTimer()  # Draw the timer
        drawScore()  # Draw the score

        # Refresh cards every 3 seconds without resetting the score or timer
        if pygame.time.get_ticks() - last_refresh_time > 3000:
            gameMapInit(game_mode)  # Refresh cards
            last_refresh_time = pygame.time.get_ticks()  # Update last refresh time

        # Check if game time has run out
        if remaining_time <= 0:  # Check if time is up
            record_high_score(score)  # Record high score at end of time
            check_game_over()  # Check if game over

    # Check if game is over (either time runs out or last row is full)
    if not start_game and game_over:
        drawGameOver()
        # Wait for click to return to mode selection
        for e in pygame.event.get():
            if e.type == pygame.MOUSEBUTTONDOWN:
                reset_game()

    handleEvent()  # Call the event handling function
    pygame.display.update()

