from binarytree import Node


def draw_tree(chromosome: list) -> None:
    """

    :param chromosome: хромосома особи
    :return: возвращает графическую структуру двоичного финологического
    дерева
    """
    root = Node(int(chromosome[-1][0]))
    nodes = {}
    for gen in chromosome[::-1]:
        start = nodes[gen[0]] if gen[0] in nodes.keys() else 0
        for i in reversed(range(start, len(root.values))):
            if root.values[i] == gen[0]:
                root[i].left = Node(int(gen[0]))
                root[i].right = Node(int(gen[1]))
                nodes[int(gen[0])] = i
                nodes[int(gen[1])] = i
                break

    print(root)
