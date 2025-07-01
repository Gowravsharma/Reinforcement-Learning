import numpy as np

places = [1,2,3,4,5,6,7,8,9]
blank_places = places
filled_place = []

class tic_tac_toe:
  filled_places = None
  blank_places = None
  places = [1,2,3,4,5,6,7,8,9]
  
  def __init__(self, blank_places = None, filled_places = None, trajectory = None):
    self.places = [1,2,3,4,5,6,7,8,9]
    self.blank_places = blank_places if blank_places is not None else self.places
    self.filled_places = filled_places if filled_places is not None else []
    self.trajectory = trajectory

  def update_blank_places(self, place):
      list = []
      for _ in blank_places:
        if _ != place:
          list.append(_)
      self.blank_places = list

  def sample_next_place(self,blank_places):
    num_blank_places = len(blank_places)
    prob = [1/num_blank_places]*num_blank_places
    next_place = np.random.choice(blank_places, p = prob)
    self.update_blank_places(next_place)

    return next_place
    
  def is_terminal_state(self, state):
    filled_place , blank_place = state
    terminal_list = [[1,2,3],[4,5,6],[7,8,9],
                    [1,4,7],[2,5,8],[3,6,9],
                    [1,5,9],[7,5,3]]
    
    if filled_place in terminal_list:
      return True
    
    return False

  def update_state(self, place):
    self.filled_place.append(place)
    curret_state = (filled_place, blank_places)
    return curret_state

  def play_game(self, start_place = None):
    trajectory = []
    intial_place = self.sample_next_place(blank_places)
    filled_place.append(intial_place)
    if place is not None:
      filled_place.append(start_place)
      self.update_blank_places(start_place)

    else:
        intial_place = self.sample_next_place(blank_places)
        filled_place.append(intial_place)
    
    current_state = (filled_place, blank_places)

    while not self.is_terminal_state(current_state):
      place = self.sample_next_place(blank_places)
      trajectory.append(place)
      current_state = self.update_state(place)

    return trajectory

print(play_game()) 
