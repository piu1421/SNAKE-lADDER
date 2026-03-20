# main.py
import tkinter as tk
from tkinter import messagebox
from game_gui import SnakeLadderGUI

def main():
    """Main entry point for the Snake and Ladder game"""
    try:
        # Create and run the game
        game = SnakeLadderGUI()
        game.run()
    except Exception as e:
        # Show error message if something goes wrong
        root = tk.Tk()
        root.withdraw()  # Hide the main window
        messagebox.showerror(
            "Error",
            f"An error occurred while starting the game:\n{str(e)}\n\nPlease make sure all files are in the correct location."
        )
        root.destroy()

if __name__ == "__main__":
    main()
