import random

from tools.crossover import crossover
from tools.fitness import fitness_count
from tools.mutation import mutation
from tools.population_creator import create_population
from tools.selection import clone


def genetic_algorithm(speciman_size: int, population_size: int,
                      max_generations: int) -> tuple:
    """

    :param speciman_size: количество вершин
    :param population_size: размер популяции
    :param max_generations: максимальное количество поколений
    :return: Возвращает лучшую особь и статистику

    Генетический алгоритм: скрещивание - мутация - отбор.

    Скрещивание - специально разработанный алгоритм для данной задачи.
    Подробнее описан в файле crossover.py

    Мутация - случайно выбираются гены (от 60% до N - 1 числа ген),
    остальные гены стираются и особь формируется на основе оставшихся
    генов.

    """
    population: list = create_population(speciman_size, population_size)
    fitness_values: list = list(map(fitness_count, population))
    for individual, fitness_value in zip(population, fitness_values):
        individual.fitness.values = fitness_value
    center = speciman_size // 2
    min_fitness_values = []
    mean_fitness_values = []
    generation_counter = 0
    while generation_counter < max_generations:
        generation_counter += 1

        random.shuffle(population)
        offspring_copied = list(map(clone, population))
        for parent1, parent2 in zip(
                offspring_copied[::2], offspring_copied[1::2]):
            result = crossover(parent1, parent2, center)
            if result[0] is not None:
                offspring_copied.append(result[0])
            if result[1] is not None:
                offspring_copied.append(result[1])
        for i in range(len(offspring_copied)):
            mutant = mutation(offspring_copied[i])
            if mutant is not None:
                offspring_copied.append(mutant)
        fresh_fitness_values = list(map(fitness_count, offspring_copied))
        for individual, fitness_value in zip(
                offspring_copied, fresh_fitness_values):
            individual.fitness.values = fitness_value
        best_offspring = sorted(
            offspring_copied,
            key=lambda ind: ind.fitness.values
        )[:population_size]
        population = best_offspring[:]

        fitness_values = [ind.fitness.values for ind in population]
        min_fitness = min(fitness_values)
        mean_fitness = sum(fitness_values) / len(population)
        min_fitness_values.append(min_fitness)
        mean_fitness_values.append(mean_fitness)
        best_index = fitness_values.index(min(fitness_values))
    return population[best_index], min_fitness_values, mean_fitness_values
