import SpaceGame as game
import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np
import pygame 
from torch.optim import Adam

LR = 0.1
GAMMA = 0.01
NUM_ACTIONS = 4
HIDDEN_NEURONS = 8
NUM_EPISODES = 100
INPUT_DIM = 17
EPSILON = 0.1
ACTIONS = [0,1,2,3] # 0 -> stay, 1 -> left, 2 -> right, 3 -> shoot
GAME = game.SpaceInvaderGame()

# defining a approximator i.e a neural net
class qnn(nn.Module):
  def __init__(self, input_dim = INPUT_DIM, hidden_neurons = HIDDEN_NEURONS, num_actions = NUM_ACTIONS):
    super(qnn, self).__init__()

    self.input_layer = nn.Linear(input_dim, hidden_neurons)
    self.linear1 = nn.Linear(hidden_neurons, 8)
    self.linear2 = nn.Linear(8, num_actions)
    self.ReLU = nn.ReLU()
    self.sigmoid = nn.Sigmoid()

  def forward(self, x):
    x = self.ReLU(self.input_layer(x))
    x = self.ReLU(self.linear1(x))
    x = self.linear2(x)
    return x

q_fn = qnn() #------- Q value function approximator object

class DQN:
  def __init__(self, Q = q_fn, gamma = GAMMA, epsilon = EPSILON, actions = ACTIONS):
    self.Q = Q
    self.epsilon = epsilon
    self.gamma = gamma
  
  def epsilon_greedy_action(self, state ,epsilon = EPSILON):
    if np.random.rand() < epsilon: # Go for Exploration
      return np.random.choice(ACTIONS)
    else: # go for exploitation
      state = torch.tensor(state)
      #print('tensor shape: ', state.shape)
      return torch.argmax(self.Q(state)).item()
  
#  def get_episodes(self):
#    sarsa_list = []
#   initial_state = GAME.reset()
#    is_game_over = False
#    while not is_game_over:
#      in_state = GAME.get_state()
#      initial_action = self.epsilon_greedy_action(state = in_state)
#      nxt_state , reward, is_game_over = GAME.step(initial_action)
#      sarsa_tuple = (initial_state, initial_action, reward, nxt_state)
#      sarsa_list.append(sarsa_tuple)
    
#    return sarsa_list

  def get_episodes(self):
    sarsa_list = []
    initial_state = GAME.reset()
    is_game_over = False
    while not is_game_over:
      for event in pygame.event.get():  # <-- this line prevents freezing
        if event.type == pygame.QUIT:
          pygame.quit()
          exit()

      in_state = GAME.get_state()
      initial_action = self.epsilon_greedy_action(state=in_state)
      nxt_state, reward, is_game_over = GAME.step(initial_action)
      sarsa_tuple = (in_state, initial_action, reward, nxt_state)
      sarsa_list.append(sarsa_tuple)
    return sarsa_list
  
  def train(self, num_episodes=NUM_EPISODES):
    optimizer = Adam(self.Q.parameters(), lr=0.1)
    loss_fn = nn.MSELoss()

    for episode in range(num_episodes):
      sarsa_list = self.get_episodes()
      train_loss = 0
      for sarsa_tuple in sarsa_list:
        in_state, in_action, reward, nxt_state = sarsa_tuple

        in_state_tensor = torch.tensor(in_state, dtype=torch.float32)
        nxt_state_tensor = torch.tensor(nxt_state, dtype=torch.float32)

        q_values = self.Q(in_state_tensor)
        q_pred = q_values[in_action]

        with torch.no_grad():
            q_next = self.Q(nxt_state_tensor)
            q_target = reward + self.gamma * torch.max(q_next)

        loss = loss_fn(q_pred, q_target)
        train_loss += loss.item()
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
      print(f'train_loss for episodes : {episode} is : ', train_loss)

    


if __name__ == '__main__':
  q_net = DQN()
  q_net.train()

