from copy import copy, deepcopy
import math
from random import randint, random, shuffle
from numpy import Infinity
from math import dist
from canvas import Canvas

MAX_X = 100
MAX_Y = 100
N_CITIES = 20
CITIES = []
DISTANCE = []
DECREASE_RATE = .9999
MIN_TEMPERATURE = 1
MAX_TEMPERATURE = 100000
 
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

   def _swapped_copy(self, a, b):
      state_cpy = deepcopy(self)
      state_cpy.cities[a] = self.cities[b]
      state_cpy.cities[b] = self.cities[a] 
      state_cpy._calc_value()
      return state_cpy

   def random_sucessor(self):
      rand_index_a = randint(0, len(self.cities) - 1)
      rand_index_b = randint(0, len(self.cities) - 1)
      while rand_index_a == rand_index_b:
         rand_index_b = randint(0, len(self.cities) - 1)
      return self._swapped_copy(rand_index_a, rand_index_b)


for i in range(N_CITIES):
   CITIES.append(City(randint(0, MAX_X), randint(0, MAX_Y)))
best_value = Infinity

for i in range(N_CITIES):
   DISTANCE.append([])
   for j in range(N_CITIES):
      distance = dist([CITIES[i].x, CITIES[i].y] , [CITIES[j].x, CITIES[j].y])
      DISTANCE[i].append(distance)
points = [(p.x, p.y) for p in CITIES]

def simulated_annealing():
   global points
   current = State([i for i in range(N_CITIES)])
   shuffle(current.cities)

   temperature = MAX_TEMPERATURE

   while True:
      canvas.get_events()
      temperature  *= DECREASE_RATE
      if temperature <= MIN_TEMPERATURE:
         return current

      next_state = current.random_sucessor()  
      delta_E = current.value - next_state.value
      
      p = pow(math.e, delta_E/temperature)
      if delta_E > 0:
         current = next_state 
      elif p > random(): 
         current = next_state

      canvas.draw(points, current.cities)
   

canvas = Canvas(MAX_Y, MAX_X, 6)
simulated_annealing()
while True:
   canvas.get_events()