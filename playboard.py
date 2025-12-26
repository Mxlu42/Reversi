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
                if self.playboard[self.row+i][self.col+j] == opposing_player:
                    case = i, j
                    if case[0] == 0:
                        b = 1
                    if case[1] == 0:
                        a = 1
                    else:
                        b = i
                        a = j
                    if self.playboard[self.row +i+b][self.col + j+a] == player:
                        print('Move is valid')
                    elif self.playboard[self.row+i+b][self.col+j+a] == None:
                        print('Move is invalid')
                    elif self.playboard[self.row+i+b][self.col+j+a] == opposing_player:
                        step = 2  # because step=1 is the neighbor we already checked
                        while True:
                            nr = self.col + i*step
                            nc = self.row + j*step

                            if not (0 <= nr < 8 and 0 <= nc < 8):
                                break

                            if self.playboard[nr][nc] is None:
                                print("Move is invalid")
                                break

                            if self.playboard[nr][nc] == player:
                                print("Move is valid")
                                return (i, j)  # direction that makes it valid
                            step += 1
        return case
                
if __name__ == '__main__':
    mov = Move()
    board = Playboard()
    pl = Player('W', 0)
    mov.move_input('64')
    board.set_move(mov)
    print(board.check_move('W','B'))
    board.set_piece(pl.get_player())
    board.display()