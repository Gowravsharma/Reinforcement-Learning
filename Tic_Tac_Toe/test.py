import numpy as np

class Player:
  def __init__(self, name='player'):
    self.name = name
    self.filled_place = []
    self.trajectory = []
    self.win = False
    self.Q = {}

  def move(self, blank_places):
    if not blank_places:
      return None
    next_move = np.random.choice(blank_places)
    self.filled_place.append(next_move)
    self.trajectory.append(next_move)
    return next_move

class Game:
  def __init__(self, player1, player2):
    self.start_player = None
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
  
  def sample_epsilon_greedy_action(self, player, state, epsilon = 0.1):
    if not player.Q[state]:
      num_actions = len(self.blank_places)
      prob = 1/num_actions if num_actions != 0 else 0
      player.Q[state] = {act: prob for act in self.blank_places}
      return player.move(self.blank_places)
    else:
      if np.random.rand() < epsilon:
        return player.move(self.blank_places)
      else:
        q_values = player.Q[state]
        return max(q_values, key = q_values.get)
      
  def play(self):
    sampled_states = [[],[]]
    self.turn = np.random.choice([0,1])
    self.start_player = self.turn
    while self.blank_places:
      s = []
      current_player = self.players[self.turn]
      state = self.filled_places_players
      s.append(state) # s = [state]
      #sampled_states[self.turn].append[state] # inserting state in trajectory i.e., sampled_states[turn][0]
      move = self.sample_epsilon_greedy_action(current_player, state)
      s.append(move) # s = [state, move]
      #sampled_states[self.turn].append[move] # inserting action after the state i.e., sampled_states[turn][1]
      self.filled_places_players[self.turn].append(move)
      
      if move is None:
        #print("No moves left!")
        break
      self.blank_places.remove(move)

      #print(f"{current_player.name} move {move}")

      if self.is_terminal_state(current_player.filled_place):
        current_player.win = True
        s.append(10) # s = [state, move, reward(10)]
        #print(f"{current_player.name} wins")
        return
      
      s.append(-1) # s = [state, move, reward(-1)]
      sampled_states[self.turn].append(s) 
      self.turn = 1 - self.turn  # switch turn
      return sampled_states

    print("Tie")

if __name__ == '__main__':
  player1 = Player(name = 'player1')
  player2 = Player(name = 'player2')

  game = Game(player1, player2)
  game.play()
  print(game.filled_places_players)
