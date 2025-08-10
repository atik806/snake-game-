import os
import time
import random
import keyboard
import threading
from collections import deque

class SnakeGame:
    def __init__(self, width=40, height=20):
        self.width = width
        self.height = height
        self.snake = deque([(width // 2, height // 2)])  # Start in center
        self.direction = (1, 0)  # Start moving right
        self.food = self.generate_food()
        self.score = 0
        self.game_over = False
        self.paused = False
        
    def generate_food(self):
        """Generate food at a random position not occupied by snake"""
        while True:
            food = (random.randint(1, self.width - 2), random.randint(1, self.height - 2))
            if food not in self.snake:
                return food
    
    def move_snake(self):
        """Move the snake in the current direction"""
        if self.game_over or self.paused:
            return
            
        head_x, head_y = self.snake[0]
        new_head = (head_x + self.direction[0], head_y + self.direction[1])
        
        # Check wall collision
        if (new_head[0] <= 0 or new_head[0] >= self.width - 1 or
            new_head[1] <= 0 or new_head[1] >= self.height - 1):
            self.game_over = True
            return
            
        # Check self collision
        if new_head in self.snake:
            self.game_over = True
            return
            
        self.snake.appendleft(new_head)
        
        # Check food collision
        if new_head == self.food:
            self.score += 10
            self.food = self.generate_food()
        else:
            self.snake.pop()  # Remove tail if no food eaten
    
    def change_direction(self, new_direction):
        """Change snake direction if not opposite to current direction"""
        if self.game_over:
            return
            
        # Prevent moving in opposite direction
        if (new_direction[0] * -1, new_direction[1] * -1) != self.direction:
            self.direction = new_direction
    
    def draw(self):
        """Draw the game board"""
        os.system('cls' if os.name == 'nt' else 'clear')
        
        board = [[' ' for _ in range(self.width)] for _ in range(self.height)]
        
        # Draw borders
        for i in range(self.width):
            board[0][i] = '─'
            board[self.height - 1][i] = '─'
        for i in range(self.height):
            board[i][0] = '│'
            board[i][self.width - 1] = '│'
        
        # Draw corners
        board[0][0] = '┌'
        board[0][self.width - 1] = '┐'
        board[self.height - 1][0] = '└'
        board[self.height - 1][self.width - 1] = '┘'
        
        # Draw snake
        for i, (x, y) in enumerate(self.snake):
            if i == 0:
                board[y][x] = '●'  # Head
            else:
                board[y][x] = '○'  # Body
        
        # Draw food
        food_x, food_y = self.food
        board[food_y][food_x] = '★'
        
        # Print board
        for row in board:
            print(''.join(row))
        
        # Print game info
        print(f"\nScore: {self.score}")
        print("Controls: Arrow keys to move, P to pause, Q to quit")
        
        if self.paused:
            print("PAUSED - Press P to resume")
        elif self.game_over:
            print("GAME OVER! Press R to restart or Q to quit")
    
    def reset_game(self):
        """Reset the game to initial state"""
        self.snake = deque([(self.width // 2, self.height // 2)])
        self.direction = (1, 0)
        self.food = self.generate_food()
        self.score = 0
        self.game_over = False
        self.paused = False

def handle_input(game):
    """Handle keyboard input in a separate thread"""
    while True:
        try:
            if keyboard.is_pressed('up') or keyboard.is_pressed('w'):
                game.change_direction((0, -1))
                time.sleep(0.1)  # Prevent multiple inputs
            elif keyboard.is_pressed('down') or keyboard.is_pressed('s'):
                game.change_direction((0, 1))
                time.sleep(0.1)
            elif keyboard.is_pressed('left') or keyboard.is_pressed('a'):
                game.change_direction((-1, 0))
                time.sleep(0.1)
            elif keyboard.is_pressed('right') or keyboard.is_pressed('d'):
                game.change_direction((1, 0))
                time.sleep(0.1)
            elif keyboard.is_pressed('p'):
                game.paused = not game.paused
                time.sleep(0.3)  # Prevent rapid toggling
            elif keyboard.is_pressed('q'):
                os._exit(0)  # Force exit
            elif keyboard.is_pressed('r') and game.game_over:
                game.reset_game()
                time.sleep(0.3)
        except:
            # Handle any keyboard errors gracefully
            pass
        
        time.sleep(0.05)  # Small delay to prevent excessive CPU usage

def main():
    """Main game loop"""
    print("Terminal Snake Game")
    print("==================")
    print("Controls:")
    print("- Arrow keys or WASD to move")
    print("- P to pause/unpause")
    print("- Q to quit")
    print("- R to restart (when game over)")
    print("\nPress any key to start...")
    
    # Wait for any key to start
    keyboard.read_event()
    
    game = SnakeGame()
    
    # Start input handler in separate thread
    input_thread = threading.Thread(target=handle_input, args=(game,), daemon=True)
    input_thread.start()
    
    # Main game loop
    while True:
        game.draw()
        
        if not game.game_over and not game.paused:
            game.move_snake()
        
        # Adjust game speed (lower value = faster game)
        time.sleep(0.15)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nGame interrupted. Thanks for playing!")
    except Exception as e:
        print(f"\nAn error occurred: {e}")
        print("Please make sure you have the 'keyboard' library installed.")
        print("Install it with: pip install keyboard")
