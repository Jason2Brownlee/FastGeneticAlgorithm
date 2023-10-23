# Fast Genetic Algorithm in Python

Exploring how to develop a fast genetic algorithm implementation in Python.

## About

I really love genetic algorithms, always have.

When I start using a new programming language, I typically develop a genetic algorithm to prove that I understand the language well enough.

Optimization algorithms have to be fast and I had a thought:

> Can I get Python genetic algorithm to run about as fast as C?

This project explores how we might develop an implementation of the "simple genetic algorithm" in Python that is about as fast as an implementation in ANSI C. It's probably not possible but it is interesting to see how close can we get.

I did this years ago, I've just decided to make it public (someone asked me about it).


## Results

Version     | Time (sec) | Speedup (c) | Speedup (v01)
------------|------------|--------------|------------
ANSI C      | 0.539      | n/a          | n/a
Version 01  | 4.874      | 0.111x       | n/a
Version 02  | 3.339      | 0.161x       | 1.460x
Version 03  | 20.590     | 0.026x       | 0.237x
Version 04  | 1.211      | 0.445x       | 4.025x
Version 05  | 0.787      | 0.685x       | 6.193x
Version 06  | 0.633      | 0.852x       | 7.700x


* Speedup (c) is the speedup factor of the python version over the ANSI-C version.
* Speedup (v01) is the speedup factor of the Python version over version 01 Python version.
* A speedup factor below 1 means the implementation is slower, above means it's faster.


## Simple Genetic Algorithm

We will define the "simple genetic algorithm" as follows:

* Uses a binary string or "bitstring" representation.
* Uses tournament selection.
* Uses one-point crossover.
* Uses point mutation.
* Solves the one max (sum of bits) problem.
* No early stopping as we pretend we don't know the solution.

All implementations use the same configuration for direct comparison:

* 1 random seed.
* 1,000 bits in each string.
* 100 sized population.
* 3 round tournament selection.
* 500 epochs.
* 1/n mutation probability.
* 95% crossover.

Each implementation should solve the problem before the maximum number of epochs. If not, a bug may have been introduced.


## ANSI C Implementation

The reference implementation is provided in C.

We are tying to develop a Python version that is about as fast as the C version.

My ANSI C is a little rusty so the implementation is naive (at best) and not highly optimized.

* Uses a struct for each candidate solution to track bits, length, and fitness.
* Mallocs each candidate on demand and candidates are not reused.
* Lots of for-loop iteration
* No fancy memory tricks or bitshifts.
* Reports best result each epoch on stdout.

That being said, if you want to develop an optimized version of this implementation, I'd love to see it.

You can review the code here:

* [simple_ga.c](src/c/simple_ga.c)

It can be compiled as follows:


```default
gcc simple_ga.c -Wall -o simple_ga
```

It can be benchmarked as follows:

```default
time ./simple_ga
```

A sample of results is provided below. This is the target for the Python version.

```default
...
>495, fitness=1000
>496, fitness=1000
>497, fitness=1000
>498, fitness=1000
>499, fitness=1000
Done!

real    0m0.539s
user    0m0.489s
sys     0m0.046s
```



## Python Implementations

Developing a Python implementation is incremental.

### Version 01 (port)

This is a port of the C version to the Python standard library with no optimization.

* Uses an integer representation for bitstrings
* Uses a dict structure for each candidate solution.

The source code is available here:

* [version01.py](src/python/version01.py)


```default
time python ./version01.py
```

A sample of results is provided below.

```default
...
>495 fitness=1000
>496 fitness=1000
>497 fitness=1000
>498 fitness=1000
>499 fitness=1000
Done

real	0m4.874s
user	0m4.785s
sys	0m0.034s
```



### Version 02 (simplified)

This version seeks to simplify the Python version.

* It uses fewer functions.
* It uses multiple assignment.

The source code is available here:

* [version02.py](src/python/version02.py)


```default
time python ./version02.py
```

A sample of results is provided below.

```default
...
>495 fitness=1000
>496 fitness=1000
>497 fitness=1000
>498 fitness=1000
>499 fitness=1000
Done

real	0m3.339s
user	0m3.285s
sys	0m0.026s
```

### Version 03 (naive numpy)

This version ports the Python version to use the NumPy API.

* Use numpy arrays for bitstrings.
* Use functions on numpy arrays, e.g. sum().
* Uses numpy random functions.

The source code is available here:

* [version03.py](src/python/version03.py)

```default
time python ./version03.py
```

A sample of results is provided below.

```default
...
>495 fitness=1000
>496 fitness=1000
>497 fitness=1000
>498 fitness=1000
>499 fitness=1000
Done

real	0m20.590s
user	0m19.569s
sys	0m0.273s
```


### Version 04 (optimized)

This version optimizes the NumPy version.

* Vectorized version of point mutation operation.
* Deleted bitstring copy function moved into crossover.
* Simplified slice in crossover.

The source code is available here:

* [version04.py](src/python/version04.py)

```default
time python ./version04.py
```

A sample of results is provided below.

```default
...
>495 fitness=1000
>496 fitness=1000
>497 fitness=1000
>498 fitness=1000
>499 fitness=1000
Done

real	0m1.211s
user	0m1.162s
sys	0m0.037s
```




### Version 05 (vectorized)

This version further optimizes the NumPy version.

* Populations are arrays of dicts.
* Preallocate parent and child memory and reuse each iteration.
* Specify bitstring array data type as int64 (seems fastest in testing).
* Vectorized tournament selection for entire population.
* Vectorized crossover point selection for entire population.

The source code is available here:

* [version05.py](src/python/version05.py)

```default
time python ./version05.py
```

A sample of results is provided below.

```default
...
>495 fitness=1000
>496 fitness=1000
>497 fitness=1000
>498 fitness=1000
>499 fitness=1000
Done

real	0m0.787s
user	0m0.744s
sys	0m0.035s
```



### Version 06 (optimizations)

This version further optimizes the NumPy version.

* Vectorized choice to crossover or not.
* Vectorized choice to mutate all bits per generation.
* Preallocate arrays for random choices.
* Use float32 for probabilistic decisions (crossover and mutate)

The source code is available here:

* [version06.py](src/python/version06.py)

```default
time python ./version06.py
```

A sample of results is provided below.

```default
...
>495 fitness=1000
>496 fitness=1000
>497 fitness=1000
>498 fitness=1000
>499 fitness=1000
Done

real	0m0.633s
user	0m0.592s
sys	0m0.033s
```




## Ideas

* Early stopping once solution found.
* Do not re-evaluate if child is a copy of parent and not mutated.
* Remove all custom functions and do everything in one large function.
* More vectorization somehow?
* Try not to copy best solution found so far, somehow?
* Benchmark more consistently (repeat 3+ times and take mean execution time).
* Optimize array data types (bitstrings, random numbers), see if speed improvement for small/different types.
* Can we represent the population of bitstrings as a matrix and is it faster?


I have genetic algorithm implementations in a bunch of other languages on disk, I may add them to this project if there's interest.

Do you have more ideas?
Do you see a bug?
Let's chat!

Email me: Jason.Brownlee05@gmail.com

