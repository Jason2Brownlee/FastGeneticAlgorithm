// simple genetic algorithm in ansi c
// jason brownlee
#include <stdio.h>
#include <stdlib.h>

// candidate solution
struct Candidate {
	int* bitstring;
	int length;
	float score;
};

// helper to generate a random float in [0, 1]
float rand_float() {
	return rand() / (float)RAND_MAX;
}

// helper to generate a random bit in {0, 1}
int	rand_bit() {
	if(rand_float() < 0.5) {
		return 0;
	}
	return 1;
}

// helper to generate random integer in [0, max] (inclusive)
int rand_int(int max) {
	return rand() % (max + 1);
}

// create a candidate solution
struct Candidate* create_bitstring(int length) {
	// allocate memory
	struct Candidate* c = malloc(sizeof(struct Candidate));
	// initialize
	c->bitstring = malloc(sizeof(int) * length);
	c->length = length;
	c->score = 0.0;
	return c;
}

// create a candidate with a random bit string
struct Candidate* random_bitstring(int length) {
	// create a candidate
	struct Candidate* c = create_bitstring(length);
	// initialize
	for(int i=0; i<length; i++) {
		c->bitstring[i] = rand_bit();
	}
	return c;
}

// copy a candidate bitstring
struct Candidate* copy_bitstring(struct Candidate* other) {
	// create a candidate
	struct Candidate* c = create_bitstring(other->length);
	// initialize
	for(int i=0; i<other->length; i++) {
		c->bitstring[i] = other->bitstring[i];
	}
	return c;
}

// evaluate the fitness of a string, onemax
float fitness(struct Candidate* bs){
	float score = 0.0;
	for (int i = 0; i < bs->length; i++){
		score += bs->bitstring[i];
	}
	return score;
}

// perform tournament selection (best of n independently random draws)
struct Candidate* tournament_selection(struct Candidate** pop, int n_strings, int n_rounds) {
	// select initial candidate (first round)
	int ix = rand_int(n_strings - 1);
	struct Candidate* selected = pop[ix];
	// perform remaining rounds
	for (int i = 0; i < n_rounds - 1; i++) {
		// make a selection
		ix = rand_int(n_strings - 1);
		// check if better
		if (pop[ix]->score > selected->score) {
			selected = pop[ix];
		}
	}
	return selected;
}

// point mutations of a candidate bit strings
void mutate(struct Candidate* bs, float m_rate) {
	// iterate over all bits
	for (int i = 0; i < bs->length; i++) {
		// conditionally perform point mutations
		if (rand_float() <= m_rate) {
			// flip the bit
			bs->bitstring[i] = 1 - bs->bitstring[i];
		}
	}
}

// perform one point crossover
struct Candidate* one_point_crossover(struct Candidate* p1, struct Candidate* p2, int point) {
	// create a copy of the first parent
	struct Candidate* child = copy_bitstring(p1);
	// iterate from cross point to the end of the string
	for (int i = point; i < p2->length; i++) {
		// copy bits from p2 over copied bits from p1
		child->bitstring[i] = p2->bitstring[i];
	}
	return child;
}

// run the genetic algorithm and return the best result
struct Candidate* genetic_algorithm(int r_seed, int n_strings, int length, int n_epochs, int n_rounds, float m_rate, float c_rate) {
	// keep track of the best solution found so far
	struct Candidate* best = NULL;
	// allocate memory for working set of solutions
	struct Candidate** pop = malloc(sizeof(struct Candidate*) * n_strings);
	// seed random numbers
	srand(r_seed);
	// create initial population
	for (int i = 0; i < n_strings; i++) {
		pop[i] = random_bitstring(length);
	}
	// evolve
	for (int epoch = 0; epoch < n_epochs; epoch++) {
		// evaluate all candidate solitions
		for (int i = 0; i < n_strings; i++) {
			// calculate and assign fitness
			pop[i]->score = fitness(pop[i]);
			// check for new best
			if (best == NULL || pop[i]->score > best->score) {
				best = pop[i];
			}
		}
		// report progress
		printf(">%d, fitness=%.0f\n", epoch, best->score);
		// allocate memory for the selected parents
		struct Candidate** parents = malloc(sizeof(struct Candidate*) * n_strings);
		// select parents for the next generation
		for (int i = 0; i < n_strings; i++) {
			// perform a single round of tournament selection
			parents[i] = tournament_selection(pop, n_strings, n_rounds);
		}
		// allocate memory for the children
		struct Candidate** children = malloc(sizeof(struct Candidate*) * n_strings);
		// create children, 2 at a time, from selected parents
		for (int i = 0; i < n_strings; i+=2) {
			// get parents
			struct Candidate* p1 = parents[i];
			struct Candidate* p2 = parents[i + 1];
			// conditionally perform crossover
			if (rand_float() <= c_rate) {
				// select crossover point
				int point =  1 + rand_int(length - 2);
				// perform one-point crossover
				children[i] = one_point_crossover(p1, p2, point);
				children[i + 1] = one_point_crossover(p2, p1, point);
			} else {
				// copy parents as children
				children[i] = copy_bitstring(p1);
				children[i + 1] = copy_bitstring(p2);
			}
			// perform point mutations
			mutate(children[i], m_rate);
			mutate(children[i + 1], m_rate);
		}
		// children replace parents
		pop = children;
	}
	// return the best solution seen
	return best;
}

// entry point of the program
int main() {
	// define configuration
	int r_seed = 1;
	int n_strings = 100;
	int length = 1000;
	int n_epochs = 500;
	int n_rounds = 3;
	float m_rate = 1.0 / (float)length;
	float c_rate = 0.95;
	struct Candidate* best = NULL;
	// run the process
	best = genetic_algorithm(r_seed, n_strings, length, n_epochs, n_rounds, m_rate, c_rate);
	// summarize result
	printf("Done!\n");
	return 0;
}
