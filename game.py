import pygame
import sys

# Constants
ROW_COUNT = 6
COLUMN_COUNT = 7
SQUARE_SIZE = 100
WINDOW_WIDTH = COLUMN_COUNT * SQUARE_SIZE
WINDOW_HEIGHT = (ROW_COUNT + 1) * SQUARE_SIZE  # +1 for the header row

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

# Initialize Pygame
pygame.init()

# Create the game window
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

# Initialize the game board
board = [[0] * COLUMN_COUNT for _ in range(ROW_COUNT)]

# Initialize player and game state variables
current_player = 1
game_state = "playing"  # "playing", "won", or "restart"

# Initialize posx with a default value
posx = WINDOW_WIDTH // 2

# Function to draw the board
def draw_board(board):
    for row in range(ROW_COUNT):
        for col in range(COLUMN_COUNT):
            pygame.draw.rect(window, BLUE, (col * SQUARE_SIZE, (row + 1) * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
            pygame.draw.circle(window, BLACK, (col * SQUARE_SIZE + SQUARE_SIZE // 2, (row + 1) * SQUARE_SIZE + SQUARE_SIZE // 2), SQUARE_SIZE // 2 - 5)
            if board[row][col] == 1:
                pygame.draw.circle(window, RED, (col * SQUARE_SIZE + SQUARE_SIZE // 2, (row + 1) * SQUARE_SIZE + SQUARE_SIZE // 2), SQUARE_SIZE // 2 - 5)
            elif board[row][col] == 2:
                pygame.draw.circle(window, YELLOW, (col * SQUARE_SIZE + SQUARE_SIZE // 2, (row + 1) * SQUARE_SIZE + SQUARE_SIZE // 2), SQUARE_SIZE // 2 - 5)

# Function to drop a piece in a column
def drop_piece(board, row, col, player):
    board[row][col] = player

# Function to check if a move is valid
def is_valid_move(board, col):
    return board[0][col] == 0

# Function to get the next available row in a column
def get_next_open_row(board, col):
    for r in range(ROW_COUNT - 1, -1, -1):
        if board[r][col] == 0:
            return r

# Function to check if a player has won
def check_win(board, player):
    # Check horizontally
    for row in range(ROW_COUNT):
        for col in range(COLUMN_COUNT - 3):
            if board[row][col] == player and board[row][col + 1] == player and board[row][col + 2] == player and board[row][col + 3] == player:
                return True

    # Check vertically
    for row in range(ROW_COUNT - 3):
        for col in range(COLUMN_COUNT):
            if board[row][col] == player and board[row + 1][col] == player and board[row + 2][col] == player and board[row + 3][col] == player:
                return True

    # Check diagonally (from bottom-left to top-right)
    for row in range(3, ROW_COUNT):
        for col in range(COLUMN_COUNT - 3):
            if board[row][col] == player and board[row - 1][col + 1] == player and board[row - 2][col + 2] == player and board[row - 3][col + 3] == player:
                return True

    # Check diagonally (from bottom-right to top-left)
    for row in range(3, ROW_COUNT):
        for col in range(3, COLUMN_COUNT):
            if board[row][col] == player and board[row - 1][col - 1] == player and board[row - 2][col - 2] == player and board[row - 3][col - 3] == player:
                return True

# Function to display a message on the screen
def draw_message(message):
    font = pygame.font.Font(None, 36)
    text = font.render(message, True, WHITE)
    window.blit(text, (20, 10))

# Draw the initial board
draw_board(board)
pygame.display.update()

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if game_state == "playing":
            if event.type == pygame.MOUSEMOTION:
                pygame.draw.rect(window, BLACK, (0, 0, WINDOW_WIDTH, SQUARE_SIZE))
                posx = event.pos[0]
                posy = SQUARE_SIZE // 2
                pygame.draw.circle(window, RED if current_player == 1 else YELLOW, (posx, posy), SQUARE_SIZE // 2 - 5)
                pygame.display.update()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pygame.draw.rect(window, BLACK, (0, 0, WINDOW_WIDTH, SQUARE_SIZE))
                col = posx // SQUARE_SIZE

                if is_valid_move(board, col):
                    row = get_next_open_row(board, col)
                    drop_piece(board, row, col, current_player)

                    if check_win(board, current_player):
                        winner_message = f"Player {current_player} wins! Press Space to restart."
                        draw_message(winner_message)
                        game_state = "won"
                    else:
                        current_player = 3 - current_player
                    draw_board(board)
                    pygame.display.update()

            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_state = "restart"

        elif game_state == "won":
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                board = [[0] * COLUMN_COUNT for _ in range(ROW_COUNT)]
                current_player = 1
                pygame.draw.rect(window, BLACK, (0, 0, WINDOW_WIDTH, WINDOW_HEIGHT))
                draw_board(board)
                pygame.display.update()
                game_state = "playing"

        elif game_state == "restart":
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                board = [[0] * COLUMN_COUNT for _ in range(ROW_COUNT)]
                current_player = 1
                pygame.draw.rect(window, BLACK, (0, 0, WINDOW_WIDTH, WINDOW_HEIGHT))
                draw_board(board)
                pygame.display.update()
                game_state = "playing"
