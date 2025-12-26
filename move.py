
class Move(): #this class represents the moving algorithm
    def __init__(self):
        self.column = 0
        self.row = 0

    def move_input(self, input):
        if int(input) <= 10 or int(input) > 88:
            print('invalid input please tell us the exact coordinates')
        else:
            self.row = input[0]
            self.column = input[1]

    def get_column(self):
        return int(self.column)

    def get_row(self):
        return int(self.row)