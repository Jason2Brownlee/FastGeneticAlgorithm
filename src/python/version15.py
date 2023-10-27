# simple genetic algorithm in python
# version 15
# jason brownlee
from numpy import zeros
from numpy import arange
from numpy import argmax
from numpy import ubyte
from numpy import float32
from numpy import ushort
from numpy import uintc
from numpy import logical_xor
from numpy import copyto
from numpy import newaxis
from numpy.random import default_rng
from gc import disable

# run the genetic algorithm and return the best result
def genetic_algorithm(r_seed, n_strings, length, n_epochs, n_rounds, m_rate, c_rate):
    # keep track of the best result
    best_fitness, best_string = -1.0, zeros(length, ubyte)
    # seed the random number generator
    rng = default_rng(r_seed)
    # initialize the first population of bitstring
    bitstrings_pop = rng.integers(0, 1, (n_strings, length), ubyte, True)
    # preallocate memory for the children we will create
    bitstrings_children = zeros((n_strings, length), ubyte)
    # empty array for all fitness scores
    fitness_pop = zeros(n_strings, ushort)
    # preallocate arrays for random choices
    cross_rands = zeros(n_strings//2, float32)
    mut_rands = zeros((n_strings, length), float32)
    aranged = arange(n_strings)
    aranged2 = arange(length)
    # indexes of selected parents
    parents = zeros(n_strings, ushort)
    # run the algorithm
    for epoch in range(n_epochs):
        # calculate fitness for current population (onemax)
        bitstrings_pop.sum(1, ushort, fitness_pop)
        # locate the candidate with the best fitness
        best_ix = argmax(fitness_pop)
        # check for new best
        if fitness_pop[best_ix] > best_fitness:
            # store the best fitness score and bit string
            best_fitness, best_string = fitness_pop[best_ix], bitstrings_pop[best_ix, :]
        # report best
        print(f'>{epoch} fitness={best_fitness}')
        # generate random indexes for the tournaments for each string
        torn_ixs = rng.integers(0, n_strings, (n_strings, n_rounds), ushort)
        # find the index of the maximum fitness in each tournament
        tournament_winners = argmax(fitness_pop[torn_ixs], axis=1)
        # update the parents with the winners' indexes
        parents[:] = torn_ixs[aranged, tournament_winners]
        # choose which pairs will participate in crossover
        cross_choices = rng.random(None, float32, cross_rands) <= c_rate
        # choose crossover points
        cross_points = rng.integers(1, length-1, n_strings//2, uintc)
        # define the crossover mask
        crossover_masks = aranged2 >= cross_points[:, newaxis]
        # update the mask to not crossover parents not participating in crossover
        crossover_masks[~cross_choices, :] = False
        # copy all selected parent bits to children
        copyto(bitstrings_children, bitstrings_pop[parents,:])
        # copy odd parent bits into even children
        copyto(bitstrings_children[::2], bitstrings_pop[parents,:][1::2], where=crossover_masks)
        # copy event parent bits into odd children
        copyto(bitstrings_children[1::2], bitstrings_pop[parents,:][::2], where=crossover_masks)
        # determine mutations for all bits in new population
        mutation_mask = rng.random(None, float32, mut_rands) <= m_rate
        # apply mutations
        logical_xor(bitstrings_children, 1, bitstrings_children, where=mutation_mask)
        # swap parents and children populations
        bitstrings_pop, bitstrings_children = bitstrings_children, bitstrings_pop
    # return best candidate discovered
    return {'fitness':best_fitness, 'bitstring':best_string}

# protect the entry point
if __name__ == '__main__':
    # disable garbage collection
    disable()
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
