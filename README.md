# Fast Genetic Algorithm in Python

Exploring how to develop a fast genetic algorithm implementation in Python.

## About

I really love genetic algorithms, always have.

When I start using a new programming language, I typically develop a genetic algorithm to prove that I understand the language well enough.

Optimization algorithms have to be fast and I had a thought:

> Can I get Python genetic algorithm to run about as fast as C?

This project explores how we might develop an implementation of the "simple genetic algorithm" in Python that is about as fast as an implementation in ANSI C. It's probably not possible but it is interesting to see how close can we get.

I explored this question years ago, I've just decided to make it public (someone asked me about it). I've since added some more versions and pushed the time closer to parity.


## Results

A naive port from C to Python is about 10x slower, work is required to get the execution time back down again to something sane. I expect numpy masters and code-golfers could cut more milliseconds and lines (if so, let me know).


Version                                | Time (sec) | Speedup (c) | Speedup (v01)
---------------------------------------|------------|--------------|-------------
[ANSI C](src/c/simple_ga.c)            | 0.539      | n/a          | n/a
[Version 01](src/python/version01.py)  | 4.874      | 0.111x       | n/a
[Version 02](src/python/version02.py)  | 3.339      | 0.161x       | 1.460x
[Version 03](src/python/version03.py)  | 20.590     | 0.026x       | 0.237x
[Version 04](src/python/version04.py)  | 1.211      | 0.445x       | 4.025x
[Version 05](src/python/version05.py)  | 0.787      | 0.685x       | 6.193x
[Version 06](src/python/version06.py)  | 0.633      | 0.852x       | 7.700x
[Version 07](src/python/version07.py)  | 0.625      | 0.862x       | 7.798x
[Version 08](src/python/version08.py)  | 0.602      | 0.895x       | 8.096x
[Version 09](src/python/version09.py)  | 0.452      | 1.192x       | 10.783x
[Version 10](src/python/version10.py)  | 0.448      | 1.203x       | 10.879x


* Execution time is taken from the best of 3 sequential runs on my workstation.
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
* Does not free memory.
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





### Version 07 (optimizations)

This version further optimizes the NumPy version.

* Preallocate array for selected parents each iteration.
* Removed fitness function, made it inline.
* Simplify crossover, remove redundant copying and return.
* Use positional over named arguments where possible.
* Move crossover and mutation to be inline.

The source code is available here:

* [version07.py](src/python/version07.py)

```default
time python ./version07.py
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

real	0m0.625s
user	0m0.583s
sys	0m0.034s
```


### Version 08 (optimizations)

This version further optimizes the NumPy version.

* Moved tournament selection to be inline.
* Simplified iteration for tournament selection.

The source code is available here:

* [version08.py](src/python/version08.py)

```default
time python ./version08.py
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

real	0m0.602s
user	0m0.563s
sys	0m0.034s
```




### Version 09 (matrix)

This version explores using a matrix to hold all bitstrings in each generation.

* One matrix for current and one for next generation.
* Separate array for fitness scores.
* Vectorized onemax (fitness) and best in population (argmax).
* Population-wide vectorization of mutation.

The source code is available here:

* [version09.py](src/python/version09.py)

```default
time python ./version09.py
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

real	0m0.452s
user	0m0.415s
sys	0m0.031s
```



### Version 10 (optimizations)

This version explores optimizing use of the matrix used to hold all bitstrings.

* Copy all selected parents over child then only copy second parents bits if crossed over.

The source code is available here:

* [version10.py](src/python/version10.py)

```default
time python ./version10.py
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

real	0m0.448s
user	0m0.410s
sys	0m0.032s
```




## Ideas

* Do not re-evaluate if child is a copy of parent and not mutated.
* More vectorization somehow?
* Try not to copy best solution found so far, somehow?
* Benchmark more consistently (repeat 3+ times and take mean execution time).
* Optimize array data types (bitstrings, random numbers), see if speed improvement for small/different types.
* All this preallocating arrays is fun, but makes it hard to read, probably introduces bugs and does not do much for speed, cut it!?
* Precompute all random numbers for all epochs (madness!)
* Use threadpool to prepare the next generation in parallel (numpy calls will release the gil)
* Find a randint function that populates array instead of create+populate (slower).
* Can we create one big mask for crossover and apply it to the entire population matrices? Surely!

I have genetic algorithm implementations in a bunch of other languages on disk, I may add them to this project if there's interest.

Do you have more ideas?
Do you see a bug?
Let's chat!

Email me: Jason.Brownlee05@gmail.com

