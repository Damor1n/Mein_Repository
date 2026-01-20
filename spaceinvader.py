import tkinter as tk
from tkinter import messagebox
import random
import math

class SpaceInvaders:
    def __init__(self, root):
        self.root = root
        self.root.title("Space Invaders")
        self.root.resizable(False, False)
        
        # Game variables
        self.width = 800
        self.height = 600
        self.score = 0
        self.game_over = False
        self.wave = 1
        
        # Canvas
        self.canvas = tk.Canvas(
            root,
            width=self.width,
            height=self.height,
            bg="black",
            highlightthickness=0
        )
        self.canvas.pack()
        
        # Info label
        self.info_label = tk.Label(
            root,
            text=f"Score: 0 | Wave: 1 | Lives: 3",
            font=("Arial", 14, "bold"),
            fg="lime",
            bg="black"
        )
        self.info_label.pack()
        
        # Player
        self.player_x = self.width // 2
        self.player_y = self.height - 50
        self.player_width = 40
        self.player_height = 40
        self.player_speed = 7
        self.keys_pressed = set()
        
        # Bullets
        self.bullets = []
        self.bullet_speed = 10
        
        # Enemies
        self.enemies = []
        self.enemy_bullets = []
        self.lives = 3
        self.create_enemies()
        
        # Bind keys
        self.root.bind("<KeyPress>", self.key_press)
        self.root.bind("<KeyRelease>", self.key_release)
        self.root.bind("<space>", self.shoot)
        
        self.game_loop()
    
    def create_enemies(self):
        """Create a wave of enemies"""
        self.enemies = []
        rows = 2 + (self.wave // 3)
        cols = 6
        
        for row in range(rows):
            for col in range(cols):
                x = col * 100 + 60
                y = row * 60 + 40
                speed = 2 + (self.wave // 5)
                self.enemies.append({
                    'x': x,
                    'y': y,
                    'width': 40,
                    'height': 30,
                    'speed': speed,
                    'direction': 1,
                    'shoot_timer': random.randint(30, 100)
                })
    
    def key_press(self, event):
        """Handle key press"""
        self.keys_pressed.add(event.keysym)
    
    def key_release(self, event):
        """Handle key release"""
        self.keys_pressed.discard(event.keysym)
    
    def shoot(self, event=None):
        """Player shoots a bullet"""
        if not self.game_over:
            bullet_x = self.player_x + self.player_width // 2
            self.bullets.append({
                'x': bullet_x,
                'y': self.player_y,
                'width': 5,
                'height': 15
            })
    
    def update_player(self):
        """Update player position"""
        if 'Left' in self.keys_pressed or 'a' in self.keys_pressed:
            self.player_x = max(0, self.player_x - self.player_speed)
        if 'Right' in self.keys_pressed or 'd' in self.keys_pressed:
            self.player_x = min(self.width - self.player_width, self.player_x + self.player_speed)
    
    def update_bullets(self):
        """Update bullet positions and check collisions"""
        # Move player bullets
        for bullet in self.bullets[:]:
            bullet['y'] -= self.bullet_speed
            
            # Remove bullets that are off screen
            if bullet['y'] < 0:
                self.bullets.remove(bullet)
                continue
            
            # Check collision with enemies
            for enemy in self.enemies[:]:
                if self.check_collision(bullet, enemy):
                    if bullet in self.bullets:
                        self.bullets.remove(bullet)
                    if enemy in self.enemies:
                        self.enemies.remove(enemy)
                        self.score += 10
                    break
        
        # Move enemy bullets
        for bullet in self.enemy_bullets[:]:
            bullet['y'] += 5
            
            # Remove bullets that are off screen
            if bullet['y'] > self.height:
                self.enemy_bullets.remove(bullet)
                continue
            
            # Check collision with player
            if self.check_collision(bullet, {
                'x': self.player_x,
                'y': self.player_y,
                'width': self.player_width,
                'height': self.player_height
            }):
                self.enemy_bullets.remove(bullet)
                self.lives -= 1
                if self.lives <= 0:
                    self.game_over = True
    
    def update_enemies(self):
        """Update enemy positions and actions"""
        if not self.enemies:
            # Next wave
            self.wave += 1
            self.create_enemies()
        
        # Move enemies
        move_down = False
        for enemy in self.enemies:
            enemy['x'] += enemy['speed'] * enemy['direction']
            
            # Check boundaries
            if enemy['x'] <= 0 or enemy['x'] + enemy['width'] >= self.width:
                move_down = True
        
        # Move down and reverse direction
        if move_down:
            for enemy in self.enemies:
                enemy['direction'] *= -1
                enemy['y'] += 30
                
                # Check if enemies reached bottom
                if enemy['y'] + enemy['height'] >= self.player_y:
                    self.game_over = True
        
        # Enemy shoots
        for enemy in self.enemies[:]:
            enemy['shoot_timer'] -= 1
            if enemy['shoot_timer'] <= 0:
                self.enemy_bullets.append({
                    'x': enemy['x'] + enemy['width'] // 2,
                    'y': enemy['y'] + enemy['height'],
                    'width': 5,
                    'height': 15
                })
                enemy['shoot_timer'] = random.randint(30, 100)
    
    def check_collision(self, obj1, obj2):
        """Check if two objects collide"""
        return (obj1['x'] < obj2['x'] + obj2['width'] and
                obj1['x'] + obj1['width'] > obj2['x'] and
                obj1['y'] < obj2['y'] + obj2['height'] and
                obj1['y'] + obj1['height'] > obj2['y'])
    
    def draw(self):
        """Draw all game objects"""
        self.canvas.delete("all")
        
        # Draw stars background
        self.canvas.create_rectangle(0, 0, self.width, self.height, fill="black")
        
        # Draw player
        self.canvas.create_rectangle(
            self.player_x,
            self.player_y,
            self.player_x + self.player_width,
            self.player_y + self.player_height,
            fill="lime",
            outline="white"
        )
        
        # Draw player bullets
        for bullet in self.bullets:
            self.canvas.create_rectangle(
                bullet['x'] - bullet['width'] // 2,
                bullet['y'],
                bullet['x'] + bullet['width'] // 2,
                bullet['y'] + bullet['height'],
                fill="yellow"
            )
        
        # Draw enemies
        for enemy in self.enemies:
            self.canvas.create_rectangle(
                enemy['x'],
                enemy['y'],
                enemy['x'] + enemy['width'],
                enemy['y'] + enemy['height'],
                fill="red",
                outline="darkred"
            )
            # Draw eyes
            self.canvas.create_oval(
                enemy['x'] + 8,
                enemy['y'] + 5,
                enemy['x'] + 12,
                enemy['y'] + 12,
                fill="yellow"
            )
            self.canvas.create_oval(
                enemy['x'] + 28,
                enemy['y'] + 5,
                enemy['x'] + 32,
                enemy['y'] + 12,
                fill="yellow"
            )
        
        # Draw enemy bullets
        for bullet in self.enemy_bullets:
            self.canvas.create_rectangle(
                bullet['x'] - bullet['width'] // 2,
                bullet['y'],
                bullet['x'] + bullet['width'] // 2,
                bullet['y'] + bullet['height'],
                fill="red"
            )
        
        # Update info label
        self.info_label.config(
            text=f"Score: {self.score} | Wave: {self.wave} | Lives: {self.lives}"
        )
    
    def game_loop(self):
        """Main game loop"""
        if self.game_over:
            if self.lives <= 0:
                messagebox.showinfo("Game Over", f"Game Over!\nFinal Score: {self.score}\nWave: {self.wave}")
            else:
                messagebox.showinfo("Game Over", f"Enemies reached you!\nFinal Score: {self.score}")
            self.root.destroy()
            return
        
        self.update_player()
        self.update_bullets()
        self.update_enemies()
        self.draw()
        
        self.root.after(30, self.game_loop)

if __name__ == "__main__":
    root = tk.Tk()
    game = SpaceInvaders(root)
    root.mainloop()
