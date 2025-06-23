import Grid_world.grid_game as game
import numpy as np

discount_factor = 1
step_size = 0.1
num_episodes = 1000
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
print(state_value.reshape((4,4)))
