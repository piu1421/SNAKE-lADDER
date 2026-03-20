# board.py
from config import BOARD_SIZE, SNAKES, LADDERS, WIN_POSITION

class GameBoard:
    def __init__(self):
        self.size = BOARD_SIZE
        self.snakes = SNAKES
        self.ladders = LADDERS
        
    def check_position(self, position):
        """Check if position has snake or ladder and return new position and event type"""
        if position in self.snakes:
            return self.snakes[position], 'snake'
        elif position in self.ladders:
            return self.ladders[position], 'ladder'
        return position, None
    
    def is_valid_move(self, current_pos, steps):
        """Check if move is valid"""
        new_pos = current_pos + steps
        return new_pos <= WIN_POSITION
    
    def get_board_numbers(self):
        """Get board numbers in snake pattern"""
        numbers = []
        for row in range(10, 0, -1):
            start = (row - 1) * 10 + 1
            end = row * 10
            if row % 2 == 0:
                numbers.append(list(range(end, start - 1, -1)))
            else:
                numbers.append(list(range(start, end + 1)))
        return numbers