import matplotlib.pyplot as plt

from tools.main_algorithm import genetic_algorithm

# Костанта задачи
INDIVIDUAL_SIZE = 25  # Количетсво генов в хромосове особи

# Константы генетического алгоритма
POPULATION_SIZE = 1000  # Количество особей в популяции
P_MUTATION = 0.1  # Вероятность мутации
P_CROSSOVER = 0.9  # Вероятность скрещивания
MAX_GENERATIONS = 100  # Максимальное число поколений


best_individual, min_values, mean_values = genetic_algorithm(
    speciman_size=INDIVIDUAL_SIZE,
    population_size=POPULATION_SIZE,
    max_generations=MAX_GENERATIONS,
    p_crossover=P_CROSSOVER,
    p_mutation=P_MUTATION,
)

plt.plot(min_values, color='red')
plt.plot(mean_values, color='blue')
plt.xlabel('Поколение')
plt.ylabel('Мин/средняя приспособленность')
plt.title(
    'Зависимость минимальной и средней приспособленности от поколения')
plt.show()
