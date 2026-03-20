# dice.py
import random
import tkinter as tk

class Dice:
    def __init__(self):
        self.value = 1
        
    def roll(self):
        """Roll the dice and return value"""
        self.value = random.randint(1, 6)
        return self.value
    
    def get_dice_faces(self):
        """Return dice face patterns"""
        return {
            1: [(2, 2)],
            2: [(1, 1), (3, 3)],
            3: [(1, 1), (2, 2), (3, 3)],
            4: [(1, 1), (1, 3), (3, 1), (3, 3)],
            5: [(1, 1), (1, 3), (2, 2), (3, 1), (3, 3)],
            6: [(1, 1), (1, 2), (1, 3), (3, 1), (3, 2), (3, 3)]
        }

class DiceAnimation:
    def __init__(self, canvas, x, y, size=100):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.size = size
        self.dice = Dice()
        self.dice_id = None
        self.animation_id = None
        self.is_rolling = False
        
    def draw_dice(self, value):
        """Draw dice with given value"""
        if self.dice_id:
            self.canvas.delete(self.dice_id)
            
        # Calculate dice dimensions
        dice_size = self.size
        dot_size = dice_size // 6
        margin = dice_size // 4
        
        # Draw dice background
        self.dice_id = self.canvas.create_rectangle(
            self.x, self.y, 
            self.x + dice_size, self.y + dice_size,
            fill='white', outline='black', width=2
        )
        
        # Get dot positions for the value
        dot_positions = self.dice.get_dice_faces()[value]
        
        # Draw dots
        for row, col in dot_positions:
            dot_x = self.x + margin + (col - 1) * (dice_size - 2 * margin) // 2
            dot_y = self.y + margin + (row - 1) * (dice_size - 2 * margin) // 2
            
            self.canvas.create_oval(
                dot_x - dot_size, dot_y - dot_size,
                dot_x + dot_size, dot_y + dot_size,
                fill='black'
            )
    
    def animate_roll(self, callback=None):
        """Animate dice rolling"""
        if self.is_rolling:
            return
            
        self.is_rolling = True
        self.roll_count = 0
        
        def update_animation():
            if self.roll_count < 10:  # Roll 10 times
                random_value = random.randint(1, 6)
                self.draw_dice(random_value)
                self.roll_count += 1
                self.animation_id = self.canvas.after(100, update_animation)
            else:
                self.is_rolling = False
                final_value = self.dice.roll()
                self.draw_dice(final_value)
                if callback:
                    callback(final_value)
        
        update_animation()
    
    def stop_animation(self):
        """Stop dice animation"""
        if self.animation_id:
            self.canvas.after_cancel(self.animation_id)
            self.is_rolling = False