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


def create_individual(n: int, template: list = None) -> Individual:
    """
    :param n: Количество вершин бинарного дерева
    :param template: шаблон дочерней особи
    :return: экземпляр класса Individual (особь)

    Хромосома имеет n - 1 генов, где n - число вершин бинарного дерева
    (или же для данной задачи это количество особей).

    Каждый ген имеет вид двухместного массива вершин, причём вершины
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
    first_place: m_arr = m_arr(arange(n))
    second_place: m_arr = m_arr(arange(n))
    cycle = 0
    if template:
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
                correct = is_chromosome_valid(temp)
                if cycle == 100:
                    raise ImpossibleToCompleteError
            first_place = masked_values(first_place, node_2)
            second_place = masked_values(second_place, node_2)
        else:
            first_place = masked_values(first_place, gen[1])
    return Individual(template)


def create_population(individual_size: int, population_size: int) -> list:
    """

    :param individual_size: количество вершин двоичного дерева
    :param population_size: размер популяции
    :return: Возвращает сформированную популяцию (в списке)
    """
    return [create_individual(individual_size) for _ in range(population_size)]
