import chess
import move_generator as gen
import evaluation
import random
from data import read


def get_correctness_rate(params):
   games = open('data/ficsgamesdb_search_122216.pgn')
   compared_c = 0
   correct_c = 0
   for position, good_move in read.get_move(games):
      params_move = position.push(gen.generate_move(position, params))
      if params_move == good_move:
         correct_c += 1
      compared_c += 1
      if(compare_c > 200):
         break
   
   print("correct_rate: {0}".format(correct_c / compared_c))
   return correct_c / compared_c 

def generate_offspring_param(param1, param2):
   mutation_chance = .005
   param1_b = '{:016b}'.format(param1)
   param2_b = '{:016b}'.format(param2)
   offspring_param = ''

   for i in range(len(param1_b)):
      if random.randint(0, 1) == 0:
         offspring_param += param1_b[i]
      else: 
         offspring_param += param2_b[i]

      if random.random() < .005:
         if offspring_param[i] == '1':
            offspring_param[i] = '0'
         else:
            offspring_param[i] = '1'

   return int(offspring_param, 2)  

def get_offspring_uniform_crossover(parent1, parent2):
   cross_rate = 0.75
   if random.random > cross_rate:
      return parent1
   offspring = evaluation.EvalParams(False)
   for param in range(offspring.param_c):
      param_val = generate_offspring_param(parent1.params[param], parent2.params[param])
      offspring.params[param] = param_val

   return offspring

def create_parent_pairs(population):
   total_fitness = sum([p.fitness for p in population])
   parents = []
   while len(parents) < len(population):
      parents.append(random.choices(population, 
                     weights=[p.fitness/total_fitness for p in population], k=2))
      
   return parents      

def generate_next_population(population):
   parents = create_parent_pairs(population)
   next_population = []
   for pair in parents:
     next_population.append(get_offspring_uniform_crossover(pair[0], pair[1]))
      
   return next_population 
      
def set_fitness(params):
   params.fitness = get_correctness_rate(params)

def set_population_fitness(population):
   for params in population:
      set_fitness(params)

def create_population(population_size):
   return [evaluation.EvalParams(True) for _ in range(population_size)]

if __name__ == "__main__":
   population_size = 100
   generations = 100
   current_pop = create_population(population_size)
   for generation in range(generations):
      print("getting fitness for generation {0}".format(generation)) 
      print("population count is {0}".format(len(current_pop)))
      set_population_fitness(current_pop)
      print("population fitness: ")
      print([p.fitness for p in current_pop])
      current_pop = generate_next_population(current_pop)
   
   with open("strongest.txt", "w") as file:
      for p in population:
         file.write("params({0}): {1}\n".format(p.fitness, p.params))
   
