import random


def select_tournament(population: list, p_len: int) -> list:
    """

    :param population: массив популяции
    :param p_len: размер популяции
    :return: Возвращает отобранную популяцию

    Функция проводит турнирный отбор.

    Алгоритм турнирного отбора:

        1. Выбираются три разные особи случайным образом;

        2. Из этих трёх особей проходит отбор только та, которая имеет
        минимальную функцию приспособленности;

        3. Отбор производится до тех пор, пока размер отобранной популяции
        не будет равен размеру изначальной популяции.

    Алгоритм турнирного отбора позволяет сохранить разнообразие популяции,
    предоставляя шанс не самым приспособленным особям пройти отбор.

    """
    offspring = []
    for i in range(p_len):
        i1 = i2 = i3 = 0
        while i1 == i2 or i1 == i3 or i2 == i3:
            i1, i2, i3 = (random.randint(0, p_len-1),
                          random.randint(0, p_len-1),
                          random.randint(0, p_len-1)
                          )
        offspring.append(min([population[i1], population[i2], population[i3]],
                             key=lambda ind: ind.fitness.values)
                         )
    return offspring
