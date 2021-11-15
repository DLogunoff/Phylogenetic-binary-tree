from tools.population_creator import Individual, individual_create


def check_genes(gen1: list, gen2: list, child: list, heads: list,
                backs: list) -> bool:
    """

    :param gen1: ген первого родителя
    :param gen2: ген второго родителя
    :param child: хромосома дочерней особи
    :param heads: список наименований верший комплесных узлов
    :param backs: список вершин, которые не могут находиться на 1 месте в гене
    :return: True/False

    Функция служит для определения пригодности двух генов для скрещивания.

    Гены не должны вызывать конфликта топологии. В каждом гене всегда на первом
    место стоит наименьшая вершина и результирующая комплексная вершина
    получает имя по наименьшей вершине, а та вершина, что была на втором месте,
    выбывает из списка доступных.
    """
    if (gen1[1] == gen2[0]
            or gen1 == gen2
            or gen1[1] == gen2[1]
            or gen1[1] in heads
            or gen2[1] in heads
            or gen1[1] in backs
            or gen2[1] in backs
            or gen2 in child
            or gen1 in child):
        return True
    return False


def generate_child_template(parent1: list, parent2: list, center: int) -> list:
    """
    :param parent1: хромосома первого родителя
    :param parent2: хромосома второго родителя
    :param center: центр хромосом (индекс)
    :return: шаблон дочерней особи

    Данная функция служит для формирования шаблонов дочерних особей, в которых
    не возникает конфликта топологии двоичного дерева.

    Основным механизмом скрещивания является преемственность, то есть
    потомки получают неизмененные участки хромосомы родителей.

    В данном случае потомок получает подходящие гены из
    первой половины хромосомы первого родителя. Вторая половина дочерней
    хромосомы формируется из подходящих генов из второй половины хромосомы
    второго родителя.

    Контроль за отбором неконфликтущих генов лежит на функции check_genes,
    которая использует имеющуюся на каждой итерации хромосому дочерней особи,
    список имён комплексных вершин, список вершин, который находились на
    втором месте в гене.

    Если не удалось получить допустимый шаблон дочерней особи, дочерней особью
    в этом случае будет являться первый родитель.

    На данной этапе формируется только шаблон в виде списка, но не сам
    экземпляр класса Individual.
    """
    child = [None] * len(parent1)
    heads = []
    backs = []
    for i, gen_in_parent_1 in enumerate(parent1[:center]):
        for j, gen_in_parent_2 in reversed(
                list(enumerate(parent2[center:], center))
        ):
            if check_genes(
                    gen_in_parent_1, gen_in_parent_2, child, heads, backs):
                continue
            heads.append(gen_in_parent_1[0])
            heads.append(gen_in_parent_2[0])
            backs.append(gen_in_parent_1[1])
            backs.append(gen_in_parent_2[1])
            child[i] = gen_in_parent_1
            child[j] = gen_in_parent_2

    return child if heads else parent1


def crossover(parent1: Individual, parent2: Individual, center: int) -> tuple:
    """

    :param parent1: первый родитель
    :param parent2: второй родитель
    :param center: середина хромосомы (индекс)
    :return: Возвращает две дочерние особи - экземпляры Individual

    Сначала генерируем допустимый шаблон дочерних особей, после, используем
    population_creator.individual_create, передавая в эту функцию шаблон
    дочерней особи. В итоге получается особь, сгенерированная по тем же
    правилам, что и особи из изначальной популяци.
    """
    n: int = len(parent1) + 1
    child_1_template: list = generate_child_template(parent1, parent2, center)
    child_2_template: list = generate_child_template(parent2, parent1, center)
    child_1: Individual = individual_create(n, template=child_1_template)
    child_2: Individual = individual_create(n, template=child_2_template)

    return child_1, child_2
