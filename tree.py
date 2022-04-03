import matplotlib.pyplot as plt

from tools.draw import draw_tree
from tools.fitness import STANDARD
from tools.main_algorithm import genetic_algorithm

# Костанта задачи
INDIVIDUAL_SIZE = len(STANDARD)  # Количетсво генов в хромосове особи

# Константы генетического алгоритма
POPULATION_SIZE = 100  # Количество особей в популяции
MAX_GENERATIONS = 5000  # Максимальное число поколений

best_individual, min_values, mean_values = genetic_algorithm(
    speciman_size=INDIVIDUAL_SIZE,
    population_size=POPULATION_SIZE,
    max_generations=MAX_GENERATIONS,
)

# draw_tree(best_individual)
# plt.plot(min_values, color='red')
# plt.plot(mean_values, color='blue')
# plt.xlabel('Поколение')
# plt.ylabel('Мин/средняя приспособленность')
# plt.title(
#     'Зависимость минимальной и средней приспособленности от поколения')
# plt.show()
