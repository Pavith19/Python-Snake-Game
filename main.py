# -----------------------------------------------
# Developed by Pavith Bambaravanage
# GitHub Repository: https://github.com/Pavith19/Python-Snake-Game.git
# -----------------------------------------------

import pygame
import time
import random
import os
import json

pygame.init()  # Initialize pygame

# Colors
WHITE = (255, 255, 255)
BLACK = (36, 36, 36)
RED = (213, 50, 80)
GREEN = (0, 255, 0)
BLUE = (50, 153, 213)
GRAY = (100, 100, 100)
YELLOW = (255, 255, 0)
LIGHT_GREEN = (150, 255, 150)

# Sizes for game window
DISPLAY_WIDTH = 600
DISPLAY_HEIGHT = 500

# Try to load icon, if file exists
try:
    icon = pygame.image.load("snakeicon.ico")
    pygame.display.set_icon(icon)
except:
    pass  # Continue without icon if not found

# Apply size to the game window
display = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
pygame.display.set_caption('Enhanced Snake Game')

clock = pygame.time.Clock()

# Game settings
SNAKE_BLOCK = 10
DEFAULT_SPEED = 15
MAX_SPEED = 30
MIN_SPEED = 5

# Fonts
score_font = pygame.font.SysFont("arial", 15)
title_font = pygame.font.SysFont("bahnschrift", 40)
message_font = pygame.font.SysFont("bahnschrift", 25)
info_font = pygame.font.SysFont("arial", 18)
small_font = pygame.font.SysFont("arial", 14)

# Game states
MAIN_MENU = 0
INSTRUCTIONS = 1
SPEED_SELECTION = 2
PLAYING = 3
PAUSED = 4
GAME_OVER = 5

# High scores file
HIGH_SCORES_FILE = "snake_high_scores.json"

def load_high_scores():
    """Load high scores from file"""
    if os.path.exists(HIGH_SCORES_FILE):
        try:
            with open(HIGH_SCORES_FILE, 'r') as file:
                return json.load(file)
        except:
            return []
    return []

def save_high_score(score, speed):
    """Save a new high score"""
    high_scores = load_high_scores()
    high_scores.append({"score": score, "speed": speed, "date": time.strftime("%Y-%m-%d")})
    
    # Sort by score (highest first)
    high_scores = sorted(high_scores, key=lambda x: x["score"], reverse=True)
    
    # Keep only top 10
    high_scores = high_scores[:10]
    
    with open(HIGH_SCORES_FILE, 'w') as file:
        json.dump(high_scores, file)

def draw_text(text, font, color, x, y, centered=False):
    """Helper function to draw text"""
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    
    if centered:
        text_rect.center = (x, y)
    else:
        text_rect.topleft = (x, y)
        
    display.blit(text_surface, text_rect)
    return text_rect

def draw_button(text, x, y, width, height, inactive_color, active_color, text_color=BLACK):
    """Draw a button and return True if clicked"""
    mouse_pos = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    
    if x < mouse_pos[0] < x + width and y < mouse_pos[1] < y + height:
        pygame.draw.rect(display, active_color, (x, y, width, height))
        if click[0] == 1:
            return True
    else:
        pygame.draw.rect(display, inactive_color, (x, y, width, height))
        
    text_surf = message_font.render(text, True, text_color)
    text_rect = text_surf.get_rect()
    text_rect.center = ((x + (width / 2)), (y + (height / 2)))
    display.blit(text_surf, text_rect)
    
    return False

def draw_score(score):
    """Render the score in the top-left corner"""
    draw_text(f" Score: {score}", score_font, WHITE, 10, 10)

def draw_speed(speed):
    """Render the current speed in the top-right corner"""
    draw_text(f"Speed: {speed}", score_font, WHITE, DISPLAY_WIDTH - 100, 10)

def draw_snake(snake_block, snake_list):
    """Render the snake's body"""
    for i, segment in enumerate(snake_list):
        # Head is slightly different color
        color = LIGHT_GREEN if i == len(snake_list) - 1 else GREEN
        pygame.draw.rect(display, color, [
            segment[0], segment[1], snake_block, snake_block], border_radius=3)

def draw_food(x, y, block_size):
    """Draw the food with a slight glow effect"""
    pygame.draw.rect(display, RED, [x, y, block_size, block_size], border_radius=5)
    # Add a small glow effect (smaller inner rectangle)
    pygame.draw.rect(display, (255, 100, 100), [x+2, y+2, block_size-4, block_size-4], border_radius=3)

