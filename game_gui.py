# game_gui.py
import tkinter as tk
from tkinter import messagebox, simpledialog
import threading
import time
from config import *
from player import Player
from board import GameBoard
from dice import DiceAnimation
from gui_board import VisualBoard

class SnakeLadderGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Snake and Ladder Game")
        self.root.geometry("1200x800")
        self.root.resizable(False, False)
        
        # Game components
        self.board = GameBoard()
        self.players = []
        self.current_player_index = 0
        self.game_active = False
        
        # GUI Components
        self.setup_ui()
        
        # Bind events
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
    def setup_ui(self):
        """Setup the user interface"""
        # Create main frames
        self.left_frame = tk.Frame(self.root, bg='#2C3E50', width=800, height=800)
        self.left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.left_frame.pack_propagate(False)
        
        self.right_frame = tk.Frame(self.root, bg='#34495E', width=400, height=800)
        self.right_frame.pack(side=tk.RIGHT, fill=tk.BOTH)
        self.right_frame.pack_propagate(False)
        
        # Setup game board
        self.canvas = tk.Canvas(self.left_frame, bg='#2C3E50', width=800, height=800)
        self.canvas.pack()
        
        # Setup visual board
        self.visual_board = VisualBoard(self.canvas, 50, 50)
        
        # Setup control panel
        self.setup_control_panel()
        
        # Draw initial board
        self.draw_board()
        
    def setup_control_panel(self):
        """Setup the right panel controls"""
        # Title
        title = tk.Label(
            self.right_frame, text="SNAKE & LADDER",
            font=('Arial', 20, 'bold'), bg='#34495E',
            fg='#ECF0F1'
        )
        title.pack(pady=20)
        
        # Players frame
        players_frame = tk.LabelFrame(
            self.right_frame, text="Players",
            font=('Arial', 12, 'bold'), bg='#34495E',
            fg='#ECF0F1', padx=10, pady=10
        )
        players_frame.pack(fill=tk.X, padx=20, pady=10)
        
        self.players_listbox = tk.Listbox(
            players_frame, height=4,
            font=('Arial', 11), bg='#ECF0F1'
        )
        self.players_listbox.pack(fill=tk.X, pady=5)
        
        # Buttons
        btn_frame = tk.Frame(players_frame, bg='#34495E')
        btn_frame.pack(fill=tk.X)
        
        tk.Button(
            btn_frame, text="Add Player", command=self.add_player_dialog,
            bg=COLORS['BUTTON'], fg='white', font=('Arial', 10, 'bold'),
            padx=10
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            btn_frame, text="Remove Player", command=self.remove_player,
            bg='#E74C3C', fg='white', font=('Arial', 10, 'bold'),
            padx=10
        ).pack(side=tk.LEFT, padx=5)
        
        # Game controls frame
        game_frame = tk.LabelFrame(
            self.right_frame, text="Game Controls",
            font=('Arial', 12, 'bold'), bg='#34495E',
            fg='#ECF0F1', padx=10, pady=10
        )
        game_frame.pack(fill=tk.X, padx=20, pady=10)
        
        # Dice display
        self.dice_frame = tk.Frame(game_frame, bg='#34495E', height=120)
        self.dice_frame.pack(fill=tk.X, pady=10)
        
        self.dice_canvas = tk.Canvas(
            self.dice_frame, width=100, height=100,
            bg='white', highlightthickness=0
        )
        self.dice_canvas.pack()
        
        self.dice = DiceAnimation(self.dice_canvas, 0, 0, 100)
        self.dice.draw_dice(1)
        
        # Roll dice button
        self.roll_btn = tk.Button(
            game_frame, text="ROLL DICE", command=self.roll_dice,
            bg=COLORS['BUTTON'], fg='white', font=('Arial', 14, 'bold'),
            state=tk.DISABLED, height=2
        )
        self.roll_btn.pack(fill=tk.X, pady=10)
        
        # Start game button
        self.start_btn = tk.Button(
            game_frame, text="START GAME", command=self.start_game,
            bg='#27AE60', fg='white', font=('Arial', 14, 'bold'),
            height=2
        )
        self.start_btn.pack(fill=tk.X, pady=5)
        
        # Reset game button
        tk.Button(
            game_frame, text="RESET GAME", command=self.reset_game,
            bg='#E67E22', fg='white', font=('Arial', 12, 'bold'),
            height=1
        ).pack(fill=tk.X, pady=5)
        
        # Game status
        status_frame = tk.LabelFrame(
            self.right_frame, text="Game Status",
            font=('Arial', 12, 'bold'), bg='#34495E',
            fg='#ECF0F1', padx=10, pady=10
        )
        status_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        self.status_text = tk.Text(
            status_frame, height=10, width=35,
            font=('Arial', 10), bg='#ECF0F1',
            state=tk.DISABLED
        )
        self.status_text.pack(fill=tk.BOTH, expand=True)
        
        # Current player display
        self.current_player_label = tk.Label(
            self.right_frame, text="Current Player: None",
            font=('Arial', 12, 'bold'), bg='#34495E',
            fg='#F1C40F'
        )
        self.current_player_label.pack(pady=10)
        
    def draw_board(self):
        """Draw the game board"""
        board_numbers = self.board.get_board_numbers()
        self.visual_board.draw_board(board_numbers)
        self.visual_board.draw_snakes_and_ladders(
            self.board.snakes, self.board.ladders
        )
        
    def add_player_dialog(self):
        """Show dialog to add player"""
        if len(self.players) >= MAX_PLAYERS:
            messagebox.showwarning("Max Players", f"Maximum {MAX_PLAYERS} players allowed!")
            return
            
        name = simpledialog.askstring("Add Player", "Enter player name:", parent=self.root)
        if name and name.strip():
            player = Player(name.strip(), len(self.players))
            self.players.append(player)
            self.players_listbox.insert(tk.END, f"{player.name} (Pos: 0)")
            
            # Create player token on board
            self.create_player_token(player)
            
            self.update_status(f"Player {player.name} added!")
            
    def create_player_token(self, player):
        """Create visual token for player"""
        x, y = self.visual_board.get_cell_coordinates(1)
        if x and y:
            # Offset based on player ID to stack tokens
            offsets = [(0, 0), (15, -15), (-15, 15), (15, 15)]
            offset_x, offset_y = offsets[player.id % 4]
            
            token_id = self.canvas.create_oval(
                x - 15 + offset_x, y - 15 + offset_y,
                x + 15 + offset_x, y + 15 + offset_y,
                fill=player.color, outline='white', width=2
            )
            player.token_id = token_id
            
    def remove_player(self):
        """Remove selected player"""
        selection = self.players_listbox.curselection()
        if selection:
            index = selection[0]
            player = self.players[index]
            
            # Remove token from board
            if player.token_id:
                self.canvas.delete(player.token_id)
                
            self.players.pop(index)
            self.players_listbox.delete(index)
            self.update_status(f"Player {player.name} removed!")
            
    def move_player_token(self, player, new_position):
        """Move player token to new position"""
        x, y = self.visual_board.get_cell_coordinates(new_position)
        if x and y and player.token_id:
            # Get offset based on player ID
            offsets = [(0, 0), (15, -15), (-15, 15), (15, 15)]
            offset_x, offset_y = offsets[player.id % 4]
            
            self.canvas.coords(
                player.token_id,
                x - 15 + offset_x, y - 15 + offset_y,
                x + 15 + offset_x, y + 15 + offset_y
            )
            
    def start_game(self):
        """Start the game"""
        if len(self.players) < MIN_PLAYERS:
            messagebox.showwarning(
                "Cannot Start",
                f"Need at least {MIN_PLAYERS} players to start!"
            )
            return
            
        self.game_active = True
        self.start_btn.config(state=tk.DISABLED)
        self.roll_btn.config(state=tk.NORMAL)
        self.current_player_index = 0
        self.update_current_player_display()
        self.update_status("Game Started! Good luck!")
        
    def roll_dice(self):
        """Handle dice roll"""
        if not self.game_active:
            return
            
        current_player = self.players[self.current_player_index]
        
        # Disable roll button during animation
        self.roll_btn.config(state=tk.DISABLED)
        
        # Animate dice roll
        def after_roll(value):
            self.process_move(current_player, value)
            
        self.dice.animate_roll(after_roll)
        
    def process_move(self, player, dice_value):
        """Process player move"""
        # Check consecutive sixes
        if dice_value == 6:
            player.consecutive_sixes += 1
            if player.consecutive_sixes == CONSECUTIVE_SIX_LIMIT:
                self.update_status(f"{player.name} rolled three sixes! Turn skipped!")
                player.consecutive_sixes = 0
                self.next_turn()
                return
        else:
            player.consecutive_sixes = 0
            
        # Move player
        old_position = player.position
        new_position = player.move(dice_value)
        
        self.update_status(f"{player.name} rolled {dice_value} and moved to {new_position}")
        
        # Animate movement
        self.animate_movement(player, old_position, new_position, dice_value)
        
    def animate_movement(self, player, old_pos, new_pos, dice_value):
        """Animate player movement"""
        # Check for snake or ladder
        final_position, event = self.board.check_position(new_pos)
        
        if event == 'snake':
            self.update_status(f"🐍 Oh no! Snake! {player.name} slides down to {final_position}")
            player.position = final_position
        elif event == 'ladder':
            self.update_status(f"🪜 Great! Ladder! {player.name} climbs up to {final_position}")
            player.position = final_position
            
        # Move token
        self.move_player_token(player, player.position)
        
        # Check win condition
        if player.position == WIN_POSITION:
            player.has_won = True
            self.game_active = False
            self.roll_btn.config(state=tk.DISABLED)
            messagebox.showinfo("Winner!", f"🎉 {player.name} WINS! 🎉")
            self.update_status(f"🎉 {player.name} wins the game! 🎉")
            return
            
        # Extra turn for rolling 6
        if dice_value == 6 and player.position < WIN_POSITION:
            self.update_status(f"{player.name} gets another turn!")
            self.roll_btn.config(state=tk.NORMAL)
        else:
            self.next_turn()
            
    def next_turn(self):
        """Move to next player's turn"""
        if not self.game_active:
            return
            
        self.current_player_index = (self.current_player_index + 1) % len(self.players)
        
        # Skip players who have won
        while self.players[self.current_player_index].has_won:
            self.current_player_index = (self.current_player_index + 1) % len(self.players)
            
        self.update_current_player_display()
        self.roll_btn.config(state=tk.NORMAL)
        
    def update_current_player_display(self):
        """Update the current player display"""
        if self.players:
            player = self.players[self.current_player_index]
            self.current_player_label.config(
                text=f"Current Player: {player.name}",
                fg=player.color
            )
            
    def update_status(self, message):
        """Update status text"""
        self.status_text.config(state=tk.NORMAL)
        self.status_text.insert(tk.END, f"> {message}\n")
        self.status_text.see(tk.END)
        self.status_text.config(state=tk.DISABLED)
        
    def reset_game(self):
        """Reset the game"""
        self.game_active = False
        self.roll_btn.config(state=tk.DISABLED)
        self.start_btn.config(state=tk.NORMAL)
        
        # Reset all players
        for player in self.players:
            player.reset()
            self.move_player_token(player, 1)  # Move back to start
            
        self.current_player_index = 0
        self.update_current_player_display()
        self.update_status("Game reset!")
        
        # Clear status text
        self.status_text.config(state=tk.NORMAL)
        self.status_text.delete(1.0, tk.END)
        self.status_text.config(state=tk.DISABLED)
        
    def on_closing(self):
        """Handle window closing"""
        if messagebox.askokcancel("Quit", "Do you want to quit the game?"):
            self.root.destroy()
            
    def run(self):
        """Run the game"""
        self.root.mainloop()

if __name__ == "__main__":
    game = SnakeLadderGUI()
    game.run()
    