import copy
from math import prod

import numpy as np

STANDARD = [[1, 0.905, 0.887, 0.817, 0.788],
            [0,  1, 0.882, 0.799, 0.775],
            [0, 0, 1, 0.805, 0.775],
            [0, 0, 0, 1, 0.778],
            [0, 0, 0, 0, 1]]


def symmetrify(matrix: list) -> list:
    """

    :param matrix: эталонная таблица мер близости
    :return: возвращает симметричную относительно главной диагонали таблицу
    """
    matrix = np.array(matrix)
    symm = matrix + matrix.T - np.diag(matrix.diagonal())
    return symm


STANDARD = symmetrify(STANDARD)


def check_if_simple(gen: list) -> bool:
    """

    :param gen: ген из последовательности sequence
    :return: является ли данный ген простым

    Ген является простым тогда, когда в него входят только простые вершины.
    """
    return not isinstance(gen[0], list) and not isinstance(gen[1], list)


def get_gen(gen: list) -> list:
    """

    :param gen: ген из последовательности sequence
    :return: возвращает ген, пригодный для использования в цикле for.

    Для более простого использования цикла for в функциях calculate_dividend
    и change_table, ген придотится к виду списка, в котором находятся два
    элемента. Каждый из этих элементов также является списком (даже из
    одного элемента). Если этого не сделать, то for i in gen[0] (или gen[1])
    может выбросить исключение

    TypeError: 'numpy.int32' (int) object is not iterable

    Эта функция позволяет обойтись без двух конструкций try-except.
    """
    final_gen: list = []
    for piece in gen:
        if isinstance(piece, int) or isinstance(piece, np.int32):
            final_gen.append([piece])
        else:
            final_gen.append(piece)
    return final_gen


def calculate_dividend(gen: list) -> float:
    """

    :param gen: ген из последовательности sequence
    :return: возвращает числитель

    Функция проходит циклом по гену из последовательности sequence,
    тем самым получая индексы ячеек эталонной таблицы. Значения этих ячеек
    суммируются, тем самым получая числитель дроби.
    """
    result: float = 0.0
    for i in gen[0]:
        for j in gen[1]:
            result += STANDARD[i][j]
    return result


def change_table(gen: list, placeholder: float, matrix: list) -> list:
    """

    :param gen: ген из последовательности sequence
    :param placeholder: значение, которое нужно внести в таблицу
    :param matrix: таблица
    :return: возвращает изменную таблицу
    """
    for i in gen[0]:
        for j in gen[1]:
            matrix[i][j] = placeholder
            matrix[j][i] = placeholder
    return matrix


def get_flat(gen: list) -> list:
    """

    :param gen: отдельно взятый ген и хромосомы;
    :return: запись гена с раскрытыми скобками.

    Эта функция нужна для того, чтобы в записи последовательности, которую
    формирует функция get_seq, не было вложенных списков.

    Например:
        [(0, 3), (1, 4), (0, 1), (0, 2)] - исходная хромосома.

        Результат без функции get_flat:

        [[0, 3], [1, 4], [[0, 3], [1, 4], [[[0, 3], [1, 4], [0, 3]]

        Результат с функцией get_flat:

        [[0, 3], [1, 4], [[0, 3], [1, 4]], [[0, 3, 1, 4], 2]]

        В результате работы этой функции, в каждой ячейке финальной
        последовательности имеется только 2 элемента, которые, если они списки,
        являются индексами для ячеек исходной таблицы.
    """
    result: list = []
    if np.shape(gen[0]) == np.shape(gen[1]):
        return list(np.reshape(gen, -1))
    for i, piece in enumerate(gen):
        if isinstance(piece, list):
            for node in piece:
                result.append(node)
        else:
            result.append(piece)
    return result if result else gen


