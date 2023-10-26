# simple genetic algorithm in python
# version 12
# jason brownlee
import numpy

# run the genetic algorithm and return the best result
def genetic_algorithm(r_seed, n_strings, length, n_epochs, n_rounds, m_rate, c_rate):
    # keep track of the best result
    best_fitness, best_string = -1.0, numpy.empty(length, numpy.int64)
    # seed the random number generator
    rng = numpy.random.default_rng(r_seed)
    # initialize the first population of bitstring
    bitstrings_pop = rng.integers(0, 1, (n_strings, length), numpy.int64, True)
    # preallocate memory for the children we will create
    bitstrings_children = numpy.empty((n_strings, length), numpy.int64)
    # empty array for all fitness scores
    fitness_pop = numpy.zeros(n_strings, numpy.int64)
    # preallocate arrays for random choices
    cross_rands = numpy.zeros(n_strings//2, numpy.float32)
    mut_rands = numpy.zeros((n_strings, length), numpy.float32)
    arranged = numpy.arange(n_strings)
    # indexes of selected parents
    parents = numpy.empty(n_strings, numpy.int64)
    # run the algorithm
    for epoch in range(n_epochs):
        # calculate fitness for current population (onemax)
        numpy.sum(bitstrings_pop, axis=1, dtype=numpy.int64, out=fitness_pop)
        # locate the candidate with the best fitness
        best_ix = numpy.argmax(fitness_pop)
        # check for new best
        if fitness_pop[best_ix] > best_fitness:
            # store the best fitness score and bit string
            best_fitness, best_string = fitness_pop[best_ix], bitstrings_pop[best_ix, :]
        # report best
        print(f'>{epoch} fitness={best_fitness}')
        # generate random indexes for the tournaments for each string
        torn_ixs = rng.integers(0, n_strings-1, (n_strings, n_rounds), numpy.int64, True)
        # find the index of the maximum fitness in each tournament
        tournament_winners = numpy.argmax(fitness_pop[torn_ixs], axis=1)
        # update the parents with the winners' indexes
        parents[:] = torn_ixs[arranged, tournament_winners]
        # generate random floats and choose all pairs to participate in crossover
        cross_choices = rng.random(None, numpy.float32, cross_rands) <= c_rate
        # choose a crossover point for all pairs of parents
        cross_points = rng.integers(1, length-2, n_strings//2, numpy.int64, True)
        # copy all selected parent bits to children
        numpy.copyto(bitstrings_children, bitstrings_pop[parents,:])
        # perform one-point crossover where needed
        for i in range(0, n_strings, 2):
            # # perform conditional crossover
            if cross_choices[i//2]:
                # get the crossover point
                cp = cross_points[i//2]
                # retrieve indexes into parent bitstrings
                p1, p2 = parents[i], parents[i+1]
                # copy bits from parents into child 1
                bitstrings_children[i,cp:] = bitstrings_pop[p2,cp:]
                # copy bits from parents into child 2
                bitstrings_children[i+1,cp:] = bitstrings_pop[p1,cp:]
        # determine mutations for all bits in new population
        mut_choices = rng.random(None, numpy.float32, mut_rands) <= m_rate
        # apply mutations
        bitstrings_children[mut_choices] = 1 - bitstrings_children[mut_choices]
        # swap parents and children populations
        bitstrings_pop, bitstrings_children = bitstrings_children, bitstrings_pop
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
