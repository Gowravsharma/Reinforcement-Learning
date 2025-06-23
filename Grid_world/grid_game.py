import numpy as np

#Grid dimensions
rows,cols = 4,4
total_states = rows*cols
states = np.arange(0,total_states,1) # [0,1,2,..., 15]
terminal_state = total_states-1
moves = ['up','down','left','right']

transition_prob = {} #policy

for i in range(total_states):
  transition_prob[i] = {}
  valid_actions = []
  for j in moves:
    if (j == 'up' and i - cols < 0) or \
      (j == 'down' and i + cols >= 16) or \
      (j == 'right' and (i + 1) % cols == 0) or \
      (j == 'left' and i % cols == 0):
      transition_prob[i][j] = 0
      continue
    valid_actions.append(j)

  prob = 1 / len(valid_actions)
  for j in valid_actions:
    transition_prob[i][j] = prob


def sample_next_action(from_state):
  actions_probs = [(a, p) for a, p in transition_prob[from_state].items() if p > 0]
  actions, probs = zip(*actions_probs)
  return np.random.choice(actions, p=probs)

#print(sample_next_action(14)) for debuging
#for i in range(16):
#  print(sample_next_action(i))

def next_state(current_state, action):
  if(action == 'up'):
    current_state = current_state - cols
  if(action == 'down'):
    current_state = current_state + cols
  if(action == 'left'):
    current_state = current_state - 1
  if(action == 'right'):
    current_state = current_state + 1
  return current_state

def is_terminal(state):
  return state == rows*cols - 1

def play_game(start_state):
  current_state = start_state
  sampled_states = []
  while not is_terminal(current_state):
    action = sample_next_action(current_state)
    sampled_states.append([current_state,action])
    current_state = next_state(current_state, action)
  return sampled_states


if __name__ == '__main__':
  print(play_game(0))  