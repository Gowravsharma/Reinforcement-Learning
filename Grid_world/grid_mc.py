import grid_game as game
import numpy as np

game1 = game.Grid_World(6,6)

discount_factor = 1
epsilon = 0.1
step_size = 0.01
num_episodes = 10000
num_states = game1.total_states


state_value_ev = np.zeros(num_states)
state_value_fv = np.zeros(num_states)

state_reward = -np.ones(num_states)
state_reward[num_states-1] = 2

print(f'number of states {num_states}')

class Monte_Carlo:
  def __init__(self,discount_factor = 1, step_size = 0.01,num_states = game1.total_states,Q = {},):
    self.discount_factor = discount_factor
    self.step_size = step_size
    self.num_states = num_states
    self.Q = Q # Q_val Dictionary

    if not self.Q:
      self.Q = {
            s: {a: 0.0 for a in game1.moves
                if not ((a == 'up' and s - game1.rows < 0) or
                        (a == 'down' and s + game1.rows >= num_states) or
                        (a == 'right' and (s + 1) % game1.rows == 0) or
                        (a == 'left' and s % game1.rows == 0))}
            for s in range(num_states)
          }

  def every_visit_mc(num_episodes):
    for i in range(num_episodes):
      initial_state = np.random.choice(game1.states)
      episode = game1.play_game(initial_state)

      G = 0
      visited_states = set()
      state = None
      for s in reversed(range(len(episode))):
        state = episode[s][0]
        reward = state_reward[state]

        G = discount_factor*G + reward

        state_value_ev[state]+= step_size*(G - state_value_ev[state])
      #print(state)

  def first_visit_mc(num_episodes):
    for episodes_num in range(num_episodes):
      initial_state = np.random.choice(game1.states)
      episodes = game1.play_game(initial_state) # returns [[state, action], ...]

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
        state_value_fv[state] += step_size*(G - state_value_fv[state])

  def epsilon_greedy_action(self, state, epsilon = 0.1):
    if np.random.rand() < epsilon:
      return game1.sample_next_action
    else:
      q_values = self.Q[state]
      return max(q_values, key= q_values.get)

#if __name__ == '__main__':
#  every_visit_mc(num_episodes)
#  print('Every Visit Monte carlo:' ,'\n', state_value_ev.reshape((4,4)))


#if __name__ == '__main__':
#  first_visit_mc(num_episodes)
#  print('First Visit Monte carlo:' ,'\n', state_value_fv.reshape((4,4)))

# Epsilon Greedy policy
  

def update_transition_policy(self,epsilon = 0.1):
  Q = self.Q
  new_policy = {}
  
  for state in range(num_states):
    valid_actions = [a for a,p in game1.transition_prob[state].items() if p > 0]

    if not valid_actions:
      new_policy[state] = {a:0 for a in game1.moves}
      continue
    
    #finding greedy action among valid action comparing Q value
    best_action = max(valid_actions, key = lambda a: Q[state][a])
    
    # Distributing probabilities : Epsilon greedily
    num_actions = len(valid_actions)
    probs = {}
    for a in valid_actions:
      if a == best_action:
        probs[a] = 1 - epsilon + (epsilon/num_actions)
      else:
        probs[a] = epsilon/num_actions

    new_policy[state] = {a: probs.get(a, 0.0) for a in game1.moves}
  
  return new_policy

def every_visite_mc_control(self,num_episodes):
  Q = self.Q
  for episode in range(num_episodes):
    episode_trace = []
    state = np.random.choice(game1.states)
    initial_action = self.epsilon_greedy_action(Q,state)

    next_state = game1.next_state(state, initial_action)
    
    episodes = game1.play_game(next_state)
    G = 0
    state = None
    visited = set()

    for s in reversed(range(len(episodes))):
      s,a = episodes[s]
      G = discount_factor*G + state_reward[s]

      if (s,a) not in visited:
        visited.add((s,a))
        #print(s,a)
        Q[s][a] += step_size*(G - Q[s][a])
    
    game1.transition_prob = update_transition_policy(Q)


def print_path_gridworld(self, initial_state, rows, cols):
  game1.rows , game1.cols = rows, cols

  # path
  agent_trajectory = game1.play_game(initial_state)
  
  action_arrows = {'up':'↑','down':'↓','left': '←', 'right':'→'}
  
  # initializing grid
  grid = np.full((rows,cols), '.', dtype = str)

  for state, action in agent_trajectory:
    row_ = state//rows
    col_ = state%cols
    grid[row_][col_] = action_arrows.get(action,'?')

  for row in grid:
    print(' '.join(row))
  print(agent_trajectory)  

print_path_gridworld(0,5,5)

#print(game.play_game(0))
#print(Q)