import numpy as np

places = [1,2,3,4,5,6,7,8,9]
blank_places = places
filled_place = []

class tic_tac_toe:
  places = [1,2,3,4,5,6,7,8,9]
  blank_places = places.copy()

  def __init__(self,trajectory = [], filled_place = []):
    self.filled_place = filled_place
    self.trajectory = trajectory

  def update_blank_places(self, place):
    tic_tac_toe.blank_places = [p for p in tic_tac_toe.blank_places if p != place]

  def sample_next_place(self):
    num_blank_places = len(tic_tac_toe.blank_places)

    if num_blank_places == 0:
      return None
    
    prob = [1/num_blank_places]*num_blank_places
    next_place = np.random.choice(tic_tac_toe.blank_places, p = prob)
    self.update_blank_places(next_place)

    return next_place
    
  def is_terminal_state(self, state):
    filled_place , blank_place = state
    terminal_lists = [[1,2,3],[4,5,6],[7,8,9],
                    [1,4,7],[2,5,8],[3,6,9],
                    [1,5,9],[3,5,7]]
    
    for lst in terminal_lists:
        if all(pos in filled_place for pos in lst):
            return True
    
    return False

  def update_state(self, place):
    self.filled_place.append(place)
    curret_state = (self.filled_place.copy(), tic_tac_toe.blank_places.copy())
    return curret_state 

  def play_game(self, start_place = None):
    
    if start_place is not None:
      self.trajectory.append(start_place)
      self.filled_place.append(start_place)
      self.update_blank_places(start_place)

    else:
        intial_place = self.sample_next_place()
        self.filled_place.append(intial_place)
    
    current_state = (self.filled_place.copy(), tic_tac_toe.blank_places.copy())

    while not self.is_terminal_state(current_state):
      place = self.sample_next_place()
      if place is None:
        break # no moves left
      self.trajectory.append(place)
      current_state = self.update_state(place)

    return self.trajectory

game1 = tic_tac_toe() 
print(game1.play_game())
 
