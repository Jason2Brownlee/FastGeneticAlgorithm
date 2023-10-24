# simple genetic algorithm in python
# version 07
# jason brownlee
import numpy

# select parents of next generation using tournament selection
def tournament_selection(parents, rng, population, n_strings, n_rounds):
    # select all draws from the population
    ixs = rng.integers(0, n_strings-1, n_rounds*n_strings, numpy.int64, True)
    # enumerate draws and select best fitness from each set of rounds
    for i in range(0, len(ixs), n_rounds):
        # select the indexes for this round
        indexes = ixs[i:i+n_rounds]
        # find the candidate with the best fitness in this round
        parents[int(i/n_rounds)] = max(population[indexes], key=lambda d: d['fitness'])

# run the genetic algorithm and return the best result
def genetic_algorithm(r_seed, n_strings, length, n_epochs, n_rounds, m_rate, c_rate):
    # keep track of the best result
    best_fitness = best_string = -1.0
    # seed the random number generator
    rng = numpy.random.default_rng(r_seed)
    # create the initial population
    pop = numpy.array([{'bitstring': rng.integers(0, 1, length, numpy.int64, True)} for _ in range(n_strings)])
    # create empty child population
    children = numpy.array([{'bitstring': numpy.zeros(length, numpy.int64)} for _ in range(n_strings)])
    # preallocate arrays for random choices
    cross_rands = numpy.zeros(int(n_strings/2), numpy.float32)
    mut_rands = numpy.zeros(n_strings*length, numpy.float32)
    # preallocate memory for parents of next generation
    parents = numpy.empty(n_strings, object)
    # run the algorithm
    for epoch in range(n_epochs):
        # evaluate the initial population
        for candidate in pop:
            # evaluate candidate and store score
            candidate['fitness'] = candidate['bitstring'].sum()
            # check for a new best
            if candidate['fitness'] > best_fitness:
                best_fitness, best_string = candidate['fitness'], candidate['bitstring'].copy()
        # report best
        print(f'>{epoch} fitness={best_fitness}')
        # select parents
        tournament_selection(parents, rng, pop, n_strings, n_rounds)
        # predetermine all crossover choices, one for each pair
        cross_choices = rng.random(None, numpy.float32, cross_rands) <= c_rate
        cross_points = rng.integers(1, length-2, int(n_strings/2), numpy.int64, True)
        # predetermine all mutation choices, one for each bit
        mut_choices = rng.random(None, numpy.float32, mut_rands) <= m_rate
        # create children, 2 at a time, from selected parents
        for i in range(0, n_strings, 2):
            # retrieve children
            child1, child2 = children[i], children[i+1]
            # wipe fitness for safety
            child1['fitness'] = child2['fitness'] = None
            # get the child bitstrings
            bs1, bs2 = child1['bitstring'], child2['bitstring']
            # perform conditional crossover
            if cross_choices[int(i/2)]:
                # get the crossover point
                cp = cross_points[int(i/2)]
                # copy bits from parents into child 1
                bs1[:cp] = parents[i]['bitstring'][:cp]
                bs1[cp:] = parents[i+1]['bitstring'][cp:]
                # copy bits from parents into child 2
                bs2[:cp] = parents[i+1]['bitstring'][:cp]
                bs2[cp:] = parents[i]['bitstring'][cp:]
            else:
                # copy data from parents into children
                numpy.copyto(bs1, parents[i]['bitstring'])
                numpy.copyto(bs2, parents[i+1]['bitstring'])
            # mutate first child
            mc = mut_choices[(i*length):(i*length+length)]
            bs1[mc] = 1 - bs1[mc]
            # mutate second child
            mc = mut_choices[((i+1)*length):((i+1)*length+length)]
            bs2[mc] = 1 - bs2[mc]
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
