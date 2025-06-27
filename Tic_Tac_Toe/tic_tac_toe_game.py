import numpy as np

places = [1,2,3,4,5,6,7,8,9]
blank_places = places
filled_place = []

def sample_next_place(blank_places):
  num_blank_places = len(blank_places)
  prob = [1/num_blank_places]*num_blank_places
  next_place = np.random.choice(blank_places, probs = prob)
  list = []

  for _ in blank_places:
    if _ != next_place:
      list.append(_)
  blank_places = list

  return next_place
  
def is_terminal_state(state):
  

def update_state(place):
  filled_place.append(place)
  curret_state = (filled_place, blank_places)
  return curret_state

def play_game():
  intial_place = sample_next_place(blank_places)
  filled_place.append(intial_place)
  current_state = (filled_place, blank_places)

  while is_terminal_state(current_state):
    place = sample_next_place(blank_places)
    current_state = update_state(place)

