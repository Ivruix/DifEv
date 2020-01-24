from random import randint, sample, random, uniform


class Population:
    vectors = []

    def __init__(self, num_of_vectors, num_of_parameters, bounds, differential_weight, crossover_probability,
                 fitness_function, ensure_bounds=True):

        for _ in range(num_of_vectors):
            self.vectors.append(Vector([uniform(bounds[i][0], bounds[i][1]) for i in range(num_of_parameters)]))
        self.fitness = [fitness_function(vector.coordinates) for vector in self.vectors]

        self.bounds = bounds
        self.differential_weight = differential_weight
        self.crossover_probability = crossover_probability
        self.num_of_parameters = num_of_parameters
        self.num_of_vectors = num_of_vectors
        self.fitness_function = fitness_function
        self.ensure_bounds = ensure_bounds
        self.iteration = 0

    def train(self, max_iterations, target_fitness, representation_interval=0, print_best_vector=False):

        for _ in range(max_iterations):
            if representation_interval > 0:
                if self.iteration % representation_interval == 0:
                    self.__default_representation_function(self.iteration, print_best_vector)

            for new_vector in enumerate(self.__next_generation()):
                vector_fitness = self.fitness_function(new_vector[1].coordinates)
                if vector_fitness >= target_fitness:
                    return new_vector[1].coordinates
                if vector_fitness > self.fitness[new_vector[0]]:
                    self.fitness[new_vector[0]] = vector_fitness
                    self.vectors[new_vector[0]] = new_vector[1]

            self.iteration += 1

        return self.vectors[self.fitness.index(max(self.fitness))].coordinates

    def __next_generation(self):

        for i in range(self.num_of_vectors):

            indexes = sample(range(self.num_of_vectors), 3)
            while not (i in indexes):
                indexes = sample(range(self.num_of_vectors), 3)
            new_vector = self.vectors[indexes[0]] + \
                         (self.vectors[indexes[1]] - self.vectors[indexes[2]]) * self.differential_weight
            r = randint(0, self.num_of_parameters)
            new_vector = Vector(
                [e[1] if (random() < self.crossover_probability or e[0] == r) else self.vectors[i].coordinates[e[0]]
                 for e in enumerate(new_vector.coordinates)])
            if self.ensure_bounds:
                new_vector = Vector([self.__ensure_bounds(e) for e in enumerate(new_vector.coordinates)])
            yield new_vector

    def __ensure_bounds(self, e):
        if e[1] < self.bounds[e[0]][0]:
            return self.bounds[e[0]][0]
        elif e[1] > self.bounds[e[0]][1]:
            return self.bounds[e[0]][1]
        else:
            return e[1]

    def __default_representation_function(self, iteration, print_best_vector):
        max_fitness = max(self.fitness)
        best_vector = self.vectors[self.fitness.index(max_fitness)].coordinates
        print("Generation:", iteration)
        print("Max fitness:", round(max_fitness, 5))
        print("Mean fitness:", round(sum(self.fitness) / self.num_of_vectors, 5))
        if print_best_vector:
            print("Best vector:", best_vector)
        print()


class Vector:
    def __init__(self, coordinates):
        self.coordinates = coordinates

    def __add__(self, v):
        return Vector([v.coordinates[i] + self.coordinates[i] for i in range(len(self.coordinates))])

    def __mul__(self, k):
        return Vector([i * k for i in self.coordinates])

    def __sub__(self, v):
        return Vector([self.coordinates[i] - v.coordinates[i] for i in range(len(self.coordinates))])

    def __repr__(self):
        return 'Vector ' + str(tuple(self.coordinates))
