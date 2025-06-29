import numpy as np

places = [1,2,3,4,5,6,7,8,9]
blank_places = places
filled_place = []

class tic_tac_toe:
  def __init__():
  def update_blank_places(place):
      list = []
      for _ in blank_places:
        if _ != place:
          list.append(_)
      blank_places = list

  def sample_next_place(blank_places):
    num_blank_places = len(blank_places)
    prob = [1/num_blank_places]*num_blank_places
    next_place = np.random.choice(blank_places, p = prob)
    
    update_blank_places(next_place)

    return next_place
    
  def is_terminal_state(state):
    filled_place , blank_place = state
    terminal_list = [[1,2,3],[4,5,6],[7,8,9],
                    [1,4,7],[2,5,8],[3,6,9],
                    [1,5,9],[7,5,3]]
    
    if filled_place in terminal_list:
      return True
    
    return False

  def update_state(place):
    filled_place.append(place)
    curret_state = (filled_place, blank_places)
    return curret_state

  def play_game(start_place = None):
    trajectory = []
    intial_place = sample_next_place(blank_places)
    filled_place.append(intial_place)
    if place is not None:
      filled_place.append(start_place)
      update_blank_places(start_place)

    else:
        intial_place = sample_next_place(blank_places)
        filled_place.append(intial_place)
    
    current_state = (filled_place, blank_places)

    while not is_terminal_state(current_state):
      place = sample_next_place(blank_places)
      trajectory.append(place)
      current_state = update_state(place)

    return trajectory

print(play_game())