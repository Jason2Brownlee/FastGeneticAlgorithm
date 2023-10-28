# simple genetic algorithm in python
# version 16
# jason brownlee
from numpy import empty
from numpy import arange
from numpy import argmax
from numpy import bool_
from numpy import float32
from numpy import ushort
from numpy import uintc
from numpy import bitwise_xor
from numpy.random import default_rng
from gc import disable

# run the genetic algorithm and return the best result
def genetic_algorithm(r_seed, n_strings, length, n_epochs, n_rounds, m_rate, c_rate):
    # keep track of the best result
    best_fitness, best_string = -1.0, empty(length, bool_)
    # seed the random number generator
    rng = default_rng(r_seed)
    # initialize the first population of bitstring
    bitstrings_parents = rng.integers(0, 1, (n_strings, length), bool_, True)
    # preallocate memory for the children we will create
    bitstrings_children = empty((n_strings, length), bool_)
    # empty array for all fitness scores
    fitness_pop = empty(n_strings, ushort)
    # preallocate arrays for random choices
    cross_rands = empty(n_strings//2, float32)
    mut_rands = empty((n_strings, length), float32)
    arranged = arange(n_strings)
    # pre-choose all crossover points for all epochs
    cross_points = rng.integers(1, length, (n_epochs, n_strings//2), uintc)
    # pre choose all tournament draws for all epochs
    torn_ixs = rng.integers(0, n_strings, (n_epochs, n_strings, n_rounds), ushort)
    # indexes of selected parents
    parents = empty(n_strings, ushort)
    # run the algorithm
    for epoch in range(n_epochs):
        # calculate fitness for current population (onemax)
        bitstrings_parents.sum(1, ushort, fitness_pop)
        # locate the candidate with the best fitness
        best_ix = argmax(fitness_pop)
        # check for new best
        if fitness_pop[best_ix] > best_fitness:
            # store the best fitness score and bit string
            best_fitness, best_string = fitness_pop[best_ix], bitstrings_parents[best_ix, :]
        # report best
        print(f'>{epoch} fitness={best_fitness}')
        # find the index of the maximum fitness in each tournament
        tournament_winners = argmax(fitness_pop[torn_ixs[epoch]], axis=1)
        # update the parents with the winners' indexes
        parents[:] = torn_ixs[epoch, arranged, tournament_winners]
        # generate random floats and choose all pairs to participate in crossover
        cross_choices = rng.random(None, float32, cross_rands) <= c_rate
        # copy all selected parent bits to children
        bitstrings_children[:] = bitstrings_parents[parents,:]
        # perform one-point crossover where needed
        for i in range(0, n_strings, 2):
            # # perform conditional crossover
            if cross_choices[i//2]:
                # get the crossover point
                cp = cross_points[epoch, i//2]
                # copy bits from parents into child 1
                bitstrings_children[i,cp:] = bitstrings_parents[parents[i+1],cp:]
                # copy bits from parents into child 2
                bitstrings_children[i+1,cp:] = bitstrings_parents[parents[i],cp:]
        # determine mutations for all bits in new population
        mutation_mask = rng.random(None, float32, mut_rands) <= m_rate
        # apply mutations
        bitwise_xor(bitstrings_children, True, out=bitstrings_children, where=mutation_mask, dtype=bool_)
        # swap parents and children populations
        bitstrings_parents, bitstrings_children = bitstrings_children, bitstrings_parents
    # return best candidate discovered
    return {'fitness':best_fitness, 'bitstring':best_string}

# protect the entry point
if __name__ == '__main__':
    # disable garbage collection
    disable()
    # configuration
    r_seed = 3
    n_strings = 100
    length = 1000
    n_epochs = 500
    n_rounds = 3
    m_rate = 1.0 / length
    c_rate = 0.95
    # run the genetic algorithm
    best = genetic_algorithm(r_seed, n_strings, length, n_epochs, n_rounds, m_rate, c_rate)
    print('Done')
