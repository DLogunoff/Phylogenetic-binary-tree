from numpy import arange, random
from numpy.ma import masked_array as m_arr
from numpy.ma import masked_values


class ImpossibleToCompleteError(ValueError):
    pass


class Fitness:
    def __init__(self):
        self.values = [0]


class Individual(list):
    def __init__(self, *args):
        super().__init__(*args)
        self.fitness = Fitness()


def get_exclude(node1: int, node2: int) -> tuple:
    """
    :param node1: первая вершина в гене
    :param node2: вторая вершина в гене
    :return Возвращает кортеж вершин. Первая вершина подлежит
    исключению(наибольшая), а вторая (наименьшая) становится именем
    комплексной вершины
    """
    return (node1, node2) if node1 > node2 else (node2, node1)


def get_order_of_nodes(node1: int, node2: int, complex_nodes: list) -> tuple:
    """

    :param node1: первая вершина в гене
    :param node2: вторая вершина в гене
    :param complex_nodes: список комплексных вершин
    :return: возвращает кортеж из двух вершин

    Стоит помнить, что комплексная вершина получает имя по минимальной из
    вершин, входящих в неё.
    Выходной кортеж формируется по следующему правилу:

        На первом месте всегда находится меньшая по номеру вершина.

    Из этого также следует, что в каждой хромосоме последний ген будет
    выглядеть (0, ... ).
    """
    if node2 in complex_nodes and node1 not in complex_nodes:
        return node2, node1
    elif node1 in complex_nodes and node2 in complex_nodes:
        if node2 < node1:
            return node2, node1
    return node1, node2


def is_chromosome_valid(chromosome: list) -> bool:
    """

    :param chromosome: хромосома (или её шаблон)
    :return: True/False для верной/нарушенной топологии хромосомы
    """
    for i, gen in enumerate(chromosome):
        for j in chromosome[:i:-1]:
            if gen and j and gen[1] in j:
                return False
    return True


def get_nodes(first_place: m_arr, second_place: m_arr) -> tuple:
    """

    :param first_place: массив, который содержит все доступные значения для первой позиции в гене
    :param second_place: массив, который содержит все доступные значения для второй позиции в гене
    :return: случайно сгенерированный ген
    """
    node_1: int = random.choice(first_place.compressed(), size=1)[0]
    node_2: int = random.choice(second_place.compressed(), size=1)[0]
    return node_1, node_2


def individual_create(n: int, template: list = None) -> Individual:
    """
    :param n: Количество вершин бинарного дерева
    :param template: шаблон дочерней особи
    :return: экземпляр класса Individual (особь)

    Хромосома имеет n - 1 генов, где n - число вершин бинарного дерева
    (или же для данной задачи это количество особей).

    Каждый ген имеет вид двуместного массива вершин, причём вершины
    располагаются в генах по следующим правилам:
        1. Занять первую позицию в гене может только та вершина, которая
        никогда до этого не была на второй позиции;

        2. Занять вторую позицию в гене может только та вершина, которая
        никогда до этого также не была на второй позиции;

        3. Вершины на первой и второй позиции в гене не могут быть одинаковыми.

    Для соблюдения этих правил были созданы 2 массива:
        1. first_place - это массив вершин, которые могут находиться на первой
        позиции в каждом гене;

        2. second_place - это массив вершин, которые могут находиться на второй
        позиции в каждом гене;

    Каждый ген образует собой вершину бинарного дерева. Эта вершина получает
    имя по минимальному элементу ветвей.

    В цикле происходит формирование генов следующим образом:
        1. На первую позицию в гене случайным образом из массива
         first_place выбирается вершина (node_1);

        2. На вторую позицию в гене случайным образом из массива
        second_place выбирается вершина (node_2);

        3. Если node_1 >= node_2, то пункты 1 и 2 повторяются снова;

        5. Ген добавляется в хромосому.


    Данная функция также используется для построения допустимых дочерних
    особей. Для этого нужно в аргумент функции передать необязательный
    параметр template.
    """
    complex_nodes: list = []
    first_place: m_arr = m_arr(arange(n))
    second_place: m_arr = m_arr(arange(n))
    check = False
    cycle = 0
    if template:
        check = True
        for i, gen in enumerate(template):
            if gen:
                second_place = masked_values(second_place, gen[1])
    else:
        template = [None] * (n - 1)
    for i, gen in enumerate(template):
        if gen is None:
            correct = False
            while not correct:
                cycle += 1
                node_1, node_2 = get_nodes(first_place, second_place)
                while node_1 >= node_2:
                    node_1, node_2 = get_nodes(first_place, second_place)
                temp: list = template
                temp[i] = (node_1, node_2)
                correct = is_chromosome_valid(template)
                if cycle >= 100:
                    break
            if cycle >= 100:
                break
            complex_nodes.append(node_1)
            first_place = masked_values(first_place, node_2)
            second_place = masked_values(second_place, node_2)
        else:
            complex_nodes.append(gen[0])
            first_place = masked_values(first_place, gen[1])
    if cycle >= 100:
        raise ImpossibleToCompleteError
    if check:
        return template
    return Individual(template)


def create_population(individual_size: int, population_size: int) -> list:
    """

    :param individual_size: количество вершин двоичного дерева
    :param population_size: размер популяции
    :return: Возвращает сформированную популяцию (в списке)
    """
    return list(
        individual_create(individual_size) for _ in range(population_size)
    )
