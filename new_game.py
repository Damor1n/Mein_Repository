import os
import sys
import time
import random
import threading
from enum import Enum

class Direction(Enum):
    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)

class CLISnakeGame:
    def __init__(self):
        self.grid_size = 16
        self.snake = [(8, 8), (7, 8), (6, 8)]
        self.food = self.spawn_food()
        self.direction = Direction.RIGHT
        self.next_direction = Direction.RIGHT
        self.score = 0
        self.game_over = False
        self.speed = 0.15  # seconds between moves
        self.input_thread_active = True
        
        # Terminal settings
        self.hide_cursor()
    
    def hide_cursor(self):
        """Hide cursor in terminal"""
        if os.name == 'nt':  # Windows
            os.system('cls')
        else:  # Unix/Linux/Mac
            sys.stdout.write('\033[?25l')
            sys.stdout.flush()
    
    def show_cursor(self):
        """Show cursor in terminal"""
        if os.name != 'nt':
            sys.stdout.write('\033[?25h')
            sys.stdout.flush()
    
    def clear_screen(self):
        """Clear the terminal screen"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def spawn_food(self):
        """Generate random food position"""
        while True:
            x = random.randint(0, self.grid_size - 1)
            y = random.randint(0, self.grid_size - 1)
            if (x, y) not in self.snake:
                return (x, y)
    
    def draw_game(self):
        """Render the game board"""
        self.clear_screen()
        
        print("╔" + "═" * (self.grid_size * 2 + 1) + "╗")
        
        for y in range(self.grid_size):
            print("║", end="")
            for x in range(self.grid_size):
                if (x, y) == self.snake[0]:  # Head
                    print("◉ ", end="")
                elif (x, y) in self.snake:  # Body
                    print("● ", end="")
                elif (x, y) == self.food:  # Food
                    print("◎ ", end="")
                else:  # Empty
                    print("· ", end="")
            print("║")
        
        print("╚" + "═" * (self.grid_size * 2 + 1) + "╝")
        print(f"\nScore: {self.score} | Length: {len(self.snake)} | Speed: {1/self.speed:.1f} moves/sec")
        print("Controls: Arrow Keys or WASD | Q: Quit | E: Increase Speed | D: Decrease Speed")
        print()
    
    def handle_input(self):
        """Handle keyboard input in a separate thread"""
        if os.name == 'nt':  # Windows
            import msvcrt
            while self.input_thread_active:
                if msvcrt.kbhit():
                    key = msvcrt.getch().decode('utf-8', errors='ignore').upper()
                    self.process_key(key)
                time.sleep(0.05)
        else:  # Unix/Linux/Mac
            import tty
            import termios
            
            fd = sys.stdin.fileno()
            old_settings = termios.tcgetattr(fd)
            
            try:
                tty.setraw(fd)
                while self.input_thread_active:
                    if sys.stdin in select_wait([sys.stdin], [], [], 0.05)[0]:
                        key = sys.stdin.read(1).upper()
                        self.process_key(key)
            finally:
                termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    
    def process_key(self, key):
        """Process keyboard input"""
        if key == 'Q':
            self.game_over = True
        elif key in ['W', 'UP']:
            if self.direction != Direction.DOWN:
                self.next_direction = Direction.UP
        elif key in ['S', 'DOWN']:
            if self.direction != Direction.UP:
                self.next_direction = Direction.DOWN
        elif key in ['A', 'LEFT']:
            if self.direction != Direction.RIGHT:
                self.next_direction = Direction.LEFT
        elif key in ['D', 'RIGHT']:
            if self.direction != Direction.LEFT:
                self.next_direction = Direction.RIGHT
        elif key == 'E':
            if self.speed > 0.05:
                self.speed -= 0.05
        elif key == 'D':
            if self.speed < 0.5:
                self.speed += 0.05
    
    def update_game(self):
        """Update game state"""
        if self.game_over:
            return
        
        self.direction = self.next_direction
        
        # Calculate new head position
        head_x, head_y = self.snake[0]
        dx, dy = self.direction.value
        new_head = (head_x + dx, head_y + dy)
        
        # Check wall collision
        if new_head[0] < 0 or new_head[0] >= self.grid_size or \
           new_head[1] < 0 or new_head[1] >= self.grid_size:
            self.game_over = True
            return
        
        # Check self collision
        if new_head in self.snake:
            self.game_over = True
            return
        
        # Add new head
        self.snake.insert(0, new_head)
        
        # Check food collision
        if new_head == self.food:
            self.score += 10
            self.food = self.spawn_food()
        else:
            self.snake.pop()
    
    def run(self):
        """Main game loop"""
        # For Unix systems, import select
        if os.name != 'nt':
            import select
            global select_wait
            select_wait = select.select
        
        # Start input handler thread
        input_thread = threading.Thread(target=self.handle_input, daemon=True)
        input_thread.start()
        
        try:
            last_update = time.time()
            
            while not self.game_over:
                current_time = time.time()
                
                # Update game at specified speed
                if current_time - last_update >= self.speed:
                    self.update_game()
                    last_update = current_time
                
                self.draw_game()
                time.sleep(0.02)  # Small delay to prevent excessive CPU usage
            
            # Game over screen
            self.input_thread_active = False
            self.clear_screen()
            print("╔════════════════════════════════════════╗")
            print("║           GAME OVER!                   ║")
            print("║════════════════════════════════════════║")
            print(f"║  Final Score: {self.score:<27}║")
            print(f"║  Snake Length: {len(self.snake):<24}║")
            print("╚════════════════════════════════════════╝")
            print()
        
        finally:
            self.input_thread_active = False
            self.show_cursor()

if __name__ == "__main__":
    game = CLISnakeGame()
    game.run()
