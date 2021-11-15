from numpy import arange, random
from numpy.ma import masked_array as m_arr
from numpy.ma import masked_values


class Fitness:
    def __init__(self):
        self.values = [0]


class Individual(list):
    def __init__(self, *args):
        super().__init__(*args)
        self.fitness = Fitness()


def extract_template(template: list, n: int) -> tuple:
    """

    :param template: шаблон дочерней особи
    :param n: количество вершин бинарного дерева
    :return: Возвращает извлеченную информацию из имеющихся генов

    Функция используется для извлечения всех необходимых данных из
    частично построенной хромосомы дочерней особи.

    В эти данных входит:

        1. first_place - список допустимых вершин для первой позиции в гене;

        2. second_place - список допустимых вершин для второй позиции в гене;

        3. complex_nodes - список комлексных вершин в хромосоме;

        4. available_places - список свободных генов в хромосоме, т.е. таких
        генов, которые не были унаследованы от родителей.
    """
    available_places: list = []
    complex_nodes: list = []
    first_place: m_arr = m_arr(arange(n))
    second_place: m_arr = m_arr(arange(n))
    for i, gen in enumerate(template):
        if gen:
            exclude, complex_node = get_exclude(gen[0], gen[1])
            complex_nodes.append(complex_node)
            first_place = masked_values(first_place, exclude)
            second_place = masked_values(second_place, exclude)
        else:
            available_places.append(i)
    return first_place, second_place, complex_nodes, available_places


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
        1. На первую позицию в гене случайным образом из массива first_place
        выбирается вершина;

        2. На первую позицию в гене случайным образом из массива second_place
        выбирается вершина;

        3. Если в гене выбраны 2 одинаковые вершины, то вторая вершина
        продолжает случайно выбираться из массива second_place до того момента,
        пока вершины не станут разными;

        4. Определяется имя созданной вершины путём исключения не минимальной
        вершины. То есть определяется максимумальная вершина из двух и она
        исключается из списков доступных вершин;

        5. Ген добавляется в хромосому.


    Данная функция также используется для построения допустимых дочерних
    особей. Для этого нужно в аргумент функции передать необязательный
    параметр template.
    """
    genes: int = n - 1
    if not template:
        first_place: m_arr = m_arr(arange(n))
        second_place: m_arr = m_arr(arange(n))
        available_genes = range(genes)
        chromosome: list = [None] * genes
        complex_nodes: list = []
    else:
        (first_place, second_place,
         complex_nodes, available_genes) = extract_template(template, n)
        chromosome: list = template

    for i in available_genes:
        node_1: int = random.choice(first_place.compressed(), size=1)[0]
        node_2: int = random.choice(second_place.compressed(), size=1)[0]
        while node_2 == node_1:
            node_2 = random.choice(second_place.compressed(), size=1)[0]
        exclude, complex_node = get_exclude(node_1, node_2)
        complex_nodes.append(complex_node)
        node_1, node_2 = get_order_of_nodes(node_1, node_2, complex_nodes)
        first_place = masked_values(first_place, exclude)
        second_place = masked_values(second_place, exclude)
        chromosome[i] = (node_1, node_2)
    return Individual(chromosome)


def create_population(individual_size: int, population_size: int) -> list:
    """

    :param individual_size: количество вершин двоичного дерева
    :param population_size: размер популяции
    :return: Возвращает сформированную популяцию (в списке)
    """
    return list(
        individual_create(individual_size) for _ in range(population_size)
    )
