import grid_game as game
import numpy as np

discount_factor = 1
step_size = 0.01
num_episodes = 100000
num_states = game.total_states

state_value = np.zeros(num_states)
state_reward = -np.ones(num_states)
state_reward[num_states-1] = 2
print(f'number of states {num_states}')
for i in range(num_episodes):
  initial_state = np.random.choice(game.states)
  episode = game.play_game(initial_state)

  G = 0
  visited_states = set()
  state = None
  for s in reversed(range(len(episode))):
    state = episode[s][0]
    reward = state_reward[state]

    G = discount_factor*G + reward

    state_value[state]+= step_size*(G - state_value[state])
  #print(state)
print('Multi Visit Monte carlo:' ,'\n', state_value.reshape((4,4)))

def first_visit_mc(num_episodes):
  for episodes_num in range(num_episodes):
    initial_state = np.random.choice(game.states)
    episodes = game.play_game(initial_state) # returns [[state, action], ...]

    G = 0
    visited = set()
    state_indices = {}

    for idx,(state,action) in enumerate(episodes):
      if state not in state_indices:
        state_indices[state] = idx

    for state, first_idx in state_indices.items():
      G = 0
      for t in reversed(range(first_idx, len(episode))):
        s = episode[t][0]
        G = discount_factor*G + state_reward[s]
      state_value[state] += step_size*(G - state_value[state])

first_visit_mc(num_episodes)

print('First Visit Monte carlo:' ,'\n', state_value.reshape((4,4)))