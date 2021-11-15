import matplotlib.pyplot as plt

from tools.main_algorithm import genetic_algorithm

# Костанта задачи
INDIVIDUAL_SIZE = 5  # Количетсво генов в хромосове особи

# Константы генетического алгоритма
POPULATION_SIZE = 100  # Количество особей в популяции
P_MUTATION = 10.0 / POPULATION_SIZE  # Вероятность мутации
P_CROSSOVER = 1.0 - P_MUTATION  # Вероятность скрещивания
MAX_GENERATIONS = 100  # Максимальное число поколений
EPS = 0.000001  # Точность определения функции приспособленности


best_individual, min_values, mean_values = genetic_algorithm(
        speciman_size=INDIVIDUAL_SIZE,
        population_size=POPULATION_SIZE,
        max_generations=MAX_GENERATIONS,
        p_crossover=P_CROSSOVER,
        p_mutation=P_MUTATION,
        eps=EPS
)


plt.plot(min_values, color='red')
plt.plot(mean_values, color='blue')
plt.xlabel('Поколение')
plt.ylabel('Мин/средняя приспособленность')
plt.title('Зависимость минимальной и средней приспособленности от поколения')
plt.show()
