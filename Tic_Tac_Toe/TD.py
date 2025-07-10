from test import Player, Game
import numpy as np

player1 = Player('player1')
player2 = Player('player2')

class TD(Game):
  def __init__(self, Q = {}):
    super.__init__(player1, player2)
  def sample_epsilon_greedy_action(self, player, state, epsilon = 0.1):
    if not player.Q[state]:
      num_actions = len(self.blank_places)
      prob = 1/num_actions if num_actions != 0 else 0
      player.Q[state] = {act: prob for act in self.blank_places}
    else:
      if np.random.rand() < epsilon:
        return player.move(self.blank_places)
      else:
        q_values = self.Q[state]
        return max(q_values, key = q_values.get)
  
  