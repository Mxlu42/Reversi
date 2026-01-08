
from move import Move
from player import Player
import tkinter as tk

class Playboard():              # class that will manage the playboard and everything related to it
    def __init__(self):
        self.playboard = []
        self.row = 0
        self.col = 0
        self.root = None
        self.labels = []

        for i in range(1,9):
            row = []
            for j in range(1,9):
                row.append(None)
            self.playboard.append(row)

        self.playboard[3][3] = 'W'
        self.playboard[3][4] = 'B'
        self.playboard[4][3] = 'B'
        self.playboard[4][4] = 'W'

    def display(self):
        print(' '+ ''.join(str(i) for i in range(1,9))) # creates the columns

        for r, row in enumerate(self.playboard):
            line = ''.join(cell if cell else '.' for cell in row) #needs some time to understand: if cell filled use cell,if not use '.' join is to glue it together
            print(r+1, line) # r is the index of the row and row is the for loop  
    
    def init_ui(self):
        if self.root is not None:
            return

        self.root = tk.Tk()
        self.root.title("Reversi - Board")

        board_frame = tk.Frame(self.root)
        board_frame.grid(row=0, column=0, padx=10, pady=10)

        # Create side panel frame for game info
        side_frame = tk.Frame(self.root, width=200, bg="lightgray")
        side_frame.grid(row=0, column=1, padx=10, pady=10, sticky="ns")
        side_frame.grid_propagate(False)

        self.labels = []
        for r in range(8):
            row_labels = []
            for c in range(8):
                lbl = tk.Label(
                    board_frame,
                    text='.',
                    width=3,
                    borderwidth=1,
                    relief="solid"
                )
                lbl.grid(row=r, column=c, sticky="nsew")
                row_labels.append(lbl)
            self.labels.append(row_labels)

        for i in range(8):
            board_frame.grid_columnconfigure(i, weight=1)
            board_frame.grid_rowconfigure(i, weight=1)

        title_label = tk.Label(
            side_frame,
            text="Game Info",
            font=("Arial", 16, "bold"),
            bg="lightgray",
            pady=10
        )
        title_label.pack()

        tk.Label(
            side_frame,
            text="Current Player:",
            font=("Arial", 10, "bold"),
            bg="lightgray"
        ).pack(anchor="w", padx=10)
        self.current_player_label = tk.Label(
            side_frame,
            text="Black (B)",
            font=("Arial", 12),
            bg="lightgray",
            fg="black"
        )
        self.current_player_label.pack(anchor="w", padx=20, pady=(0, 10))

        tk.Label(
            side_frame,
            text="Scores:",
            font=("Arial", 10, "bold"),
            bg="lightgray"
        ).pack(anchor="w", padx=10)
        
        self.black_score_label = tk.Label(
            side_frame,
            text="Black: 2",
            font=("Arial", 11),
            bg="lightgray"
        )
        self.black_score_label.pack(anchor="w", padx=20)
        
        self.white_score_label = tk.Label(
            side_frame,
            text="White: 2",
            font=("Arial", 11),
            bg="lightgray"
        )
        self.white_score_label.pack(anchor="w", padx=20, pady=(0, 10))

        tk.Label(
            side_frame,
            text="Valid Moves:",
            font=("Arial", 10, "bold"),
            bg="lightgray"
        ).pack(anchor="w", padx=10)
        
        self.valid_moves_count_label = tk.Label(
            side_frame,
            text="0 moves",
            font=("Arial", 11),
            bg="lightgray"
        )
        self.valid_moves_count_label.pack(anchor="w", padx=20, pady=(0, 5))
        
        moves_frame = tk.Frame(side_frame, bg="lightgray")
        moves_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        
        scrollbar = tk.Scrollbar(moves_frame)
        scrollbar.pack(side="right", fill="y")
        
        self.valid_moves_text = tk.Text(
            moves_frame,
            height=8,
            width=15,
            font=("Arial", 9),
            wrap="word",
            yscrollcommand=scrollbar.set,
            bg="black",
            relief="solid",
            borderwidth=1
        )
        self.valid_moves_text.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=self.valid_moves_text.yview)

        # Initial paint
        self.update_ui()

    def update_ui(self, current_player=None, black_score=None, white_score=None, valid_moves=None):
        if self.root is None:
            return

        for r in range(8):
            for c in range(8):
                value = self.playboard[r][c]
                self.labels[r][c]["text"] = value if value is not None else "."

        if current_player is not None:
            player_text = "Black (B)" if current_player == 'B' else "White (W)"
            player_color = "black" if current_player == 'B' else "gray"
            self.current_player_label.config(text=player_text, fg=player_color)
        
        if black_score is not None:
            self.black_score_label.config(text=f"Black: {black_score}")
        
        if white_score is not None:
            self.white_score_label.config(text=f"White: {white_score}")
        
        if valid_moves is not None:
            move_count = len(valid_moves)
            self.valid_moves_count_label.config(text=f"{move_count} move{'s' if move_count != 1 else ''}")
            
            self.valid_moves_text.delete("1.0", tk.END)
            if move_count > 0:
                move_strings = [f"{row}{col}" for row, col in sorted(valid_moves)]
                moves_display = ", ".join(move_strings)
                self.valid_moves_text.insert("1.0", moves_display)
            else:
                self.valid_moves_text.insert("1.0", "No valid moves")

        self.root.update_idletasks()
        self.root.update()

    def set_move(self, mov):
        self.row = mov.get_row() - 1
        self.col = mov.get_column() - 1   

    def set_piece(self, player):
        self.playboard[self.row][self.col] = player

    def check_move(self, player, opposing_player):

        self.playboard[self.row][self.col]
        case = 0
        b = 0
        a = 0
        for i in range(-1,2):
            for j in range(-1,2):
                adj_row = self.row + i
                adj_col = self.col + j
                if not (0 <= adj_row < 8 and 0 <= adj_col < 8):
                    continue
                    
                if self.playboard[adj_row][adj_col] == opposing_player:
                    case = i, j
                    if case[0] == 0: # turning 0 into 1 for the loops
                        b = 1
                    if case[1] == 0:
                        a = 1
                    else:
                        b = i
                        a = j
                    
                    next_row = self.row + i + b
                    next_col = self.col + j + a
                    if not (0 <= next_row < 8 and 0 <= next_col < 8):
                        continue
                        
                    if self.playboard[next_row][next_col] == player:
                        return (i, j)  # valid move
                    elif self.playboard[next_row][next_col] == None:
                        pass  # Move is invalid
                    elif self.playboard[next_row][next_col] == opposing_player:
                        step = 2 
                        while True:
                            check_row = self.row + i*step  
                            check_col = self.col + j*step  

                            if not (0 <= check_row < 8 and 0 <= check_col < 8):
                                break

                            if self.playboard[check_row][check_col] is None:
                                break  # Move is invalid

                            if self.playboard[check_row][check_col] == player:
                                return (i, j)  # direction that makes it valid
                            step += 1
        return case
                