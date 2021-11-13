from fitness import fitness_count
from population_creator import create_population

# Костанта задачи
INDIVIDUAL_SIZE = 5  # Количетсво генов в хромосове особи

# Константы генетического алгоритма
POPULATION_SIZE = 200  # Количество особей в популяции
P_CROSSOVER = 0.9  # Вероятность скрещивания
P_MUTATION = 0.1  # Вероятность мутации
MAX_GENERATIONS = 50  # Максимальное число поколений


population: list = create_population(INDIVIDUAL_SIZE, POPULATION_SIZE)

fitness_values = list(map(fitness_count, population))

for individual, fitness_value in zip(population, fitness_values):
    individual.fitness.values = fitness_value
