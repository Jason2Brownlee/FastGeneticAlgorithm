# simple genetic algorithm in python
# version 01
# jason brownlee
import random

# helper to generate a random float in [0, 1]
def rand_float():
    return random.random()

# helper to generate a random bit in {0, 1}
def rand_bit():
    return random.randint(0, 1)

# helper to generate random integer in [0, max] (inclusive)
def rand_int(max_value):
    return random.randint(0, max_value)

# create a single candidate of random bits of a given length
def random_bitstring(length):
    return {'bitstring':[rand_bit() for _ in range(length)]}

# create a new candidate as a copy of another candidate's bitstring
def copy_bitstring(other):
    return {'bitstring': other['bitstring'].copy()}

# evaluate the fitness of a string, onemax
def fitness(candidate):
    # sum of the values
    return sum(candidate['bitstring'])

# perform tournament selection (best of n independently random draws)
def tournament_selection(population, n_strings, n_rounds):
    # select initial candidate (first round)
    ix = rand_int(n_strings - 1)
    selected = population[ix]
    # perform the remaining rounds
    for _ in range(n_rounds - 1):
        # select a random candidate
        ix = rand_int(n_strings - 1)
        candidate = population[ix]
        # check if the fitness is better than the current best
        if candidate['fitness'] > selected['fitness']:
            # we have a new best
            selected = candidate
    return selected

# point mutations of a candidate bit strings
def mutate(candidate, m_rate):
    # get the bitstring
    bitstring = candidate['bitstring']
    # enumerate all bits in the genome
    for i in range(len(bitstring)):
        # conditionally perform point mutations
        if rand_float() <= m_rate:
            # flip the bit
            bitstring[i] = 1 - bitstring[i]

# perform one point crossover
def one_point_crossover(parent1, parent2, point):
    # copy parent into child
    child = copy_bitstring(parent1)
    # copy over the remaining bits
    end = len(parent2['bitstring'])
    child['bitstring'][point:end] = parent2['bitstring'][point:end]
    return child

# run the genetic algorithm and return the best result
def genetic_algorithm(r_seed, n_strings, length, n_epochs, n_rounds, m_rate, c_rate):
    # keep track of the best result
    best = None
    # seed the random number generator
    random.seed(r_seed)
    # create the initial population
    pop = [random_bitstring(length) for _ in range(n_strings)]
    # run the algorithm
    for epoch in range(n_epochs):
        # evaluate the initial population
        for candidate in pop:
            # evaluate candidate and store score
            candidate['fitness'] = fitness(candidate)
            # check for a new best
            if best is None or candidate['fitness'] > best['fitness']:
                best = candidate
        # report best
        print(f">{epoch} fitness={best['fitness']}")
        # select parents
        parents = [tournament_selection(pop, n_strings, n_rounds) for _ in range(n_strings)]
        # clear out the list ready for the children
        pop.clear()
        # create children, 2 at a time, from selected parents
        for i in range(0, n_strings, 2):
            # select parents
            p1 = parents[i]
            p2 = parents[i + 1]
            # conditionally perform crossover
            if rand_float() <= c_rate:
                # select crossover point
                point =  1 + rand_int(length - 2)
                # perform one-point crossover
                child1 = one_point_crossover(p1, p2, point)
                child2 = one_point_crossover(p2, p1, point)
            else:
                # copy parents
                child1 = copy_bitstring(p1)
                child2 = copy_bitstring(p2)
            # mutate children
            mutate(child1, m_rate)
            mutate(child2, m_rate)
            # store children
            pop.append(child1)
            pop.append(child2)
    return best

# protect the entry point
if __name__ == '__main__':
    # configuration
    r_seed = 1
    n_strings = 100
    length = 1000
    n_epochs = 500
    n_rounds = 3
    m_rate = 1.0 / length
    c_rate = 0.95
    # run the genetic algorithm
    best = genetic_algorithm(r_seed, n_strings, length, n_epochs, n_rounds, m_rate, c_rate)
    print('Done')
