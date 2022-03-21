from random import randint, random
from xmlrpc.client import Boolean

MUTATION_RATE = 0.02
IDEAL_FITNESS = 10 # all 10 numbers even/odd

class Individual:
   def __init__(self, sequence: list = None)-> None:
      self.sequence = sequence
      if not sequence:
         self.sequence = []
         for i in range(10):
            self.sequence.append(randint(0, 99))       

def weighted_by(population: list, fitness: callable) -> list:
   weights = []
   for individual in population:
      weights.append(fitness(individual))
   return weights # not used. using fitness instead

def fitness(individual: Individual):
   fitness = 0
   for elem in individual.sequence:
      fitness += elem % 2 # increases when odd 
   return fitness

# more fitness => more chances to be selected
# TODO: make population sorted by fitness
def weighted_random_choices(population: list, weights: list, amount: int) -> tuple:
   # weights and amount not used for simplification
   parent1 = parent2 = None   
   i = 0
   while parent1 == None:
      rand_fitness = randint(0, IDEAL_FITNESS)
      if rand_fitness < fitness(population[i % len(population)]):
         parent1 = population[i % len(population)]
      i+=1
   i = 0
   while parent2 == None or parent2 is parent1:
      rand_fitness = randint(0, IDEAL_FITNESS)
      if rand_fitness < fitness(population[i % len(population)]):
         parent2= population[i % len(population)]
      i+=1
   return parent1, parent2

def mutate(child: Individual) -> None:
   random_index = randint(0, len(child.sequence)- 1)
   random_value = randint(0, 99) # mutation
   child.sequence[random_index] = random_value 

def best_individual(population: list) -> Individual:
   best = population[0]
   for i in range(1, len(population)):
      current_fitness = fitness(population[i])
      if current_fitness > fitness(best):
         best = population[i]   
   return best

def fit_enough(population: list) -> Boolean:
   return fitness(best_individual(population)) == 10

def genetic_algorithm(population: list, fitness: callable) -> tuple:
   global MUTATION_RATE
   generation = 0

   while not fit_enough(population):
      weights = weighted_by(population, fitness)  # same as fitness proprety
      next_population = []
   
      for i in range(0, len(population)):
         parent1, parent2 = weighted_random_choices(population, weights, 2)
         child = reproduce(parent1, parent2)
         
         if random() < MUTATION_RATE:
            mutate(child)
   
         next_population.append(child)
      generation += 1
      print_population(population, generation)
      population = next_population
   return best_individual(population), generation

def reproduce(parent1, parent2):
   n = len(parent1.sequence)
   c = randint(1, n)
   seq1 = parent1.sequence[:c]
   seq2 = parent2.sequence[c:]
   full_seq = seq1 + seq2
   child = Individual(full_seq)
   return child

def print_population(population: list, generation: int) -> None: # debug only
   print(f"Generation: {generation}")
   for individual in population:
      print(f"{individual.sequence}")

individuals = []
for i in range(20):
   individuals.append(Individual())

best, generations = genetic_algorithm(individuals, fitness)
print(f"Best: {best.sequence} ({generations} generations)")