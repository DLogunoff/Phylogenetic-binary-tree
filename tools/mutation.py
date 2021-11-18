from random import randint

from tools.population_creator import (ImpossibleToCompleteError, Individual,
                                      individual_create)


def mutation(individual: Individual) -> None:
    """

    :param individual: особь
    :return: возвращает мутировавшую особь

    Для мутации хромосомы сначала с помощью генератора случайных чисел
    выбирается количество генов, которые
    не будут подвержены мутации (от 1 до половины длины хромосомы).

    После выбираются сами гены, которые не будут подтвержены мутации.

    На основании полученных в прошлом шаге номеров генов, формируется
    шаблон хромосомы и функцией individual_create достраивается до
    полной хромосомы.
    """
    length: int = len(individual)
    template: list = [None] * length
    no_change_amount = range(randint(1, length // 2))
    no_change_index = sorted(
        [randint(0, length - 1) for _ in no_change_amount]
    )
    for i in no_change_index:
        template[i] = individual[i]
    try:
        mutant = individual_create(length + 1, template=template)
    except ImpossibleToCompleteError:
        mutant = individual
    individual[:] = mutant[:]