def get_seq(individual: list) -> list:
    """
    :param individual: хромосома особи
    :return: последовательность для заполнения таблицы меры близости sequence

    Данная функция формирует список, в котором каждая запись показывает,
    как можно вычислить меру близости для каждого узла бинарного дерева.

    Словарь leaves служит для хранения всех вершин, входящих в вершину.
    Структура словаря: {номер вершины: [простейшие узлы, входящие в вершину]}

    Список sequence служит для формирования ответа. Изначально этот список
    имеет структуру хромосомы, где каждый ген записан в списке, а не в
    кортеже

    Формирование последовательности происходит по следующему алгоритму:
        1. Берём из хромосомы (gen) ген и его порядковый номер (i) в хромосоме;

        2. Из гена берём вершину (node) и её порядковый номер в гене (k);

        3. Если в словаре leaves имеется ключ, соответствующий вершине (node),
        то на место взятой вершины в гене ставится список простейших вершин,
        соответствующих этой комплексной вершине. В противном случае алгоритм
        переходит на шаг 4.

        4. В словарь leaves добавляется последовательность вершин,
        соответствующая вершине (node)
    """
    leaves: dict = {}
    sequence: list = []
    for i, gen in enumerate(individual):
        sequence.append(list(gen))
    for i, gen in enumerate(sequence):
        for k, node in enumerate(gen):
            if node in leaves.keys():
                temp: list = copy.deepcopy(leaves[node])
                sequence[i][k] = get_flat(temp)
            leaves[node] = sequence[i]
    return sequence


def table_for_individual(individual: list) -> list:
    """

    :param individual: хромосома особи
    :return: Возвращает таблицу мер близости этой особи относительно эталонной

    Таблица особи будет формироваться на основании эталонной таблицы и
    последотельности вершин (seq), полученной с помощью функции get_seq.

    В последовательности seq, если в гене присутствуют комплесные вершины,
    значение в первой ячейке гене является строкой таблицы, а значение во
    второй ячейке является столбцом таблицы (хотя можно и наоборот, т.к.
    таблица симметрична относительно главной диагонали).

    Алгоритм составления таблицы:

        1. Проверяется взятый ген из последовательности seq. Если он состоит
        только из простых вершин, то итерация завершена. В противном случае
        переходим на шаг 2;

        2. Необходимо вычислить меру близости для комплексной вершины.
        Для этого необходимо:

            TL;DR: Нужно взять среднее арифметические мер близости одной вершины
            относительно второй (порядок не важен, т.к. таблица симметрична).

            2.1. Необходимо получить сумму мер близости, в соответствии с
            последовательностю seq;

            2.2. Полученную сумму нужно разделить на число слагаемых;

        3. Полученное значение необходимо занести в таблицу в те ячейки,
        которые использовались для вычисления этой меры близости.

    Пример:

    seq = [[1, 3], [2, 4], [0, [2, 4]], [[2, 4, 0], [1, 3]]]
    Первые 2 гена являются простыми генами, поэтому ячейки R[1][3] (R[3][1]) и
    R[2][4] (R[4][2]) не меняются.

    Следующий ген [0, [2, 4]] имеет в себе комплексную вершину. Поэтому, в
    соответствии с пунктом 2:

        2.1. dividend = R[0][2] + R[0][4];

        2.2 result = dividend / 2.

    Занесем полученное значение в таблицу в ячейки R[0][2] (R[2][0]) и
    R[0][4] (R[4][0]).

    Для следуюещего гена [[2, 4, 0], [1, 3]]:

        2.1. dividend = R[2][1] + R[2][3] + R[4][1] + R[4][3] + R[0][1] +
        R[0][3];

        2.2. result = dividend / 6;

        3. Вносим в таблицу значение result в ячейки R[2][1], R[2][3], R[4][1],
        R[4][3], R[0][1], R[0][3] и симметричные им.
    """
    table: list = copy.deepcopy(STANDARD)
    seq: list = get_seq(individual)
    for gen in seq:
        if check_if_simple(gen):
            continue
        modified_gen: list = get_gen(gen)
        dividend: float = calculate_dividend(modified_gen)
        divider: int = prod(
            len(part) for part in gen if isinstance(part, list)
        )
        result: float = dividend / divider
        table: list = change_table(modified_gen, result, table)
    return table


def fitness_count(individual: list) -> float:
    """

    :param individual: экземпляр сущности Individual. Представлен хромосомой.
    :return: Возвращает значение функции приспособленности особи

    Для получения функции приспособленности особи нужно иметь таблицу мер
    близости для данной особи (table).

    Имея таблицу table, нужно поэлементно вычислить среднеквадратичное
    отклонение (quadratic_difference) между эталонной и полученной таблицами.

    Значением функции приспособленности будет сумму всех квадратичных
    отклонений в таблице.
    """
    table: list = table_for_individual(individual)
    quadratic_difference: list = np.power(table - STANDARD, 2)
    return sum(sum(quadratic_difference))
