import copy
import random

from tools.population_creator import (ImpossibleToCompleteError, Individual,
                                      create_individual, is_chromosome_valid)


def generate_child_template(parent1: list, parent2: list, center: int) -> list:
    """
    :param parent1: хромосома первого родителя
    :param parent2: хромосома второго родителя
    :param center: центр хромосом (индекс)
    :return: шаблон дочерней особи

    Данная функция служит для формирования шаблонов дочерних особей, в которых
    не возникает конфликта топологии двоичного дерева.

    Основным механизмом скрещивания является преемственность, то есть
    потомки получают не измененные участки хромосомы родителей.

    В данном случае потомок получает подходящие гены из
    первой половины хромосомы первого родителя. Вторая половина дочерней
    хромосомы формируется из подходящих генов из второй половины хромосомы
    второго родителя.

    На данной этапе формируется только шаблон в виде списка, но не сам
    экземпляр класса Individual.
    """
    child = [None] * len(parent1)
    first = list(range(center))
    second = list(range(center, len(parent1)))
    random.shuffle(first), random.shuffle(second)
    for i, j in zip(first, second):
        gen_in_parent_1 = parent1[i]
        gen_in_parent_2 = parent2[j]
        for k in range(3):
            temp = copy.copy(child)
            if k == 0:
                temp[i] = gen_in_parent_1
                temp[j] = gen_in_parent_2
                if is_chromosome_valid(temp):
                    child[:] = temp[:]
                    break
            elif k == 1:
                temp[i] = gen_in_parent_1
                if is_chromosome_valid(temp):
                    child[:] = temp[:]
                    break
            else:
                temp[j] = gen_in_parent_2
                if is_chromosome_valid(temp):
                    child[:] = temp[:]
                    break
    return child


def crossover(parent1: Individual, parent2: Individual,
              center: int) -> tuple:
    """

    :param parent1: первый родитель
    :param parent2: второй родитель
    :param center: середина хромосомы (индекс)
    :return: Возвращает две дочерние особи - экземпляры Individual

    Сначала генерируем допустимый шаблон дочерних особей, после, используем
    population_creator.create_individual, передавая в эту функцию шаблон
    дочерней особи. В итоге получается особь, сгенерированная по тем же
    правилам, что и особи из изначальной популяци.


    Если не удалось сгенерировать полную хромосому по шаблону, то дочерней
    особью в этом случае будет являться первый родитель.
    """
    n: int = len(parent1) + 1
    child_1_template: list = generate_child_template(parent1, parent2, center)
    child_2_template: list = generate_child_template(parent2, parent1, center)
    try:
        child_1 = create_individual(n, template=child_1_template)
    except ImpossibleToCompleteError:
        child_1 = None
    try:
        child_2 = create_individual(n, template=child_2_template)
    except ImpossibleToCompleteError:
        child_2 = None
    return child_1, child_2
