# DifEv
This is a simple implementation of [differential evolution](https://en.wikipedia.org/wiki/Differential_evolution) algorithm. It's written in python without use of any external libraries.

## Installation
You can either download this repo, or use pip to install it with this command:
```
pip3 install git+https://github.com/Ivruix/DifEv
```

## Usage
First, you need to import `Population` class from `difev`.
```python
from difev import Population
```
Then, you need to specify fitness function.
```python
def fitness_function(a):                         # should take list as an argument
    return 100 - sum([abs(e) for e in a])        # simple fitness function
```
Next, you need to initialise new population with these parameters (you can read more about them at Wikipedia page about [differential evolution](https://en.wikipedia.org/wiki/Differential_evolution) algorithm):
```python
num_of_vectors = 4                               # number of vectors in population, must be >= 4  
num_of_parameters = 3                            # dimensionality of problem, must be >= 1
bounds = [[-100, 100], [-100, 100], [-100, 100]] # bounds of each value, consists of pairs [min_value, max_value]
differential_weight = 0.6                        # value should be in range [0,2]
crossover_probability = 0.8                      # value should be in range [0,1]

p = Population(num_of_vectors, num_of_parameters, bounds, differential_weight, 
               crossover_probability, fitness_function)
```
After that, start optimisation process. It ends if fitness function reaches it's target value, or algorithm reaches it's maximum iteration.
```python
max_iteration = 100
target_fitness = 100
print(p.train(max_iteration, target_fitness))    # at the end of training returns best solution
```
After training is done, you should see something like this:
```python
Generation: 0
Max fitness: 65.77771
Mean fitness -34.66543

Generation: 25
Max fitness: 99.13482
Mean fitness 94.9277

Generation: 50
Max fitness: 99.55339
Mean fitness 99.34972

Generation: 75
Max fitness: 99.96135
Mean fitness 99.95119

[0.00043471808742134854, -0.0007301719104293918, -0.0006206301893956611]
```
