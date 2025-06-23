import grid_game as game
import numpy as np

discount_factor = 1
epsilon = 0.1
step_size = 0.01
num_episodes = 100
num_states = game.total_states

state_value = np.zeros(num_states)
state_reward = -np.ones(num_states)
state_reward[num_states-1] = 2

print(f'number of states {num_states}')

# Q_val Dictionary
Q = {
  s: {a: 0.0 for a in game.moves
      if not ((a == 'up' and s - game.rows < 0) or
              (a == 'down' and s + game.rows >= 16) or
              (a == 'right' and (s + 1) % game.rows == 0) or
              (a == 'left' and s % game.rows == 0))}
  for s in range(num_states)
}



def every_visit_mc(num_episodes):
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

every_visit_mc(num_episodes)
print('Every Visit Monte carlo:' ,'\n', state_value.reshape((4,4)))

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
      for t in reversed(range(first_idx, len(episodes))):
        s = episodes[t][0]
        G = discount_factor*G + state_reward[s]
      state_value[state] += step_size*(G - state_value[state])

first_visit_mc(num_episodes)
print('First Visit Monte carlo:' ,'\n', state_value.reshape((4,4)))

# Epsilon Greedy policy
def epsilon_greedy_action(Q,state):

  if np.random.rand() < epsilon:
    return game.sample_next_action
  else:
    q_values = Q[state]
    return max(q_values, key= q_values.get)
  
def every_visite_mc_control(num_episodes):
  for episode in range(num_episodes):
    episode_trace = []
    state = np.random.choice(game.states)
    initial_action = epsilon_greedy_action(state)

    next_state = game.next_state(state, initial_action)
    
    episodes = game.play_game(next_state)
    G = 0
    state = None
    visited = set()

    for s in reversed(len(episodes)):
      s,a = episodes[s]
      G = discount_factor*G + state_reward[s]

      if (s,a) not in visited:
        visited.add((s,a))
        Q[s][a] += step_size*(G - Q[s][a])