import numpy as np

class Player:
  def __init__(self, name='player'):
    self.name = name
    self.filled_place = []
    self.trajectory = []
    self.Q_values = {}

  def move(self, blank_places, state = None):
    if not blank_places:
      return None
    next_move = np.random.choice(blank_places)
    self.filled_place.append(next_move)
    self.trajectory.append(next_move)
    return next_move
  

class Game:
  def __init__(self, player1, player2):
    self.state = []
    self.players = [player1, player2]
    self.blank_places = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    self.filled_places_players = [[],[]]
    self.turn = 0  # 0 for player1, 1 for player2

  def is_terminal_state(self, filled_place):
    wins = [[1,2,3],[4,5,6],[7,8,9],
            [1,4,7],[2,5,8],[3,6,9],
            [1,5,9],[3,5,7]]
    for pattern in wins:
      if all(pos in filled_place for pos in pattern):
          return True
    return False
  
  def play(self):
    while self.blank_places:
      current_player = self.players[self.turn]
      move = current_player.move(self.blank_places)
      self.filled_places_players[self.turn].append(move)
      if move is None:
        print("No moves left!")
        break
      self.blank_places.remove(move)

      print(f"{current_player.name} move {move}")

      if self.is_terminal_state(current_player.filled_place):
        print(f"{current_player.name} wins")
        return

      self.turn = 1 - self.turn  # switch turn

    print("Tie")

if __name__ == '__main__':
  player1 = Player(name = 'player1')
  player2 = Player(name = 'player2')

  game = Game(player1, player2)
  game.play()
  print(game.filled_places_players)
