from copy import copy, deepcopy
import math
from random import randint, random, shuffle
from numpy import Infinity
from math import dist
from canvas import Canvas

MAX_X = 100
MAX_Y = 100
N_CITIES = 15
CITIES = []
DISTANCE = []

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


   def calc_sucessors(self):
      self.sucessors = []
      for i in range(N_CITIES):
         for j in range(i+1, N_CITIES):
            swapped = self._swapped_copy(i, j)
            self.sucessors.append(swapped)
      return self.sucessors

   def _swapped_copy(self, a, b):
      state_cpy = deepcopy(self)
      state_cpy.cities[a] = self.cities[b]
      state_cpy.cities[b] = self.cities[a] 
      state_cpy._calc_value()
      return state_cpy

   def random_sucessor(self):
      assert self.sucessors
      return self.sucessors[randint(0, len(self.sucessors) - 1)]

   def highest_valuated(self):
      assert self.sucessors
      neighbor = None
      highest = Infinity
      for s in range(len(self.sucessors)):
        if self.sucessors[s].value < highest:
            highest = self.sucessors[s].value
            neighbor = self.sucessors[s]
      return neighbor 


for i in range(N_CITIES):
   CITIES.append(City(randint(0, MAX_X), randint(0, MAX_Y)))
best_value = Infinity

for i in range(N_CITIES):
   DISTANCE.append([])
   for j in range(N_CITIES):
      distance = dist([CITIES[i].x, CITIES[i].y] , [CITIES[j].x, CITIES[j].y])
      DISTANCE[i].append(distance)
points = [(p.x, p.y) for p in CITIES]

def hill_climbing():
   global points
   current = State([i for i in range(N_CITIES)])
   shuffle(current.cities)
   i = 0
   t = 1
   while True:
      t -= 1/100
      if t <= 0:
         return current

      current.calc_sucessors()
      next_state = current.random_sucessor()  
      delta_E = next_state.value - current.value
      
      p = pow(math.e, delta_E/t)
      if delta_E > 0 or random() < p: 
         current = next_state 
         
      c.draw(points, current.cities)
      i+=1






c = Canvas(MAX_Y, MAX_X, 6)
hill_climbing()