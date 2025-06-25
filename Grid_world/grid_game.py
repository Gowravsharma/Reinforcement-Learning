import numpy as np

class Grid_World:
  def __init__(self, rows, cols, moves = ['up','down','left','right'], transition_prob = {} ):
    self.rows = rows
    self.cols = cols
    self.moves = moves
    self.transition_prob = transition_prob
    self.total_states = rows*cols
    self.states = np.arange(0,self.total_states,1) # [0,1,2,..., termial_state]
    self.terminal_state = self.total_states - 1
    
    if not self.transition_prob:
      for i in range(self.total_states):
        transition_prob[i] = {}
        valid_actions = []
        for j in moves:
          if (j == 'up' and i - cols < 0) or \
            (j == 'down' and i + cols >= self.total_states) or \
            (j == 'right' and (i + 1) % cols == 0) or \
            (j == 'left' and i % cols == 0):
            transition_prob[i][j] = 0
            continue
          valid_actions.append(j)

        prob = 1 / len(valid_actions)
        for j in valid_actions:
          transition_prob[i][j] = prob
  def sample_next_action(self, from_state):
    actions_probs = [(a, p) for a, p in self.transition_prob[from_state].items() if p > 0]
    actions, probs = zip(*actions_probs)
    return np.random.choice(actions, p=probs)
      
  def next_state(self, current_state, action):
    if(action == 'up'):
      current_state = current_state - self.cols
    if(action == 'down'):
      current_state = current_state + self.cols
    if(action == 'left'):
      current_state = current_state - 1
    if(action == 'right'):
      current_state = current_state + 1
    return current_state

  def is_terminal(self, state):
    return state == self.terminal_state

  def play_game(self, start_state):
    current_state = start_state
    sampled_states = []
    while not self.is_terminal(current_state):
      action = self.sample_next_action(current_state)
      sampled_states.append([current_state,action])
      current_state = self.next_state(current_state, action)
    return sampled_states

#Grid dimensions
#rows,cols = 5,5
#total_states = rows*cols
#states = np.arange(0,total_states,1) # [0,1,2,..., termial_state]
#terminal_state = total_states-1
#moves = ['up','down','left','right']
#transition_prob = {} #policy
#print(sample_next_action(14)) for debuging
#for i in range(16):
#  print(sample_next_action(i))


if __name__ == '__main__':
  g1 = Grid_World(5,5)
  trajectory = g1.play_game(0)
  print(trajectory, '\nLenght of trajectory: ',len(trajectory))  