# player.py
from config import COLORS

class Player:
    def __init__(self, name, player_id):
        self.id = player_id
        self.name = name
        self.position = 0
        self.color = list(COLORS.values())[player_id + 3]  # Start from PLAYER1 color
        self.moves_history = []
        self.consecutive_sixes = 0
        self.has_won = False
        self.token_id = None  # Will be set by the GUI
        
    def move(self, steps):
        """Move player by given steps"""
        old_position = self.position
        new_position = self.position + steps
        
        if new_position <= 100:
            self.position = new_position
            
        self.moves_history.append({
            'from': old_position,
            'to': self.position,
            'steps': steps
        })
        
        return self.position
    
    def reset(self):
        """Reset player for new game"""
        self.position = 0
        self.moves_history = []
        self.consecutive_sixes = 0
        self.has_won = False
    
    def __str__(self):
        return f"{self.name} (Position: {self.position})"