def draw_controls_info():
    """Display control information at the bottom of the screen"""
    controls = "Controls: WASD = Movement | P = Pause | R = Restart | Q = Quit"
    draw_text(controls, small_font, GRAY, DISPLAY_WIDTH // 2, DISPLAY_HEIGHT - 20, True)

def show_main_menu():
    """Display the main menu screen"""
    display.fill(BLACK)
    
    # Title
    draw_text("SNAKE GAME", title_font, GREEN, DISPLAY_WIDTH // 2, 80, True)
    
    button_width = 200
    button_height = 50
    button_x = DISPLAY_WIDTH // 2 - button_width // 2
    
    # Draw buttons
    play_clicked = draw_button("Play Game", button_x, 180, button_width, button_height, GREEN, LIGHT_GREEN)
    speed_clicked = draw_button("Set Speed", button_x, 250, button_width, button_height, BLUE, (100, 200, 255))
    instructions_clicked = draw_button("Instructions", button_x, 320, button_width, button_height, YELLOW, (255, 255, 150))
    high_scores_clicked = draw_button("High Scores", button_x, 390, button_width, button_height, RED, (255, 150, 150))
    
    # Version info
    draw_text("v2.0", small_font, GRAY, DISPLAY_WIDTH - 30, DISPLAY_HEIGHT - 20)
    
    pygame.display.update()
    return play_clicked, speed_clicked, instructions_clicked, high_scores_clicked

def show_instructions():
    """Display the game instructions"""
    display.fill(BLACK)
    
    draw_text("HOW TO PLAY", title_font, YELLOW, DISPLAY_WIDTH // 2, 50, True)
    
    instructions = [
        "1. Use WASD keys to control the snake's direction",
        "2. Eat the red food to grow and increase your score",
        "3. Avoid hitting the walls or your own tail",
        "4. Press P to pause the game at any time",
        "5. Press R to restart if you're not doing well",
        "6. Try to beat your high score!"
    ]
    
    for i, line in enumerate(instructions):
        draw_text(line, info_font, WHITE, 50, 120 + i * 40)
    
    # Back button
    back_clicked = draw_button("Back to Menu", DISPLAY_WIDTH // 2 - 100, 400, 200, 50, GREEN, LIGHT_GREEN)
    
    pygame.display.update()
    return back_clicked

def show_speed_selection(current_speed):
    """Display speed selection screen"""
    display.fill(BLACK)
    
    draw_text("SELECT GAME SPEED", title_font, BLUE, DISPLAY_WIDTH // 2, 50, True)
    draw_text(f"Current Speed: {current_speed}", message_font, WHITE, DISPLAY_WIDTH // 2, 120, True)
    
    # Speed explanation
    draw_text("Lower = Easier, Higher = Harder", info_font, GRAY, DISPLAY_WIDTH // 2, 160, True)
    
    button_width = 60
    button_height = 60
    
    # Speed buttons
    speeds = [5, 10, 15, 20, 25, 30]
    selected_speed = current_speed
    
    for i, speed in enumerate(speeds):
        x = 100 + i * (button_width + 20)
        y = 220
        
        # Highlight current selection
        color = LIGHT_GREEN if speed == current_speed else GREEN
        hover_color = (200, 255, 200) if speed == current_speed else LIGHT_GREEN
        
        if draw_button(str(speed), x, y, button_width, button_height, color, hover_color):
            selected_speed = speed
    
    # Back button
    back_clicked = draw_button("Save & Back", DISPLAY_WIDTH // 2 - 100, 350, 200, 50, BLUE, (100, 200, 255))
    
    pygame.display.update()
    return selected_speed, back_clicked

def show_high_scores():
    """Display high scores screen"""
    display.fill(BLACK)
    
    draw_text("HIGH SCORES", title_font, RED, DISPLAY_WIDTH // 2, 50, True)
    
    high_scores = load_high_scores()
    
    if not high_scores:
        draw_text("No high scores yet. Play the game to set a record!", info_font, 
                  WHITE, DISPLAY_WIDTH // 2, 200, True)
    else:
        # Headers
        draw_text("Rank", info_font, YELLOW, 100, 120)
        draw_text("Score", info_font, YELLOW, 220, 120)
        draw_text("Speed", info_font, YELLOW, 340, 120)
        draw_text("Date", info_font, YELLOW, 450, 120)
        
        # Draw divider line
        pygame.draw.line(display, GRAY, (80, 145), (520, 145), 2)
        
        # List scores
        for i, score_data in enumerate(high_scores[:10]):
            y_pos = 170 + i * 30
            
            # Rank
            draw_text(f"#{i+1}", info_font, WHITE, 100, y_pos)
            
            # Score
            draw_text(str(score_data["score"]), info_font, WHITE, 220, y_pos)
            
            # Speed
            draw_text(str(score_data["speed"]), info_font, WHITE, 340, y_pos)
            
            # Date
            draw_text(score_data["date"], info_font, WHITE, 450, y_pos)
    
    # Back button
    back_clicked = draw_button("Back to Menu", DISPLAY_WIDTH // 2 - 100, 400, 200, 50, GREEN, LIGHT_GREEN)
    
    pygame.display.update()
    return back_clicked

def show_game_over_screen(final_score, current_speed, high_scores):
    """Display the game over screen with final score"""
    display.fill(BLACK)
    
    draw_text("Game Over!", title_font, RED, DISPLAY_WIDTH // 2, 100, True)
    draw_text(f"Final Score: {final_score}", message_font, WHITE, DISPLAY_WIDTH // 2, 170, True)
    
    # Check if this is a high score
    is_high_score = False
    if not high_scores or final_score > min(score["score"] for score in high_scores):
        if len(high_scores) < 10 or final_score > min(score["score"] for score in high_scores):
            is_high_score = True
            draw_text("NEW HIGH SCORE!", message_font, YELLOW, DISPLAY_WIDTH // 2, 210, True)
    
    button_width = 200
    button_height = 50
    button_x = DISPLAY_WIDTH // 2 - button_width // 2
    
    # Draw buttons
    play_again_clicked = draw_button("Play Again", button_x, 270, button_width, button_height, GREEN, LIGHT_GREEN)
    main_menu_clicked = draw_button("Main Menu", button_x, 340, button_width, button_height, BLUE, (100, 200, 255))
    
    pygame.display.update()
    return play_again_clicked, main_menu_clicked, is_high_score

def game_loop(current_speed):
    """Main game loop"""
    game_state = PLAYING
    game_exit = False
    
    # Snake initial position
    x1 = DISPLAY_WIDTH / 2
    y1 = DISPLAY_HEIGHT / 2
    
    x1_change = 0
    y1_change = 0
    
    snake_list = []
    snake_length = 1
    
    # Generate initial food position
    foodx = round(random.randrange(0, DISPLAY_WIDTH - SNAKE_BLOCK) / 10.0) * 10.0
    foody = round(random.randrange(0, DISPLAY_HEIGHT - SNAKE_BLOCK) / 10.0) * 10.0
    
    # Direction flags to prevent 180° turns
    going_right = False
    going_left = False  
    going_up = False
    going_down = False
    
    last_direction_change = pygame.time.get_ticks()
    direction_change_threshold = 50  # ms
    
    # Main game loop
    while not game_exit:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "QUIT", 0
                
            if event.type == pygame.KEYDOWN:
                current_time = pygame.time.get_ticks()
                
                # Game state controls
                if event.key == pygame.K_p:  # Pause game
                    if game_state == PLAYING:
                        game_state = PAUSED
                    elif game_state == PAUSED:
                        game_state = PLAYING
                
                elif event.key == pygame.K_r:  # Restart game
                    return "RESTART", 0
                
                elif event.key == pygame.K_q:  # Quit to menu
                    return "MENU", 0
                
                elif event.key == pygame.K_SPACE and game_state == GAME_OVER:
                    return "RESTART", 0
                
                # Movement controls - only process if time threshold passed and not paused
                if game_state == PLAYING and current_time - last_direction_change > direction_change_threshold:
                    if event.key == pygame.K_a and not going_right:  # Left
                        x1_change = -SNAKE_BLOCK
                        y1_change = 0
                        going_left = True
                        going_right = going_up = going_down = False
                        last_direction_change = current_time
                        
                    elif event.key == pygame.K_d and not going_left:  # Right
                        x1_change = SNAKE_BLOCK
                        y1_change = 0
                        going_right = True
                        going_left = going_up = going_down = False
                        last_direction_change = current_time
                        
                    elif event.key == pygame.K_w and not going_down:  # Up
                        y1_change = -SNAKE_BLOCK
                        x1_change = 0
                        going_up = True
                        going_left = going_right = going_down = False
                        last_direction_change = current_time
                        
                    elif event.key == pygame.K_s and not going_up:  # Down
                        y1_change = SNAKE_BLOCK
                        x1_change = 0
                        going_down = True
                        going_left = going_right = going_up = False
                        last_direction_change = current_time
        
        # Handle different game states
        if game_state == PAUSED:
            display.fill(BLACK)
            draw_text("Game Paused", title_font, BLUE, DISPLAY_WIDTH // 2, 200, True)
            draw_text("Press P to Resume", message_font, WHITE, DISPLAY_WIDTH // 2, 250, True)
            draw_controls_info()
            pygame.display.update()
            continue
            
        elif game_state == GAME_OVER:
            high_scores = load_high_scores()
            play_again, main_menu, is_high_score = show_game_over_screen(snake_length - 1, current_speed, high_scores)
            
            # Save score if it's a high score
            if is_high_score and not any(hs.get("saved") for hs in high_scores):
                save_high_score(snake_length - 1, current_speed)
                
                # Mark as saved to prevent multiple saves
                for hs in high_scores:
                    hs["saved"] = True
            
            if play_again:
                return "RESTART", 0
                
            if main_menu:
                return "MENU", 0
                
            continue
            
        # Process game logic only if we're playing
        if game_state == PLAYING:
            # Check if snake hit the boundaries
            if x1 >= DISPLAY_WIDTH or x1 < 0 or y1 >= DISPLAY_HEIGHT or y1 < 0:
                game_state = GAME_OVER
                continue
            
            # Update snake position
            x1 += x1_change
            y1 += y1_change
            
            # Draw everything
            display.fill(BLACK)
            draw_food(foodx, foody, SNAKE_BLOCK)
            
            # Update snake list
            snake_head = []
            snake_head.append(x1)
            snake_head.append(y1)
            snake_list.append(snake_head)
            
            # Remove the oldest segment if snake hasn't grown
            if len(snake_list) > snake_length:
                del snake_list[0]
            
            # Check if snake collided with itself
            for segment in snake_list[:-1]:
                if segment == snake_head:
                    game_state = GAME_OVER
                    continue
            
            # Draw the snake, score, and speed
            draw_snake(SNAKE_BLOCK, snake_list)
            draw_score(snake_length - 1)
            draw_speed(current_speed)
            draw_controls_info()
            
            # Update display
            pygame.display.update()
            
            # Check if snake ate food
            if x1 == foodx and y1 == foody:
                # Generate new food position
                foodx = round(random.randrange(0, DISPLAY_WIDTH - SNAKE_BLOCK) / 10.0) * 10.0
                foody = round(random.randrange(0, DISPLAY_HEIGHT - SNAKE_BLOCK) / 10.0) * 10.0
                snake_length += 1
            
            # Control game speed
            clock.tick(current_speed)
    
    return "QUIT", 0

def main():
    """Main function to control game flow"""
    game_state = MAIN_MENU
    current_speed = DEFAULT_SPEED
    running = True
    
    while running:
        if game_state == MAIN_MENU:
            play, speed, instructions, high_scores = show_main_menu()
            
            if play:
                game_state = PLAYING
            elif speed:
                game_state = SPEED_SELECTION
            elif instructions:
                game_state = INSTRUCTIONS
            elif high_scores:
                game_state = GAME_OVER  # Reuse game over for high scores
                
        elif game_state == INSTRUCTIONS:
            back = show_instructions()
            
            if back:
                game_state = MAIN_MENU
                
        elif game_state == SPEED_SELECTION:
            new_speed, back = show_speed_selection(current_speed)
            current_speed = new_speed
            
            if back:
                game_state = MAIN_MENU
                
        elif game_state == GAME_OVER:
            back = show_high_scores()
            
            if back:
                game_state = MAIN_MENU
                
        elif game_state == PLAYING:
            result, _ = game_loop(current_speed)
            
            if result == "QUIT":
                running = False
            elif result == "MENU":
                game_state = MAIN_MENU
            elif result == "RESTART":
                game_state = PLAYING
        
        # Handle events for other screens
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
    
    pygame.quit()

if __name__ == "__main__":
    main()


# -----------------------------------------------
# Developed by Pavith Bambaravanage
# GitHub Repository: https://github.com/Pavith19/Python-Snake-Game.git
# -----------------------------------------------
