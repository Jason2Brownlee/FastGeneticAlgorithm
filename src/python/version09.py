# simple genetic algorithm in python
# version 09
# jason brownlee
import numpy

# run the genetic algorithm and return the best result
def genetic_algorithm(r_seed, n_strings, length, n_epochs, n_rounds, m_rate, c_rate):
    # keep track of the best result
    best_fitness = best_string = -1.0
    # seed the random number generator
    rng = numpy.random.default_rng(r_seed)
    # initialize population
    bitstrings_pop = rng.integers(0, 1, (n_strings, length), numpy.int64, True)
    bitstrings_children = numpy.empty((n_strings, length), numpy.int64)
    fitness_pop = numpy.zeros(n_strings, numpy.int64)
    # preallocate arrays for random choices
    cross_rands = numpy.zeros(int(n_strings/2), numpy.float32)
    mut_rands = numpy.zeros((n_strings, length), numpy.float32)
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
            best_fitness, best_string = fitness_pop[best_ix], bitstrings_pop[best_ix, :].copy()
        # report best
        print(f'>{epoch} fitness={best_fitness}')
        # select all draws from the population
        torn_ixs = rng.integers(0, n_strings-1, n_rounds*n_strings, numpy.int64, True)
        # enumerate draws and select best fitness from each set of rounds
        for i in range(n_strings):
            # select the indexes for this round
            indexes = torn_ixs[i*n_rounds:i*n_rounds+n_rounds]
            # find the candidate with the best fitness in this round
            parents[i] = max(indexes, key=lambda d: fitness_pop[d])
        # predetermine all crossover choices, one for each pair
        cross_choices = rng.random(None, numpy.float32, cross_rands) <= c_rate
        cross_points = rng.integers(1, length-2, int(n_strings/2), numpy.int64, True)
        # perform one-point crossover
        for i in range(0, n_strings, 2):
            # retrieve indexes into parent bitstrings
            p1, p2 = parents[i], parents[i+1]
            # # perform conditional crossover
            if cross_choices[int(i/2)]:
                # get the crossover point
                cp = cross_points[int(i/2)]
                # copy bits from parents into child 1
                bitstrings_children[i,:cp] = bitstrings_pop[p1,:cp]
                bitstrings_children[i,cp:] = bitstrings_pop[p2,cp:]
                # copy bits from parents into child 2
                bitstrings_children[i+1,:cp] = bitstrings_pop[p2,:cp]
                bitstrings_children[i+1,cp:] = bitstrings_pop[p1,cp:]
            else:
                # copy data from parents into children
                numpy.copyto(bitstrings_children[i,:], bitstrings_pop[p1,:])
                numpy.copyto(bitstrings_children[i+1,:], bitstrings_pop[p2,:])
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
