from sys import stderr
from copy import deepcopy
from random import randint, random, shuffle
from math import dist, e as euler

GUI_MODE = True 
if GUI_MODE:
   try:
      from canvas import Canvas
   except:
      stderr.write('Missing module "canvas". Switching to non-gui mode.\n')
      GUI_MODE = False
   else:
      MAX_X = 800
      MAX_Y = 600
      POINTS = []
N_CITIES = 21
CITIES = []
DISTANCE = []
COOLING_RATE = .999
MIN_TEMPERATURE = 1
MAX_TEMPERATURE = 10000
INPUT = [(571, 377), (189, 158), (367, 236), (479, 240), (97 , 14 ), (524, 59 ), (184, 212), (577, 171), (473, 386), (327, 436), (504, 343), (41 , 349), (    16 , 162), (288, 344), (170, 283), (720, 324), (312, 154), (642, 543), (238, 535), (789, 408), (276, 529)]

class City:
   def __init__(self, x, y) -> None:
      self.x = x
      self.y = y

class State:
   def __init__(self, cities) -> None:
      self.cities = cities 
      self._calc_value()

   def _calc_value(self):
      self.value = 0
      for i in range(N_CITIES):
         city_index_1 = self.cities[i % N_CITIES]
         city_index_2 = self.cities[(i + 1) % N_CITIES]
         self.value += DISTANCE[city_index_1][city_index_2]

   def _create_swapped_copy(self, a, b):
      swapped_copy = deepcopy(self)
      swapped_copy.cities[a] = self.cities[b]
      swapped_copy.cities[b] = self.cities[a] 
      swapped_copy._calc_value()
      return swapped_copy

   def create_random_sucessor(self):
      rand_index_a = randint(0, len(self.cities) - 1)
      rand_index_b = randint(0, len(self.cities) - 1)
      while rand_index_a == rand_index_b:
         rand_index_b = randint(0, len(self.cities) - 1)
      return self._create_swapped_copy(rand_index_a, rand_index_b)


# for i in range(N_CITIES):
#    CITIES.append(City(randint(0, MAX_X), randint(0, MAX_Y)))
for x, y in INPUT:
   CITIES.append(City(x, y))

def generate_distance_matrix():
   global POINTS
   for i in range(N_CITIES):
      DISTANCE.append([])
      for j in range(N_CITIES):
         distance = dist([CITIES[i].x, CITIES[i].y] , [CITIES[j].x, CITIES[j].y])
         DISTANCE[i].append(distance)
   if GUI_MODE:
      POINTS = [(p.x, p.y) for p in CITIES]

def simulated_annealing():
   global POINTS
   current_state = State([i for i in range(N_CITIES)])
   shuffle(current_state.cities)
   current_temperature = MAX_TEMPERATURE

   while True:
      if GUI_MODE:
         canvas.get_events()
      current_temperature  *= COOLING_RATE
      if current_temperature <= MIN_TEMPERATURE:
         return current_state

      next_state = current_state.create_random_sucessor()  
      energy_difference = current_state.value - next_state.value
      
      probability = pow(euler, energy_difference/current_temperature)
      if energy_difference > 0:
         current_state = next_state 
      elif probability > random(): 
         current_state = next_state

      if GUI_MODE:
         canvas.draw(POINTS, current_state.cities)
   
# ----------------------------------------
if GUI_MODE:
   canvas = Canvas(MAX_X, MAX_Y, 1)
generate_distance_matrix()
solutions = ""
for i in range(2):
  best_state = simulated_annealing()
  solutions += f"{best_state.cities} ({best_state.value})\n"
print(solutions)
# -----------------------------------------

if GUI_MODE:
   while True:
      canvas.get_events()