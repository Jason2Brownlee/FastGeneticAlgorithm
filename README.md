# Fast Genetic Algorithm in Python

Exploring how to develop a fast genetic algorithm implementation in Python.

## About

I really love genetic algorithms, always have.

When I start using a new programming language, I topically develop a genetic algorithm to prove that I understand the language well enough.

Optimization algorithms have to be fast and I had a thought: "can I get Python to run about as fast as c?"

This project explores how we might develop an implementation of the "simple genetic algorithm" in Python that is about as fast as an implementation in ANSI C. It's probably not possible but how close can we get?

I did this years ago, just decided to make it public (someone asked me about it).


## Results

Version     | Time (sec) | Speedup (c) | Speedup (v01)
------------|------------|--------------|------------
ANSI C      | 0.539      | n/a          | n/a
Version 01  | 4.874      | 0.111x       | n/a
Version 02  | 3.339      | 0.161x       | 1.460x
Version 03  | 20.590     | 0.026x       | 0.237x
Version 04  | 1.211      | 0.445x       | 4.025x
Version 05  | 0.787      | 0.685x       | 6.193x



## Simple Genetic Algorithm

We will define the "simple genetic algorithm" as follows:

* Uses a binary string or bitstring representation.
* Uses tournament selection.
* Uses one-point crossover.
* Uses point mutation.
* Solves the one max (sum of bits) problem.
* Stops when the best solution is found.

All implementations use the same configuration for direct comparison:

* 1 random seed.
* 1,000 bits in each string.
* 100 sized population.
* 3 round tournament selection.
* 500 epochs, no early stopping.
* 1/n mutation probability.
* 95% crossover.

## ANSI C Implementation

The reference implementation is provided in C.

We are tying to develop a Python version that is about as fast as the C version.

My ANSI C is a little rusty so the implementation is not highly optimized.

* Uses a struct for each candidate solution to track bits, length, and fitness.
* Mallocs each candidate on demand and candidates are not reused.
* Lots of for-loop iteration
* No fancy memory tricks.
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



### Version 02

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

### Version 03

This version ports the Python version to use the NumPy API.

* Use numpy arrays for bitstrings.
* Use functions on numpy arrays, e.g. sum().
* Uses nunpy random functions.

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


### Version 04

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




### Version 05

This version further optimizes the NumPy version.

* Populations are arrays of dicts.
* Preallocate parent and child memory and reuse each iteration.
* Specify bitstring array data type as int64 (seems fastest in testing).
* Vectorized tournament selection for entire population.
* Vectorize crossover point selection for entire population.

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


## Ideas

* Early stopping once solution found.
* Do not re-evaluate if child is a copy of parent and not mutated.
* Reuse arrays used for vectorized random number generation.



