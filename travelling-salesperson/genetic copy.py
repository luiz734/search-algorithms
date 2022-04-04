from copy import deepcopy
from json.encoder import INFINITY
from random import randint, random, shuffle
from math import dist
from canvas import Canvas

MUTATION_RATE = 0.25
MAX_X = 100
MAX_Y = 100
N_CITIES = 30
POPULATION_SIZE = 100
canvas = Canvas(MAX_Y, MAX_X, 6)
generations = 0
best_generation = 0
display_text = []
connections = []
# const
CITIES = []
DISTANCE = []

class City:
   def __init__(self, x, y) -> None:
      self.x = x
      self.y = y

# pre calculated values
for i in range(N_CITIES):
   CITIES.append(City(randint(0, MAX_X), randint(0, MAX_Y)))
best_value = INFINITY

for i in range(N_CITIES):
   DISTANCE.append([])
   for j in range(N_CITIES):
      distance = dist([CITIES[i].x, CITIES[i].y] , [CITIES[j].x, CITIES[j].y])
      DISTANCE[i].append(distance)
points = [(p.x, p.y) for p in CITIES]
# # # # # 



class Individual:
   def __init__(self, cities: list = None)-> None:
      if cities:
         self.cities = cities
      else:
         self.cities = [i for i in range(0, N_CITIES)]
         shuffle(self.cities)
      self.calc_fitness()

   def calc_fitness(self):
      global CITIES 
      self.fitness = 0 # total dist
      for i in range(0, len(self.cities)):
         city_index_1 = self.cities[i % N_CITIES]
         city_index_2 = self.cities[(i + 1) % N_CITIES]
         self.fitness += DISTANCE[city_index_1][city_index_2]

   def swap_cities(self, a, b):
      tmp = self.cities[a]
      self.cities[a] = self.cities[b]
      self.cities[b] = tmp

# TODO: check if it works as expected
def wighted_index(population: list):
   weights = [1/(pow(individual.fitness, 8)+1) for individual in population]
   total = sum(weights)
   weights = [i/total for i in weights]
   total = sum(weights)
   r = random()
   w = 0
   for i in range(len(weights)):
      w += weights[i]
      if r < w:
         return i
   return len(weights) - 1

def weighted_random_choices(population: list, amount: int) -> tuple:
   # weights and amount not used for simplification
   parents = []

   i = 0
   while i < amount:
      new_parent = population[wighted_index(population)]
      if new_parent not in parents:
         parents.append(new_parent)
         i += 1
   return tuple(parents) 

def mutate(child: Individual) -> None:
   for i in range(N_CITIES // 5):
      random_index_1 = randint(1, len(child.cities) - 1)
      random_index_2 = randint(1, len(child.cities) - 1)
      current_child = deepcopy(child)
      child.swap_cities(random_index_1, random_index_2)
      child.calc_fitness()
      # child = child if child.fitness < current_child.fitness else current_child

def best_individual(population: list) -> Individual:
   best = population[0]
   for i in range(1, len(population)):
      current_fitness = population[i].fitness
      if current_fitness < best.fitness:
         best = population[i]   
   return best

def fit_enough(population: list):
   global best_value, generations, best_generation, connections
   current_best = best_individual(population)

   if current_best.fitness < best_value:
      best_value = current_best.fitness
      connections = current_best.cities
      best_generation = generations
      print(f"Best: {best_value} ({generations} gen) {current_best.cities}")
   
   # never enough
   return False

def genetic_algorithm(population: list) -> tuple:
   global MUTATION_RATE, generations, best_generation, display_text, points, connections
   
   while not fit_enough(population):
      canvas.get_events()
      next_population = []
      # print(generation)
      for i in range(0, len(population)):
         parent1, parent2 = weighted_random_choices(population, 2)
         child = reproduce(parent1, parent2)
         
         if random() < MUTATION_RATE:
            mutate(child)
   
         next_population.append(child)
      generations += 1
      MUTATION_RATE -= 1/10000
      if MUTATION_RATE < 0.05:
         MUTATION_RATE = 0.05

      # print_population(population, generation)
      # print(fitness(best_individual(population)))
      # canvas.draw_text([0, 0], [f"GEN: {generations}"])
      display_text = [
         f"N Cities: {N_CITIES}",
         f"Mutation Rate: {MUTATION_RATE}",
         f"BestFit: {best_value}",
         f"BestGen: {best_generation}",
         f"Current Gen: {generations}"]     
      canvas.draw(points, connections, display_text) 
      population = next_population
   return best_individual(population), generations

def reproduce(parent1, parent2):
   n = N_CITIES 
   rng_start = randint(0, n - 2)
   rng_end = randint(rng_start + 1, n)
   child = parent1.cities[rng_start:rng_end]
   for i in range(N_CITIES):
      if parent2.cities[i] not in child:
         child.append(parent2.cities[i])
   # print(rng_start, rng_end)
   return Individual(child)

population = []
for i in range(POPULATION_SIZE):
   population.append(Individual())

genetic_algorithm(population)
print(f"Best: {best_value}")
