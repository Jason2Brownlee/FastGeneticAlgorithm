# simple genetic algorithm in python
# version 06
# jason brownlee
import numpy

# evaluate the fitness of a string, onemax
def fitness(candidate):
    # sum of the values
    return candidate['bitstring'].sum()

# select parents of next generation using tournament selection
def tournament_selection(rng, population, n_strings, n_rounds):
    # preallocate memory for parents of next generation
    parents = numpy.empty(len(population), dtype=object)
    # select all draws from the population
    ixs = rng.integers(0, high=n_strings-1, size=n_rounds*n_strings, endpoint=True)
    # enumerate draws and select best fitness from each set of rounds
    for i in range(0, len(ixs), n_rounds):
        # select the indexes for this round
        indexes = ixs[i:i+n_rounds]
        # find the candidate with the best fitness in this round
        parents[int(i/n_rounds)] = max(population[indexes], key=lambda d: d['fitness'])
    return parents

# point mutations of a candidate bit strings
def mutate(candidate, mut_choices):
    # get the bitstring
    bitstring = candidate['bitstring']
    # flip bits for those those indexes that are to be mutated
    bitstring[mut_choices] = 1 - bitstring[mut_choices]

# perform one point crossover
def one_point_crossover(cross_choice, cross_point, parent1, parent2, child1, child2):
    # copy data from parents into children
    numpy.copyto(child1['bitstring'], parent1['bitstring'])
    numpy.copyto(child2['bitstring'], parent2['bitstring'])
    # conditionally perform crossover
    if cross_choice:
        # copy remaining bits from parent 2 into child 1
        child1['bitstring'][cross_point:] = parent2['bitstring'][cross_point:]
        # copy remaining bits from parent 1 into child 2
        child2['bitstring'][cross_point:] = parent1['bitstring'][cross_point:]
    return child1, child2

# run the genetic algorithm and return the best result
def genetic_algorithm(r_seed, n_strings, length, n_epochs, n_rounds, m_rate, c_rate):
    # keep track of the best result
    best_fitness = best_string = -1.0
    # seed the random number generator
    rng = numpy.random.default_rng(r_seed)
    # create the initial population
    pop = numpy.array([{'bitstring': rng.integers(0, high=1, size=length, dtype=numpy.int64, endpoint=True)} for _ in range(n_strings)])
    # create empty child population
    children = numpy.array([{'bitstring': numpy.zeros((length,), dtype=numpy.int64)} for _ in range(n_strings)])
    # preallocate arrays for random choices
    cross_rands = numpy.zeros(int(n_strings/2), dtype=numpy.float32)
    mut_rands = numpy.zeros(n_strings*length, dtype=numpy.float32)
    # run the algorithm
    for epoch in range(n_epochs):
        # evaluate the initial population
        for candidate in pop:
            # evaluate candidate and store score
            candidate['fitness'] = fitness(candidate)
            # check for a new best
            if candidate['fitness'] > best_fitness:
                best_fitness, best_string = candidate['fitness'], candidate['bitstring'].copy()
        # report best
        print(f'>{epoch} fitness={best_fitness}')
        # select parents
        parents = tournament_selection(rng, pop, n_strings, n_rounds)
        # pre-determine all crossover choices, one for each pair
        cross_choices = rng.random(dtype=numpy.float32, out=cross_rands) <= c_rate
        cross_points = rng.integers(low=1, high=length-2, size=int(n_strings/2), endpoint=True, dtype=numpy.int64)
        # pre-determine all mutation choices, one for each bit
        mut_choices = rng.random(dtype=numpy.float32, out=mut_rands) <= m_rate
        # create children, 2 at a time, from selected parents
        for i in range(0, n_strings, 2):
            # retrieve children
            child1, child2 = children[i], children[i+1]
            # wipe fitness for safety
            child1['fitness'] = child2['fitness'] = None
            # retrieve cross choice
            cross_choice = cross_choices[int(i/2)]
            cross_point = cross_points[int(i/2)]
            # perform one point crossover
            one_point_crossover(cross_choice, cross_point, parents[i], parents[i+1], child1, child2)
            # mutate children
            mutate(child1, mut_choices[(i*length):(i*length+length)])
            mutate(child2, mut_choices[((i+1)*length):((i+1)*length+length)])
        # swap parents and children populations
        pop, children = children, pop
    # return best candidate discovered
    return {'fitness':best_fitness, 'bitstring':best_string}

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
