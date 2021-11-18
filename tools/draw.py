def draw_tree(chromosome: list) -> None:
    """

    :param chromosome: хромосома особи
    :return: возвращает графическую структуру двоичного финологического
    дерева
    """
    from binarytree import Node
    root = Node(chromosome[-1][0])
    for gen in chromosome[::-1]:
        for i in reversed(range(0, len(root.values))):
            if root.values[i] == gen[0]:
                root[i].left = Node(gen[0])
                root[i].right = Node(gen[1])
                break
    print(root)
