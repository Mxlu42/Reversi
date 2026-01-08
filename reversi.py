from playboard import Playboard
from move import Move
from player import Player
import tkinter as tk

class Reversi:
    
    def __init__(self):
        self.board = Playboard()
        self.current_player = 'B'
        self.player_black = Player('B', 2)
        self.player_white = Player('W', 2)
        self.game_over = False
        
    def get_current_player(self):
        return self.current_player
    
    def get_opposing_player(self):
        return 'W' if self.current_player == 'B' else 'B'
    
    def switch_player(self):
        self.current_player = self.get_opposing_player()
    
    def is_valid_move(self, row, col):
        if not (1 <= row <= 8 and 1 <= col <= 8):
            return False
        
        if self.board.playboard[row - 1][col - 1] is not None:
            return False
        
        mov = Move()
        mov.row = row
        mov.column = col
        self.board.set_move(mov)
        
        current = self.current_player
        opposing = self.get_opposing_player()
        result = self.board.check_move(current, opposing)
        
        if isinstance(result, tuple) and len(result) == 2:
            i, j = result
            if -1 <= i <= 1 and -1 <= j <= 1 and (i != 0 or j != 0):
                return True
        
        return False
    
    def get_valid_moves(self):
        valid_moves = []
        for row in range(1, 9):
            for col in range(1, 9):
                if self.is_valid_move(row, col):
                    valid_moves.append((row, col))
        return valid_moves
    
    def display_valid_moves(self):
        valid_moves = self.get_valid_moves()
        
        if len(valid_moves) == 0:
            print(f"No valid moves available for {self.current_player}.")
            return
        
        print(f"\nValid moves for {self.current_player}:")
        
        move_strings = [f"{row}{col}" for row, col in valid_moves]
        
        print("Move format: row+column ( '64' = row 6, column 4)")
        print("Available moves:", ", ".join(sorted(move_strings)))
        
        print(f"Total: {len(valid_moves)} valid move(s)\n")
    
    def make_move(self, row, col):
        if not self.is_valid_move(row, col):
            return False
        
        mov = Move()
        mov.row = row
        mov.column = col
        self.board.set_move(mov)
        
        directions = self._get_flip_directions(row, col)
        
        self.board.set_piece(self.current_player)
        
        for direction in directions:
            self._flip_pieces(row, col, direction)
        
        self._update_scores()
        
        return True
    
    def _get_flip_directions(self, row, col):
        directions = []
        
        for delta_row in range(-1, 2):
            for delta_col in range(-1, 2):
                if delta_row == 0 and delta_col == 0:
                    continue
                
                if self._check_direction(row, col, delta_row, delta_col):
                    directions.append((delta_row, delta_col))
        
        return directions
    
    def _check_direction(self, row, col, delta_row, delta_col):
        opposing = self.get_opposing_player()
        current = self.current_player
        
        adj_row = row - 1 + delta_row
        adj_col = col - 1 + delta_col
        
        if not (0 <= adj_row < 8 and 0 <= adj_col < 8):
            return False
        
        if self.board.playboard[adj_row][adj_col] != opposing:
            return False
        
        step = 2
        while True:
            check_row = row - 1 + delta_row * step
            check_col = col - 1 + delta_col * step
            
            if not (0 <= check_row < 8 and 0 <= check_col < 8):
                return False
            
            cell = self.board.playboard[check_row][check_col]
            
            if cell is None:
                return False
            
            if cell == current:
                return True
            
            step += 1
    
    def _flip_pieces(self, row, col, direction):
        delta_row, delta_col = direction
        opposing = self.get_opposing_player()
        current = self.current_player
        
        step = 1
        while True:
            flip_row = row - 1 + delta_row * step
            flip_col = col - 1 + delta_col * step
            
            if not (0 <= flip_row < 8 and 0 <= flip_col < 8):
                break
            
            cell = self.board.playboard[flip_row][flip_col]
            
            if cell == current:
                break
            
            if cell == opposing:
                self.board.playboard[flip_row][flip_col] = current
            
            step += 1
    
    def _update_scores(self):
        black_count = 0
        white_count = 0
        
        for row in self.board.playboard:
            for cell in row:
                if cell == 'B':
                    black_count += 1
                elif cell == 'W':
                    white_count += 1
        
        self.player_black.score = black_count
        self.player_white.score = white_count
    
    def check_game_over(self):
        current_moves = self.get_valid_moves()
        
        if len(current_moves) > 0:
            return False
        
        self.switch_player()
        other_moves = self.get_valid_moves()
        self.switch_player()
        
        if len(other_moves) > 0:
            return False
        
        return True
    
    def get_winner(self):
        self._update_scores()
        black_score = self.player_black.get_score()
        white_score = self.player_white.get_score()
        
        if black_score > white_score:
            return 'B'
        elif white_score > black_score:
            return 'W'
        else:
            return None
    
    def _show_results_window(self, winner):
        """Display a Tkinter window with game results."""
        results_window = tk.Tk()
        results_window.title("Reversi - Game Over")
        results_window.geometry("400x250")
        
        # Game Over title
        title_label = tk.Label(
            results_window,
            text="GAME OVER",
            font=("Arial", 20, "bold"),
            pady=10
        )
        title_label.pack()
        
        # Final scores
        black_score = self.player_black.get_score()
        white_score = self.player_white.get_score()
        
        scores_text = f"Black: {black_score}  |  White: {white_score}"
        scores_label = tk.Label(
            results_window,
            text=scores_text,
            font=("Arial", 14),
            pady=10
        )
        scores_label.pack()
        
        # Winner announcement
        if winner:
            winner_text = f"Winner: {'Black' if winner == 'B' else 'White'}!"
            winner_color = "black" if winner == 'B' else "gray"
        else:
            winner_text = "It's a tie!"
            winner_color = "blue"
        
        winner_label = tk.Label(
            results_window,
            text=winner_text,
            font=("Arial", 16, "bold"),
            fg=winner_color,
            pady=10
        )
        winner_label.pack()
        
        # Close button
        close_button = tk.Button(
            results_window,
            text="Close",
            command=results_window.destroy,
            font=("Arial", 12),
            padx=20,
            pady=5
        )
        close_button.pack(pady=10)
        
        results_window.mainloop()
    
    def play(self):
        print("Welcome to Reversi!")
        print("Black (B) goes first. Enter moves as row+column ('64' for row 6, column 4)")
        print("Type 'quit' to exit the game.")
        print("Type 'moves' to see all valid moves for the current player.\n")

        # Open the Tkinter window and keep it updated alongside the terminal game
        self.board.init_ui()
        
        while not self.game_over:
            # Update scores before displaying
            self._update_scores()
            
            # Get valid moves for current player
            valid_moves = self.get_valid_moves()
            
            # Update the GUI board view with current game state
            self.board.update_ui(
                current_player=self.current_player,
                black_score=self.player_black.get_score(),
                white_score=self.player_white.get_score(),
                valid_moves=valid_moves
            )

            self.board.display()
            print(f"\nCurrent player: {self.current_player}")
            print(f"Black: {self.player_black.get_score()} | White: {self.player_white.get_score()}")
            
            if len(valid_moves) == 0:
                print(f"No valid moves for {self.current_player}. Switching players...")
                self.switch_player()
                
                # Update UI after switching players
                self._update_scores()
                new_valid_moves = self.get_valid_moves()
                self.board.update_ui(
                    current_player=self.current_player,
                    black_score=self.player_black.get_score(),
                    white_score=self.player_white.get_score(),
                    valid_moves=new_valid_moves
                )
                
                if self.check_game_over():
                    self.game_over = True
                    break
                continue
            
            self.display_valid_moves()
            
            move_input = input(f"Enter your move (row+column) for {self.current_player}: ").strip()
            
            if move_input.lower() == 'quit':
                print("Game ended by player.")
                break
            
            if move_input.lower() == 'moves':
                self.display_valid_moves()
                continue
            
            if len(move_input) != 2 or not move_input.isdigit():
                print("Invalid input. Please enter two digits ( '64' for row 6, column 4)")
                continue
            
            mov = Move()
            mov.move_input(move_input)
            row = mov.get_row()
            col = mov.get_column()
            
            if self.make_move(row, col):
                print(f"Move placed at row {row}, column {col}")
                self.switch_player()
                
                # Update UI after move
                self._update_scores()
                valid_moves = self.get_valid_moves()
                self.board.update_ui(
                    current_player=self.current_player,
                    black_score=self.player_black.get_score(),
                    white_score=self.player_white.get_score(),
                    valid_moves=valid_moves
                )
                
                if self.check_game_over():
                    self.game_over = True
            else:
                print("Invalid move! Please try again.")
        
        print("\n" + "="*50)
        print("GAME OVER")
        print("="*50)
        self.board.display()
        # Final GUI refresh before exiting
        self._update_scores()
        final_valid_moves = self.get_valid_moves()
        self.board.update_ui(
            current_player=self.current_player,
            black_score=self.player_black.get_score(),
            white_score=self.player_white.get_score(),
            valid_moves=final_valid_moves
        )
        print(f"\nFinal Scores:")
        print(f"Black: {self.player_black.get_score()}")
        print(f"White: {self.player_white.get_score()}")
        
        winner = self.get_winner()
        if winner:
            print(f"\nWinner: {'Black' if winner == 'B' else 'White'}!")
        else:
            print("\nIt's a tie!")
        
        # Create a results window showing the winner and final scores
        self._show_results_window(winner)


if __name__ == '__main__':
    game = Reversi()
    game.play()
