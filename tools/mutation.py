from random import randint

from tools.population_creator import (ImpossibleToCompleteError, Individual,
                                      create_individual)


def mutation(individual: Individual) -> Individual:
    """

    :param individual: особь
    :return: возвращает мутировавшую особь

    Для мутации хромосомы сначала с помощью генератора случайных чисел
    выбирается количество генов, которые не будут подвержены мутации.
    Это значение лежит в интервале от 60% генов до N - 1 ген. То есть,
    как минимум один ген мутирует всегда.

    После выбираются сами гены, которые не будут подтвержены мутации.

    На основании полученных в прошлом шаге номеров генов, формируется
    шаблон хромосомы и функцией create_individual достраивается до
    полной хромосомы.
    """
    length: int = len(individual)
    template: list = [None] * length
    no_change_amount = range(randint(int(length * 0.6), length - 1))
    no_change_index = []
    for _ in no_change_amount:
        while True:
            random_index = randint(0, length - 1)
            if random_index not in no_change_index:
                no_change_index.append(random_index)
                break
    no_change_index.sort()
    for i in no_change_index:
        template[i] = individual[i]
    try:
        mutant = create_individual(length + 1, template=template)
    except ImpossibleToCompleteError:
        mutant = individual
    return mutant
