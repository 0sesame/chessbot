import chess
import move_generator as gen
import evaluation
from data import read


def get_correctness_rate(params):
   games = open('data/ficsgamesdb_search_122216.pgn')
   compared_c = 0
   correct_c = 0
   for position, good_move in read.get_move(games):
      print(position)
      print("--------------------------------------")
      print(good_move)
      print("--------------------------------------")
      params_move = position.push(gen.generate_move(position, params))
      if params_move == good_move:
         correct_c += 1
      compared_c += 1
      
   return correct_c / compared_c 
      
   

def set_fitness(params):
   params.fitness = get_correctness_rate(params)

def set_population_fitness(population):
   for params in population:
      set_fitness(params)

def create_population(population_size):
   return [evaluation.EvalParams(True) for _ in range(population_size)]

if __name__ == "__main__":
   population_size = 5
   pop = create_population(population_size)
   set_population_fitness(pop)
   print([p.fitness for p in pop])
   
