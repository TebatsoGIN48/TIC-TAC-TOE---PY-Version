import pygame
import sys

# Initialize Pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 600, 600
LINE_WIDTH = 5
BOARD_COLOR = (28, 170, 156)
LINE_COLOR = (255, 255, 255)  # Sparkling white
X_COLOR = (0, 255, 0)  # Green
O_COLOR = (255, 0, 0)  # Red
BG_COLOR = (22, 22, 22)  # Light blue-black

# Set up display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic Tac Toe")
screen.fill(BG_COLOR)

# Fonts
FONT = pygame.font.Font(None, 100)
MESSAGE_FONT = pygame.font.Font(None, 50)

# Sounds
place_sound = pygame.mixer.Sound("place.wav")
win_sound = pygame.mixer.Sound("win.wav")
draw_sound = pygame.mixer.Sound("draw.wav")

# Board
board = [[" " for _ in range(3)] for _ in range(3)]

# Draw grid
def draw_grid():
    pygame.draw.line(screen, LINE_COLOR, (WIDTH // 3, 0), (WIDTH // 3, HEIGHT), LINE_WIDTH)
    pygame.draw.line(screen, LINE_COLOR, (2 * WIDTH // 3, 0), (2 * WIDTH // 3, HEIGHT), LINE_WIDTH)
    pygame.draw.line(screen, LINE_COLOR, (0, HEIGHT // 3), (WIDTH, HEIGHT // 3), LINE_WIDTH)
    pygame.draw.line(screen, LINE_COLOR, (0, 2 * HEIGHT // 3), (WIDTH, 2 * HEIGHT // 3), LINE_WIDTH)

# Draw X or O with animation
def draw_mark(row, col, mark):
    center_x = col * WIDTH // 3 + WIDTH // 6
    center_y = row * HEIGHT // 3 + HEIGHT // 6
    for i in range(10):  # Animation effect
        if mark == "X":
            pygame.draw.line(screen, X_COLOR, (center_x - 50, center_y - 50), (center_x - 50 + i * 10, center_y - 50 + i * 10), LINE_WIDTH)
            pygame.draw.line(screen, X_COLOR, (center_x + 50, center_y - 50), (center_x + 50 - i * 10, center_y - 50 + i * 10), LINE_WIDTH)
        elif mark == "O":
            pygame.draw.circle(screen, O_COLOR, (center_x, center_y), 5 * i, LINE_WIDTH)
        pygame.display.update()
        pygame.time.delay(20)

# Display message
def display_message(message):
    text = MESSAGE_FONT.render(message, True, (233, 196, 196))
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.fill(BG_COLOR)
    screen.blit(text, text_rect)
    pygame.display.update()
    pygame.time.wait(2000)

# Check for winner
def check_winner():
    # Check rows, columns, and diagonals
    for row in range(3):
        if board[row][0] == board[row][1] == board[row][2] != " ":
            return board[row][0]
    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] != " ":
            return board[0][col]
    if board[0][0] == board[1][1] == board[2][2] != " ":
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] != " ":
        return board[0][2]
    return None

# Check for draw
def is_draw():
    return all(board[row][col] != " " for row in range(3) for col in range(3))

# Main game loop
def main():
    draw_grid()
    current_player = "X"
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                clicked_row = mouse_y // (HEIGHT // 3)
                clicked_col = mouse_x // (WIDTH // 3)

                if board[clicked_row][clicked_col] == " ":
                    board[clicked_row][clicked_col] = current_player
                    place_sound.play()
                    draw_mark(clicked_row, clicked_col, current_player)

                    winner = check_winner()
                    if winner:
                        win_sound.play()
                        display_message(f"Player {winner} wins!")
                        running = False
                    elif is_draw():
                        draw_sound.play()
                        display_message("It's a draw!")
                        running = False
                    else:
                        current_player = "O" if current_player == "X" else "X"

        pygame.display.update()

    # Replay option
    replay_text = MESSAGE_FONT.render("Press R to Replay or Q to Quit", True, (221, 213, 213))
    replay_rect = replay_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))
    screen.blit(replay_text, replay_rect)
    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    board[:] = [[" " for _ in range(3)] for _ in range(3)]
                    screen.fill(BG_COLOR)
                    draw_grid()
                    main()
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()

if __name__ == "__main__":
    main()
