# simple genetic algorithm in python
# version 04
# jason brownlee
import numpy

# create a single candidate of random bits of a given length
def random_bitstring(rng, length):
    return {'bitstring': rng.integers(0, high=1, size=length, endpoint=True)}

# evaluate the fitness of a string, onemax
def fitness(candidate):
    # sum of the values
    return candidate['bitstring'].sum()

# perform tournament selection (best of n independently random draws)
def tournament_selection(rng, population, n_strings, n_rounds):
    # perform all rounds
    ixs = rng.integers(0, high=n_strings-1, size=n_rounds, endpoint=True)
    # take the first selection
    selected = population[ixs[0]]
    # check remaining selections
    for i in ixs[1:]:
        # check if the fitness is better than the current best
        if population[i]['fitness'] > selected['fitness']:
            # we have a new best
            selected = population[i]
    return selected

# point mutations of a candidate bit strings
def mutate(rng, candidate, m_rate):
    # get the bitstring
    bitstring = candidate['bitstring']
    # generate the probability of mutation for each bit
    values = rng.random(len(bitstring))
    # get boolean values for whether each bit should be mutated
    ixs = values <= m_rate
    # flip bits for those those indexes that are to be mutated
    bitstring[ixs] = 1 - bitstring[ixs]

# perform one point crossover
def one_point_crossover(rng, parent1, parent2, length, c_rate):
    # copy parents
    child1 = {'bitstring': parent1['bitstring'].copy()}
    child2 = {'bitstring': parent2['bitstring'].copy()}
    # conditionally perform crossover
    if rng.random() <= c_rate:
        # select crossover point
        i = rng.integers(1, length - 2, endpoint=True)
        # copy remaining bits from parent 2 into child 1
        child1['bitstring'][i:] = parent2['bitstring'][i:]
        # copy remaining bits from parent 1 into child 2
        child2['bitstring'][i:] = parent1['bitstring'][i:]
    return child1, child2

# run the genetic algorithm and return the best result
def genetic_algorithm(r_seed, n_strings, length, n_epochs, n_rounds, m_rate, c_rate):
    # keep track of the best result
    best = None
    # seed the random number generator
    rng = numpy.random.default_rng(r_seed)
    # create the initial population
    pop = [random_bitstring(rng, length) for _ in range(n_strings)]
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
        parents = [tournament_selection(rng, pop, n_strings, n_rounds) for _ in range(n_strings)]
        # clear out the list ready for the children
        pop.clear()
        # create children, 2 at a time, from selected parents
        for i in range(0, n_strings, 2):
            # perform one point crossover
            child1, child2 = one_point_crossover(rng, parents[i], parents[i+1], length, c_rate)
            # mutate children
            mutate(rng, child1, m_rate)
            mutate(rng, child2, m_rate)
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
