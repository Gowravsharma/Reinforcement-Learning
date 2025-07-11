from test import Player, Game
import numpy as np

class TD(Game):
  def __init__(self, player1, player2,step_size, discount_factor, epsilon = None):
    super().__init__(player1, player2)
    self.player1 = player1
    self.player2 = player2
    self.step_size = step_size
    self.discount_factor = discount_factor
    self.epsilon = epsilon if epsilon is not None else 0.1
  
  def TD_control(self, num_episodes):
    for episode in range(num_episodes):
      episode_trace = []
      
      print(f'self.play is being called in ep: {episode}')
      episodes = self.play()
      player_idx = self.start_player
      print('self.play called & initializing players')
      player1 = self.players[player_idx]
      player2 = self.players[1-player_idx]
      print('Initialization done & accesing episodes')
      ep1 = episodes[player_idx]
      ep2 = episodes[1-player_idx]
      G = 0

      for s in range(len(ep1) - 1):
        state_t,action_t,reward_t = ep1[s]
        state_tp1 , action_tp1, reward_tp1 = ep1[s+1]

        if action_t == None or action_tp1 is None:
          continue
        
        q_predict = player1.Q[state_t][action_t]
        q_target = reward_tp1 + self.discount_factor * player1.Q[state_tp1][action_tp1]
        player1.Q[state_t][action_t] += self.step_size * (q_target - q_predict)
      print('Trained')

if __name__ == '__main__':
  player1 = Player(name = 'player1')
  player2 = Player(name = 'player2')

  td1 = TD(player1, player2,step_size = 0.01, discount_factor = 0.1, epsilon = 0.1)
  td1.TD_control(1000)
  td1.play()
  print(td1.filled_places_players)