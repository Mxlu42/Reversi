class Player(): # the class that will determine the player object
    def __init__(self, player, score):
        self.player = player
        self.score = score
    
    def get_player(self):
        print(self.player)
        return self.player

    def get_score(self):
        return self.score

if __name__ == '__main__':
    player_white = Player('White', 0)
    player_white.get_player()
    player_black = Player('Black', 0)

