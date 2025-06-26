import grid_game as game
import numpy as np

#discount_factor = 1
#epsilon = 0.1
#step_size = 0.01
#num_episodes = 10000
#num_states = game1.total_states


#state_value_ev = np.zeros(num_states)
#state_value_fv = np.zeros(num_states)

#state_reward = -np.ones(num_states)
#state_reward[num_states-1] = 2

#print(f'number of states {num_states}')

class Monte_Carlo:
  def __init__(self,env ,discount_factor = 1, step_size = 0.01 ,Q = None, state_value = None, state_reward = None):
    self.game1 = env
    self.policy = self.game1.transition_prob
    self.discount_factor = discount_factor
    self.step_size = step_size
    self.num_states = env.total_states
    self.state_value = state_value if state_value is not None else np.zeros(self.num_states)
    self.state_reward = state_reward if state_reward is not None else np.append(-np.ones(self.num_states - 1), 2) 
    self.Q = Q if  Q is not None else {
            s: {a: 0.0 for a in self.game1.moves
                if not ((a == 'up' and s - self.game1.rows < 0) or
                        (a == 'down' and s + self.game1.rows >= self.num_states) or
                        (a == 'right' and (s + 1) % self.game1.rows == 0) or
                        (a == 'left' and s % self.game1.rows == 0))}
            for s in range(self.num_states)
          }# Q_val Dictionary

#####################################################################
  def every_visit_mc(self,num_episodes):
    self.state_value = np.zeros_like(self.state_value)
    for i in range(num_episodes):
      initial_state = np.random.choice(self.game1.states)
      episode = self.game1.play_game(initial_state)

      G = 0
      #visited_states = set()
      state = None
      for s in reversed(range(len(episode))):
        state = episode[s][0]
        reward = self.state_reward[state]

        G = self.discount_factor*G + reward

        self.state_value[state]+= self.step_size*(G - self.state_value[state])
      #print(state)
#####################################################################
  def first_visit_mc(self, num_episodes):
    self.state_value = np.zeros_like(self.state_value)
    for episodes_num in range(num_episodes):
      initial_state = np.random.choice(self.game1.states)
      episodes = self.game1.play_game(initial_state) # returns [[state, action], ...]

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
          G = self.discount_factor*G + self.state_reward[s]
        self.state_value[state] += self.step_size*(G - self.state_value[state])
############################################
  def epsilon_greedy_action(self, state, epsilon = 0.1):
    if not self.Q[state]:
      return None # if Q[state] is Empty like terminal
    if np.random.rand() < epsilon:
      return self.game1.sample_next_action(state)
    else:
      q_values = self.Q[state]
      return max(q_values, key= q_values.get)

###############################################
  def update_transition_policy(self,epsilon = 0.1):
    Q = self.Q
    new_policy = {}
    
    for state in range(self.num_states):
      valid_actions = [a for a,p in self.policy[state].items() if p > 0]

      if not valid_actions:
        new_policy[state] = {a:0 for a in self.game1.moves}
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

      new_policy[state] = {a: probs.get(a, 0.0) for a in self.game1.moves}
    
    return new_policy

#######################################################
  def every_visit_mc_control(self,num_episodes):
    Q = self.Q
    for episode in range(num_episodes):
      episode_trace = []
      state = np.random.choice(self.game1.states)
      episodes = self.game1.play_game(state, self.policy)

      G = 0
      visited = set()

      for s in reversed(range(len(episodes))):
        state_,action_ = episodes[s]
        if action_ == None:
          continue
        G = self.discount_factor*G + self.state_reward[state_]

        if (state_,action_) not in visited:
          visited.add((state_,action_))
          #print(s,a)
          Q[state_][action_] += self.step_size*(G - Q[state_][action_])
      
      self.policy = self.update_transition_policy()



######################################################
  def print_path_gridworld(self, initial_state,policy = None):
    # path
    agent_trajectory = self.game1.play_game(initial_state, self.policy)
    
    action_arrows = {'up':'↑','down':'↓','left': '←', 'right':'→'}
    
    # initializing grid
    grid = np.full((self.game1.rows,self.game1.cols), '.', dtype = str)

    for state, action in agent_trajectory:
      row_ = state//self.game1.rows
      col_ = state%self.game1.cols
      grid[row_][col_] = action_arrows.get(action,'#')

    for row in grid:
      print(' '.join(row))
    print(agent_trajectory)  

########################################3
game1 = game.Grid_World(5,5)
mc = Monte_Carlo(env = game1)
mc.every_visit_mc_control(1000)
mc.print_path_gridworld(0)
