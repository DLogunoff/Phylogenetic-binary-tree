import random

from tools.crossover import crossover
from tools.fitness import fitness_count
from tools.population_creator import create_population, individual_create
from tools.selection import clone, select_tournament


def genetic_algorithm(speciman_size: int, population_size: int,
                      max_generations: int, p_crossover: float,
                      p_mutation: float, eps: float) -> tuple:
    """

    :param speciman_size: количество вершин
    :param population_size: размер популяции
    :param max_generations: максимальное количество поколений
    :param p_crossover: вероятность скрещивания
    :param p_mutation: вероятность мутации
    :param eps: требуемая точность
    :return: Возвращает лучшую особь и статистику

    Стандартный генетический алгоритм: отбор - скрещивание - мутация.

    Отбор - турнирный отбор (3 особи)

    Скрещивание - специально разработанный алгоритм для данной задачи.
    Подробнее описан в файле crossover.py

    Мутация - особь, подверженная мутации, заново генерирует свою хромосому.

    """
    population: list = create_population(speciman_size, population_size)
    center = speciman_size // 2
    fitness_values: list = list(map(fitness_count, population))
    min_fitness_values = []
    mean_fitness_values = []
    generation_counter = 0
    while (min(fitness_values) > eps
           and generation_counter < max_generations):
        generation_counter += 1

        offspring = select_tournament(population, population_size)
        offspring = list(map(clone, offspring))
        for parent1, parent2 in zip(offspring[::2], offspring[1::2]):
            if random.random() < p_crossover:
                crossover(parent1, parent2, center)
        for i in range(population_size):
            if random.random() < p_mutation:
                offspring[i] = individual_create(speciman_size)
        fresh_fitness_values = list(map(fitness_count, offspring))
        for individual, fitness_value in zip(offspring, fresh_fitness_values):
            individual.fitness.values = fitness_value
        population[:] = offspring

        fitness_values = [ind.fitness.values for ind in population]
        min_fitness = min(fitness_values)
        mean_fitness = sum(fitness_values) / population_size
        min_fitness_values.append(min_fitness)
        mean_fitness_values.append(mean_fitness)
        best_index = fitness_values.index(min(fitness_values))
    return population[best_index], min_fitness_values, mean_fitness_values
