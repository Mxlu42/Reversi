from move import Move
from player import Player

class Playboard():              # class that will manage the playboard and everything related to it
    def __init__(self):
        self.playboard = []
        self.row = 0
        self.col = 0

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
                