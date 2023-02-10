class Node:
    def __init__(self, 
                    pos: tuple[int, int], 
                    prev: 'Node', 
                    f: int = 0):
        self.pos = pos
        self.prev = prev
        self.f = f

    def __eq__(self, other: 'Node') -> (bool):
        return self.pos == other.pos

    def __ne__(self, other: 'Node') -> (bool):
        return self.pos != other.pos

    def __lt__(self, other: 'Node') -> (bool):
        return self.f < other.f

    def __gt__(self, other: 'Node') -> (bool):
        return self.f > other.f

    def __getitem__(self, key: int) -> (int):
        return self.pos[key]

    def __str__(self) -> (str):
        return 'Node({})'.format(self.pos)

    def path(self, 
            start_node: 'Node') -> (list[tuple[int, int]]):
        path = []
        node = self.prev
        if node is None:
            return path
        while node != start_node:
            path.append(node.pos)
            node = node.prev
        path.reverse()
        #print('start_node: {}, end_node: {}'.format(start_node.pos, self.pos))
        #print('path: {}'.format(path))
        return path