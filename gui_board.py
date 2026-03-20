# gui_board.py
import tkinter as tk
from config import COLORS, CELL_SIZE, BOARD_DIMENSION

class VisualBoard:
    def __init__(self, canvas, start_x, start_y):
        self.canvas = canvas
        self.start_x = start_x
        self.start_y = start_y
        self.cells = {}
        self.snake_lines = []
        self.ladder_lines = []
        
    def draw_board(self, board_numbers):
        """Draw the game board"""
        # Draw board background
        self.canvas.create_rectangle(
            self.start_x, self.start_y,
            self.start_x + CELL_SIZE * BOARD_DIMENSION,
            self.start_y + CELL_SIZE * BOARD_DIMENSION,
            fill=COLORS['BOARD_BG'], outline='black', width=3
        )
        
        # Draw cells and numbers
        for row in range(BOARD_DIMENSION):
            for col in range(BOARD_DIMENSION):
                x1 = self.start_x + col * CELL_SIZE
                y1 = self.start_y + row * CELL_SIZE
                x2 = x1 + CELL_SIZE
                y2 = y1 + CELL_SIZE
                
                # Alternate cell colors
                color = COLORS['CELL_LIGHT'] if (row + col) % 2 == 0 else COLORS['CELL_DARK']
                
                # Draw cell
                cell_id = self.canvas.create_rectangle(
                    x1, y1, x2, y2,
                    fill=color, outline='gray', width=1
                )
                
                # Add number
                number = board_numbers[row][col]
                text_id = self.canvas.create_text(
                    x1 + CELL_SIZE//2, y1 + CELL_SIZE//2,
                    text=str(number), font=('Arial', 10, 'bold'),
                    fill=COLORS['TEXT']
                )
                
                self.cells[number] = {
                    'rect': cell_id,
                    'text': text_id,
                    'x': x1 + CELL_SIZE//2,
                    'y': y1 + CELL_SIZE//2,
                    'bbox': (x1, y1, x2, y2)
                }
    
    def draw_snakes_and_ladders(self, snakes, ladders):
        """Draw snakes and ladders on the board"""
        # Draw ladders first (so snakes appear on top)
        for bottom, top in ladders.items():
            if bottom in self.cells and top in self.cells:
                bottom_pos = self.cells[bottom]
                top_pos = self.cells[top]
                
                # Draw ladder (green lines)
                line_id = self.canvas.create_line(
                    bottom_pos['x'] - 10, bottom_pos['y'],
                    top_pos['x'] - 10, top_pos['y'],
                    fill=COLORS['LADDER'], width=4, dash=(4, 2)
                )
                line_id2 = self.canvas.create_line(
                    bottom_pos['x'] + 10, bottom_pos['y'],
                    top_pos['x'] + 10, top_pos['y'],
                    fill=COLORS['LADDER'], width=4, dash=(4, 2)
                )
                self.ladder_lines.extend([line_id, line_id2])
        
        # Draw snakes
        for head, tail in snakes.items():
            if head in self.cells and tail in self.cells:
                head_pos = self.cells[head]
                tail_pos = self.cells[tail]
                
                # Draw snake (red squiggly line)
                points = self._create_squiggly_line(
                    head_pos['x'], head_pos['y'],
                    tail_pos['x'], tail_pos['y']
                )
                line_id = self.canvas.create_line(
                    points, fill=COLORS['SNAKE'], 
                    width=3, smooth=True
                )
                self.snake_lines.append(line_id)
    
    def _create_squiggly_line(self, x1, y1, x2, y2, segments=10):
        """Create squiggly line for snake representation"""
        points = []
        for i in range(segments + 1):
            t = i / segments
            x = x1 + (x2 - x1) * t
            y = y1 + (y2 - y1) * t
            
            # Add wiggle
            if 0 < t < 1:
                wiggle = 10 * (t * (1 - t)) * 4
                if i % 2 == 0:
                    x += wiggle
                else:
                    x -= wiggle
            
            points.extend([x, y])
        return points
    
    def get_cell_coordinates(self, position):
        """Get coordinates for a cell"""
        if position in self.cells:
            return self.cells[position]['x'], self.cells[position]['y']
        return None, None