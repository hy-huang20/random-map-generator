import random
import numpy as np
from utils import *
from node import *

MAP_SIZE = 50
DISTANCE = 20

MAP_BLACK = 0
MAP_WHITE = 1
MAP_RED = 2
MAP_GREEN = 3
MAP_PINK = 4
MAP_YELLOW = 5
MAP_BLUE = 6
MAP_CYAN = 7
MAP_ORANGE = 8
MAP_PURPLE = 9

class RandomMap:
    def __init__(self):
        self.my_map = np.zeros((MAP_SIZE, MAP_SIZE), dtype=np.int32)
        self.open = Queue()
        self.closed = Set()
        self.start_node = Node((0, 0), None)
        self.end_node = Node((0, 0), None)

        self.tmp_map = None
        self.path = []
        self.path_idx = 0

        self.bfs_initialized = False
        self.bfs_open = Queue()
        self.bfs_closed = Set()

        self.dfs_initialized = False
        self.dfs_open = Stack()
        self.dfs_closed = Set()

        self.ids_initialized = False
        self.ids_open = Stack()
        self.ids_closed = Set()
        self.ids_depth = 0

        self.bbfs_initialized = False
        self.bbfs_open_1 = Queue()
        self.bbfs_open_2 = Queue()
        self.bbfs_closed_1 = Set()
        self.bbfs_closed_2 = Set()

        self.bdfs_initialized = False
        self.bdfs_open_1 = Stack()
        self.bdfs_open_2 = Stack()
        self.bdfs_closed_1 = Set()
        self.bdfs_closed_2 = Set()

        self.bids_initialized = False
        self.bids_open_1 = Stack()
        self.bids_open_2 = Stack()
        self.bids_closed_1 = Set()
        self.bids_closed_2 = Set()
        self.bids_depth = 0

        self.ucs_initialized = False
        self.ucs_open = None
        self.ucs_closed = None

        self.gbfs_initialized = False
        self.gbfs_open = None
        self.gbfs_closed = None

        self.a_star_initialized = False
        self.a_star_open = None
        self.a_star_closed = None

        self.b_a_star_initialized = False
        self.b_a_star_open_1 = None
        self.b_a_star_open_2 = None
        self.b_a_star_closed_1 = None
        self.b_a_star_closed_2 = None

        self.id_a_star_initialized = False
        self.id_a_star_open = None
        self.id_a_star_closed = None
        self.id_a_star_depth = 0

    def initialize(self) -> (None):
        # 随机选择一个起始节点
        node = (random.randint(0, MAP_SIZE - 1), random.randint(0, MAP_SIZE - 1))

        self.open.push(node)
        self.closed.add(node)
        self.my_map[node[0]][node[1]] = MAP_WHITE

    def generate(self) -> (bool):
        """
        Generate a random map using BFS
        """
        if self.open.empty():
            return True
        
        node = self.open.pop()
        self.closed.add(node)
        self.my_map[node[0]][node[1]] = MAP_WHITE
        self.update(node)

        return False

    def set_start_and_end_node(self) -> (None):
        while abs(self.start_node.pos[0] - self.end_node.pos[0]) + \
                abs(self.start_node.pos[1] - self.end_node.pos[1]) < DISTANCE:
            closed_length = len(self.closed._items)
            randint1 = random.randint(0, closed_length - 1)
            if randint1 > closed_length // 2:
                randint2 = random.randint(0, randint1 - 1)
            else:
                randint2 = random.randint(randint1 + 1, closed_length - 1)
            count = 0
            for i in range(MAP_SIZE):
                for j in range(MAP_SIZE):
                    if count == randint1:
                        self.start_node = Node((i, j), None)
                    elif count == randint2:
                        self.end_node = Node((i, j), None)
                    count += 1

    def show_start_and_end_node(self) -> (None):
        self.my_map[self.start_node.pos[0]][self.start_node.pos[1]] = MAP_RED
        self.my_map[self.end_node.pos[0]][self.end_node.pos[1]] = MAP_GREEN

    def set_tmp_map(self) -> (None):
        self.start_node.prev = None
        self.start_node.f = 0
        self.end_node.prev = None
        self.end_node.f = 0
        self.tmp_map = np.copy(self.my_map)

    def get_child_nodes(self, 
                        node: tuple[int, int]) -> (list[tuple[int, int]]):
        """
        Get all child nodes of a node
        """
        x, y = node
        child_nodes = []
        if x - 1 >= 0 and x - 1 <= MAP_SIZE - 1:
            child_nodes.append((x - 1, y))
        if x + 1 >= 0 and x + 1 <= MAP_SIZE - 1:
            child_nodes.append((x + 1, y))
        if y - 1 >= 0 and y - 1 <= MAP_SIZE - 1:
            child_nodes.append((x, y - 1))
        if y + 1 >= 0 and y + 1 <= MAP_SIZE - 1:
            child_nodes.append((x, y + 1))
        
        return child_nodes

    def update(self, 
                node: tuple[int, int], 
                random_max: int = 100, 
                low_limit: int = 100, 
                probability: float = 0.5) -> (Queue):
        """
        Update open and closed
        """
        child_nodes = self.get_child_nodes(node)
        random_number = random.randint(0, random_max - 1)
        for child in child_nodes:
            if child not in self.closed:
                # 保证地图生成不会因为生成的随机性而提前结束
                if len(self.open._items) > low_limit:
                    # 随机条件
                    random_condition = random_number < probability * random_max
                    if random_condition:
                        self.open.push(child)
                    else:
                        self.closed.add(child)
                else:
                    self.open.push(child)

    def get_my_map(self) -> (np.ndarray):
        return self.my_map

    def eliminate_big_blanks(self, kernel_size: int = 3) -> (None):
        """
        Eliminate all big blanks in the map
        """
        node_x, node_y = self.find_big_blank(kernel_size)
        while node_x != -1 and node_y != -1:
            node_list = self.locate_big_blank((node_x, node_y))
            self.eliminate_big_blank(node_list)
            node_x, node_y = self.find_big_blank(kernel_size)

    def find_big_blank(self, kernel_size) -> (tuple[int, int]):
        """
        Return a point's position of the first big blank in the map
        """
        node_x, node_y = -1, -1
        for i in range(MAP_SIZE - kernel_size + 1):
            for j in range(MAP_SIZE - kernel_size + 1):
                # 即这 4 个位置均为 0
                if np.sum(self.my_map[i:i + kernel_size, j:j + kernel_size]) == 0:
                    node_x, node_y = i, j
                    return node_x, node_y

        return node_x, node_y

    def locate_big_blank(self, node: tuple[int, int]) -> (list[tuple[int, int]]):
        """
        Locate a big blank in the map using BFS\n
        """
        open = Queue()
        closed = Set()
        open.push(node)
        closed.add(node)
        while not open.empty():
            node = open.pop()
            closed.add(node)
            child_nodes = self.get_child_nodes(node)
            for child in child_nodes:
                if child not in closed\
                    and self.my_map[child[0]][child[1]] == MAP_BLACK:
                    open.push(child)

        node_list = list(closed._items)
        return node_list

    def eliminate_big_blank(self, 
                            node_list: list[tuple[int, int]],
                            random_rate: int = 0.5) -> (None):
        random.shuffle(node_list)
        for i, node in enumerate(node_list):
            if i < len(node_list) * random_rate:
                self.my_map[node[0]][node[1]] = MAP_WHITE
            else:
                self.my_map[node[0]][node[1]] = MAP_BLACK

    def show_path(self) -> (bool):
        if self.path_idx == len(self.path):
            return True

        node = self.path[self.path_idx]
        #print('node: {}'.format(node))
        self.tmp_map[node[0]][node[1]] = MAP_CYAN

        self.path_idx += 1

        return False

    def initialize_bfs(self) -> (None):
        if self.bfs_initialized:
            return

        self.set_tmp_map()

        node = self.start_node
        self.bfs_open.push(node)
        self.bfs_closed.add(node.pos)

        self.bfs_initialized = True

    def find_path_by_bfs(self) -> (bool):
        node = self.bfs_open.pop()
        self.bfs_closed.add(node.pos)

        if node == self.end_node:
            self.end_node.prev = node.prev
            self.path = self.end_node.path(self.start_node)
            self.path_idx = 0
            return True

        if node != self.start_node and node != self.end_node:
            self.tmp_map[node.pos[0]][node.pos[1]] = MAP_YELLOW
        
        child_nodes = self.get_child_nodes(node.pos)
        count = 0
        for child in child_nodes:
            if self.tmp_map[child[0]][child[1]] == MAP_WHITE:
                count += 1
                self.bfs_open.push(Node(child, node))
                self.tmp_map[child[0]][child[1]] = MAP_BLUE
            elif self.tmp_map[child[0]][child[1]] == MAP_GREEN:
                count += 1
                self.bfs_open.push(Node(child, node))
        
        if count == 0:
            self.tmp_map[node.pos[0]][node.pos[1]] = MAP_PINK
        
        return False

    def initialize_dfs(self) -> (None):
        if self.dfs_initialized:
            return

        self.set_tmp_map()

        node = self.start_node
        self.dfs_open.push(node)
        self.dfs_closed.add(node.pos)

        self.dfs_initialized = True

    def find_path_by_dfs(self) -> (bool):
        node = self.dfs_open.pop()
        self.dfs_closed.add(node.pos)
        
        if node == self.end_node:
            self.end_node.prev = node.prev
            self.path = self.end_node.path(self.start_node)
            self.path_idx = 0
            return True

        if node != self.start_node and node != self.end_node:
            self.tmp_map[node.pos[0]][node.pos[1]] = MAP_YELLOW
        
        child_nodes = self.get_child_nodes(node.pos)
        count = 0
        for child in child_nodes:
            if self.tmp_map[child[0]][child[1]] == MAP_WHITE:
                count += 1
                self.dfs_open.push(Node(child, node))
                self.tmp_map[child[0]][child[1]] = MAP_BLUE
            elif self.tmp_map[child[0]][child[1]] == MAP_GREEN:
                count += 1
                self.dfs_open.push(Node(child, node))
        
        if count == 0:
            self.tmp_map[node.pos[0]][node.pos[1]] = MAP_PINK
        
        return False

    def initialize_ids(self) -> (None):
        if self.ids_initialized:
            return

        self.set_tmp_map()

        node = self.start_node
        self.ids_open.push(node)
        self.ids_closed.add(node.pos)

        self.ids_initialized = True

    def depth_limited_search(self) -> (bool):
        if self.ids_open.empty():
            return True

        node = self.ids_open.pop()
        self.ids_closed.add(node.pos)

        if node == self.end_node:
            self.end_node.prev = node.prev
            self.path = self.end_node.path(self.start_node)
            self.path_idx = 0
            return True

        if node != self.start_node and node != self.end_node:
            self.tmp_map[node.pos[0]][node.pos[1]] = MAP_YELLOW

        node_depth = len(node.path(self.start_node))

        if node_depth > self.ids_depth:
            self.tmp_map[node.pos[0]][node.pos[1]] = MAP_BLUE
            return False
        
        child_nodes = self.get_child_nodes(node.pos)
        count = 0
        for child in child_nodes:
            if self.tmp_map[child[0]][child[1]] == MAP_WHITE:
                count += 1
                self.ids_open.push(Node(child, node))
                self.tmp_map[child[0]][child[1]] = MAP_BLUE
            elif self.tmp_map[child[0]][child[1]] == MAP_GREEN:
                count += 1
                self.ids_open.push(Node(child, node))

        if count == 0:
            self.tmp_map[node.pos[0]][node.pos[1]] = MAP_PINK

        return False

    def find_path_by_ids(self) -> (bool):
        if self.depth_limited_search():
            if self.end_node.prev is not None:
                return True

            self.ids_depth += 1
            self.ids_open = Stack()
            self.ids_closed = Set()
            self.set_tmp_map()
            self.ids_open.push(self.start_node)
            self.ids_closed.add(self.start_node.pos)
            return False
        
        return False

    def initialize_bbfs(self) -> (None):
        if self.bbfs_initialized:
            return

        self.set_tmp_map()

        node_1 = self.start_node
        node_2 = self.end_node
        self.bbfs_open_1.push(node_1)
        self.bbfs_open_2.push(node_2)
        self.bbfs_closed_1.add(node_1.pos)
        self.bbfs_closed_2.add(node_2.pos)

        self.bbfs_initialized = True

    def find_path_by_bbfs(self) -> (bool):
        node_1 = self.bbfs_open_1.pop()
        self.bbfs_closed_1.add(node_1.pos)

        node_2 = self.bbfs_open_2.pop()
        self.bbfs_closed_2.add(node_2.pos)

        tmp_1 = self.bbfs_open_1.find(node_2)
        tmp_2 = self.bbfs_open_2.find(node_1)
        if tmp_1 is not None:
            tmp_1 = self.bbfs_open_1._items[tmp_1]
            node_2_path = node_2.path(self.end_node)
            list.reverse(node_2_path)
            self.path = tmp_1.path(self.start_node) + [tmp_1.pos] + node_2_path
            self.path_idx = 0
            return True
        elif tmp_2 is not None:
            tmp_2 = self.bbfs_open_2._items[tmp_2]
            node_2_path = tmp_2.path(self.end_node)
            list.reverse(node_2_path)
            self.path = node_1.path(self.start_node) + [tmp_2.pos] + node_2_path
            self.path_idx = 0
            return True
        elif node_1 == self.end_node:
            self.path = node_1.path(self.start_node)
            self.path_idx = 0
            return True
        elif node_2 == self.start_node:
            node_2_path = node_2.path(self.end_node)
            list.reverse(node_2_path)
            self.path = node_2_path
            self.path_idx = 0
            return True

        if node_1 != self.start_node and node_1 != self.end_node:
            self.tmp_map[node_1.pos[0]][node_1.pos[1]] = MAP_YELLOW

        if node_2 != self.start_node and node_2 != self.end_node:
            self.tmp_map[node_2.pos[0]][node_2.pos[1]] = MAP_ORANGE

        child_nodes_1 = self.get_child_nodes(node_1.pos)
        child_nodes_2 = self.get_child_nodes(node_2.pos)
        
        count_1 = 0
        for child in child_nodes_1:
            if self.tmp_map[child[0]][child[1]] == MAP_WHITE or \
                self.tmp_map[child[0]][child[1]] == MAP_ORANGE or \
                self.tmp_map[child[0]][child[1]] == MAP_PURPLE:
                count_1 += 1
                self.bbfs_open_1.push(Node(child, node_1))
                self.tmp_map[child[0]][child[1]] = MAP_BLUE
            elif self.tmp_map[child[0]][child[1]] == MAP_GREEN:
                count_1 += 1
                self.bbfs_open_1.push(Node(child, node_1))

        if count_1 == 0:
            self.tmp_map[node_1.pos[0]][node_1.pos[1]] = MAP_PINK

        count_2 = 0
        for child in child_nodes_2:
            if self.tmp_map[child[0]][child[1]] == MAP_WHITE or \
                self.tmp_map[child[0]][child[1]] == MAP_YELLOW or \
                self.tmp_map[child[0]][child[1]] == MAP_BLUE:
                count_2 += 1
                self.bbfs_open_2.push(Node(child, node_2))
                self.tmp_map[child[0]][child[1]] = MAP_PURPLE
            elif self.tmp_map[child[0]][child[1]] == MAP_RED:
                count_2 += 1
                self.bbfs_open_2.push(Node(child, node_2))

        if count_2 == 0:
            self.tmp_map[node_2.pos[0]][node_2.pos[1]] = MAP_PINK

        return False

    def initialize_bdfs(self) -> (None):
        if self.bdfs_initialized:
            return

        self.set_tmp_map()

        node_1 = self.start_node
        node_2 = self.end_node
        self.bdfs_open_1.push(node_1)
        self.bdfs_open_2.push(node_2)
        self.bdfs_closed_1.add(node_1.pos)
        self.bdfs_closed_2.add(node_2.pos)

        self.bdfs_initialized = True

    def find_path_by_bdfs(self) -> (bool):
        node_1 = self.bdfs_open_1.pop()
        self.bdfs_closed_1.add(node_1.pos)

        node_2 = self.bdfs_open_2.pop()
        self.bdfs_closed_2.add(node_2.pos)

        if node_1 in self.bdfs_open_2:
            tmp = self.bdfs_open_2.find(node_1)
            tmp = self.bdfs_open_2._items[tmp]
            node_1_path = node_1.path(self.start_node)
            tmp_path = tmp.path(self.end_node)
            list.reverse(tmp_path)
            self.path = node_1_path + [tmp.pos] + tmp_path
            self.path_idx = 0
            return True
        elif node_2 in self.bdfs_open_1:
            tmp = self.bdfs_open_1.find(node_2)
            tmp = self.bdfs_open_1._items[tmp]
            node_2_path = node_2.path(self.end_node)
            list.reverse(node_2_path)
            self.path = tmp.path(self.start_node) + [tmp.pos] + node_2_path
            self.path_idx = 0
            return True
        elif node_1 == self.end_node:
            self.path = node_1.path(self.start_node)
            self.path_idx = 0
            return True
        elif node_2 == self.start_node:
            node_2_path = node_2.path(self.end_node)
            list.reverse(node_2_path)
            self.path = node_2_path
            self.path_idx = 0
            return True

        if node_1 != self.start_node and node_1 != self.end_node:
            self.tmp_map[node_1.pos[0]][node_1.pos[1]] = MAP_YELLOW

        if node_2 != self.start_node and node_2 != self.end_node:
            self.tmp_map[node_2.pos[0]][node_2.pos[1]] = MAP_ORANGE

        child_nodes_1 = self.get_child_nodes(node_1.pos)
        child_nodes_2 = self.get_child_nodes(node_2.pos)
        
        count_1 = 0
        for child in child_nodes_1:
            if self.tmp_map[child[0]][child[1]] == MAP_WHITE or \
                self.tmp_map[child[0]][child[1]] == MAP_ORANGE or \
                self.tmp_map[child[0]][child[1]] == MAP_PURPLE:
                count_1 += 1
                self.bdfs_open_1.push(Node(child, node_1))
                self.tmp_map[child[0]][child[1]] = MAP_BLUE
            elif self.tmp_map[child[0]][child[1]] == MAP_GREEN:
                count_1 += 1
                self.bdfs_open_1.push(Node(child, node_1))

        if count_1 == 0:
            self.tmp_map[node_1.pos[0]][node_1.pos[1]] = MAP_PINK
        
        count_2 = 0
        for child in child_nodes_2:
            if self.tmp_map[child[0]][child[1]] == MAP_WHITE or \
                self.tmp_map[child[0]][child[1]] == MAP_YELLOW or \
                self.tmp_map[child[0]][child[1]] == MAP_BLUE:
                count_2 += 1
                self.bdfs_open_2.push(Node(child, node_2))
                self.tmp_map[child[0]][child[1]] = MAP_PURPLE
            elif self.tmp_map[child[0]][child[1]] == MAP_RED:
                count_2 += 1
                self.bdfs_open_2.push(Node(child, node_2))

        if count_2 == 0:
            self.tmp_map[node_2.pos[0]][node_2.pos[1]] = MAP_PINK

        return False

    def initialize_bids(self) -> (None):
        if self.bids_initialized:
            return 

        self.set_tmp_map()

        node_1 = self.start_node
        node_2 = self.end_node
        self.bids_open_1.push(node_1)
        self.bids_open_2.push(node_2)
        self.bids_closed_1.add(node_1.pos)
        self.bids_closed_2.add(node_2.pos)

        self.bids_initialized = True

    def depth_limited_search_from_start(self) -> (int):
        if self.bids_open_1.empty():
            return 2

        node_1 = self.bids_open_1.pop()
        self.bids_closed_1.add(node_1.pos)

        if node_1 in self.bids_open_2:
            node_2 = self.bids_open_2.find(node_1)
            node_2 = self.bids_open_2._items[node_2]
            node_2_path = node_2.path(self.end_node)
            list.reverse(node_2_path)
            self.path = node_1.path(self.start_node) + [node_2.pos] + node_2_path
            self.path_idx = 0
            return 1
        elif node_1 == self.end_node:
            self.end_node.prev = node_1.prev
            self.path = self.end_node.path(self.start_node)
            self.path_idx = 0
            return 1

        if node_1 != self.start_node and node_1 != self.end_node:
            self.tmp_map[node_1.pos[0]][node_1.pos[1]] = MAP_YELLOW

        node_depth = len(node_1.path(self.start_node))

        if node_depth > self.bids_depth:
            self.tmp_map[node_1.pos[0]][node_1.pos[1]] = MAP_BLUE
            return 0
        
        child_nodes = self.get_child_nodes(node_1.pos)
        count = 0
        for child in child_nodes:
            if self.tmp_map[child[0]][child[1]] == MAP_WHITE or \
                self.tmp_map[child[0]][child[1]] == MAP_ORANGE or \
                self.tmp_map[child[0]][child[1]] == MAP_PURPLE:
                count += 1
                self.bids_open_1.push(Node(child, node_1))
                self.tmp_map[child[0]][child[1]] = MAP_BLUE
            elif self.tmp_map[child[0]][child[1]] == MAP_GREEN:
                count += 1
                self.bids_open_1.push(Node(child, node_1))

        if count == 0:
            self.tmp_map[node_1.pos[0]][node_1.pos[1]] = MAP_PINK

        return 0

    def depth_limited_search_from_end(self) -> (int):
        if self.bids_open_2.empty():
            return 2

        node_2 = self.bids_open_2.pop()
        self.bids_closed_2.add(node_2.pos)

        if node_2 in self.bids_open_1:
            node_1 = self.bids_open_1.find(node_2)
            node_1 = self.bids_open_1._items[node_1]
            node_2_path = node_2.path(self.end_node)
            list.reverse(node_2_path)
            self.path = node_1.path(self.start_node) + [node_2.pos] + node_2_path
            self.path_idx = 0
            return 1
        elif node_2 == self.start_node:
            self.start_node.prev = node_2.prev
            start_node_path = self.start_node.path(self.end_node)
            list.reverse(start_node_path)
            self.path = start_node_path
            self.path_idx = 0
            return 1

        if node_2 != self.start_node and node_2 != self.end_node:
            self.tmp_map[node_2.pos[0]][node_2.pos[1]] = MAP_ORANGE

        node_depth = len(node_2.path(self.end_node))

        if node_depth > self.bids_depth:
            self.tmp_map[node_2.pos[0]][node_2.pos[1]] = MAP_PURPLE
            return 0
        
        child_nodes = self.get_child_nodes(node_2.pos)
        count = 0
        for child in child_nodes:
            if self.tmp_map[child[0]][child[1]] == MAP_WHITE or \
                self.tmp_map[child[0]][child[1]] == MAP_YELLOW or \
                self.tmp_map[child[0]][child[1]] == MAP_BLUE:
                count += 1
                self.bids_open_2.push(Node(child, node_2))
                self.tmp_map[child[0]][child[1]] = MAP_PURPLE
            elif self.tmp_map[child[0]][child[1]] == MAP_RED:
                count += 1
                self.bids_open_2.push(Node(child, node_2))

        if count == 0:
            self.tmp_map[node_2.pos[0]][node_2.pos[1]] = MAP_PINK

        return 0

    def find_path_by_bids(self) -> (bool):
        result_1 = self.depth_limited_search_from_start()
        result_2 = self.depth_limited_search_from_end()

        if result_1 == 1 or result_2 == 1:
            return True

        if result_1 == 2 or result_2 == 2:
            self.bids_depth += 1
            self.bids_open_1 = Stack()
            self.bids_open_2 = Stack()
            self.bids_closed_1 = Set()
            self.bids_closed_2 = Set()
            self.set_tmp_map()
            self.bids_open_1.push(self.start_node)
            self.bids_closed_1.add(self.start_node.pos)
            self.bids_open_2.push(self.end_node)
            self.bids_closed_2.add(self.end_node.pos)
        
        return False

    def initialize_ucs(self) -> (None):
        if self.ucs_initialized:
            return

        self.set_tmp_map()

        node = self.start_node
        self.ucs_open = PriorityQueue(node)
        self.ucs_closed = Set()
        self.ucs_closed.add(node.pos)

        self.ucs_initialized = True

    def find_path_by_ucs(self) -> (bool):
        node = self.ucs_open.pop()
        self.ucs_closed.add(node.pos)

        if node == self.end_node:
            self.path = node.path(self.start_node)
            self.path_idx = 0
            return True
        
        if node != self.start_node and node != self.end_node:
            self.tmp_map[node.pos[0]][node.pos[1]] = MAP_YELLOW

        child_nodes = self.get_child_nodes(node.pos)
        count = 0
        for child in child_nodes:
            if self.tmp_map[child[0]][child[1]] == MAP_WHITE:
                count += 1
                self.ucs_open.push(Node(child, node, node.f + 1))
                self.ucs_closed.add(child)
                self.tmp_map[child[0]][child[1]] = MAP_BLUE
            elif self.tmp_map[child[0]][child[1]] == MAP_GREEN:
                count += 1
                self.ucs_open.push(Node(child, node, node.f + 1))
                self.ucs_closed.add(child)
            elif self.tmp_map[child[0]][child[1]] != MAP_BLACK:
                loc = self.ucs_open.find(Node(child, node)) 
                if loc is not None:
                    if self.ucs_open.compare_and_replace(loc, Node(child, node, node.f + 1)):
                        count += 1
        
        if count == 0:
            self.tmp_map[node.pos[0]][node.pos[1]] = MAP_PINK

        return False

    def initialize_gbfs(self) -> (None):
        if self.gbfs_initialized:
            return

        self.set_tmp_map()
        self.start_node.f = \
            abs(self.start_node.pos[0] - self.end_node.pos[0]) + \
            abs(self.start_node.pos[1] - self.end_node.pos[1])

        node = self.start_node
        self.gbfs_open = PriorityQueue(node)
        self.gbfs_closed = Set()
        self.gbfs_closed.add(node.pos)

        self.gbfs_initialized = True

    def find_path_by_gbfs(self) -> (bool):
        node = self.gbfs_open.pop()
        self.gbfs_closed.add(node.pos)

        if node == self.end_node:
            self.path = node.path(self.start_node)
            self.path_idx = 0
            return True

        if node != self.start_node and node != self.end_node:
            self.tmp_map[node.pos[0]][node.pos[1]] = MAP_YELLOW

        child_nodes = self.get_child_nodes(node.pos)
        count = 0
        for child in child_nodes:
            if self.tmp_map[child[0]][child[1]] == MAP_WHITE:
                count += 1
                f = abs(child[0] - self.end_node.pos[0]) + \
                    abs(child[1] - self.end_node.pos[1])
                self.gbfs_open.push(Node(child, node, f))
                self.gbfs_closed.add(child)
                self.tmp_map[child[0]][child[1]] = MAP_BLUE
            elif self.tmp_map[child[0]][child[1]] == MAP_GREEN:
                count += 1
                f = abs(child[0] - self.end_node.pos[0]) + \
                    abs(child[1] - self.end_node.pos[1])
                self.gbfs_open.push(Node(child, node, f))
                self.gbfs_closed.add(child)
            elif self.tmp_map[child[0]][child[1]] != MAP_BLACK:
                loc = self.gbfs_open.find(Node(child, node)) 
                if loc is not None:
                    f = abs(child[0] - self.end_node.pos[0]) + \
                        abs(child[1] - self.end_node.pos[1])
                    if self.gbfs_open.compare_and_replace(loc, Node(child, node, f)):
                        count += 1
        
        if count == 0:
            self.tmp_map[node.pos[0]][node.pos[1]] = MAP_PINK

        return False

    def initialize_a_star(self) -> (None):
        if self.a_star_initialized:
            return

        self.set_tmp_map()
        self.start_node.f = \
            abs(self.start_node.pos[0] - self.end_node.pos[0]) + \
            abs(self.start_node.pos[1] - self.end_node.pos[1])

        node = self.start_node
        self.a_star_open = PriorityQueue(node)
        self.a_star_closed = Set()
        self.a_star_closed.add(node.pos)

        self.a_star_initialized = True

    def find_path_by_a_star(self) -> (bool):
        node = self.a_star_open.pop()
        self.a_star_closed.add(node.pos)

        if node == self.end_node:
            self.end_node.prev = node.prev
            self.path = node.path(self.start_node)
            self.path_idx = 0
            return True

        if node != self.start_node and node != self.end_node:
            self.tmp_map[node.pos[0]][node.pos[1]] = MAP_YELLOW

        child_nodes = self.get_child_nodes(node.pos)
        count = 0
        for child in child_nodes:
            node_h = abs(node.pos[0] - self.end_node.pos[0]) + abs(node.pos[1] - self.end_node.pos[1])
            node_g = node.f - node_h
            child_g = node_g + 1
            child_h = abs(child[0] - self.end_node.pos[0]) + abs(child[1] - self.end_node.pos[1])
            f = child_g + child_h
            if self.tmp_map[child[0]][child[1]] == MAP_WHITE:
                count += 1
                self.a_star_open.push(Node(child, node, f))
                self.tmp_map[child[0]][child[1]] = MAP_BLUE
            elif self.tmp_map[child[0]][child[1]] == MAP_GREEN:
                count += 1
                self.a_star_open.push(Node(child, node, f))
            else:
                if self.tmp_map[child[0]][child[1]] != MAP_BLACK:
                    loc = self.a_star_open.find(Node(child, node)) 
                    if loc is not None:
                        if self.a_star_open.compare_and_replace(loc, Node(child, node, f)):
                            count += 1

        if count == 0:
            self.tmp_map[node.pos[0]][node.pos[1]] = MAP_PINK

        return False

    def initialize_b_a_star(self) -> (None):
        if self.b_a_star_initialized:
            return

        self.set_tmp_map()
        initial_f = abs(self.start_node.pos[0] - self.end_node.pos[0]) + \
                    abs(self.start_node.pos[1] - self.end_node.pos[1])
        self.start_node.f = initial_f
        self.end_node.f = initial_f

        self.b_a_star_open_1 = PriorityQueue(self.start_node)
        self.b_a_star_open_2 = PriorityQueue(self.end_node)
        self.b_a_star_closed_1 = Set()
        self.b_a_star_closed_2 = Set()
        self.b_a_star_closed_1.add(self.start_node.pos)
        self.b_a_star_closed_2.add(self.end_node.pos)

        self.b_a_star_initialized = True

    def find_path_by_b_a_star(self) -> (bool):
        node_1 = self.b_a_star_open_1.pop()
        self.b_a_star_closed_1.add(node_1.pos)

        node_2 = self.b_a_star_open_2.pop()
        self.b_a_star_closed_2.add(node_2.pos)

        if self.b_a_star_open_2.find(node_1) is not None:
            node_2_idx = self.b_a_star_open_2.find(node_1)
            node_2 = self.b_a_star_open_2._queue.pop(node_2_idx)
            node_2_path = node_2.path(self.end_node)
            list.reverse(node_2_path)
            self.path = node_1.path(self.start_node) + [node_2.pos] + node_2_path
            self.path_idx = 0
            return True
        elif self.b_a_star_open_1.find(node_2) is not None:
            node_1_idx = self.b_a_star_open_1.find(node_2)
            node_1 = self.b_a_star_open_1._queue.pop(node_1_idx)
            node_2_path = node_2.path(self.end_node)
            list.reverse(node_2_path)
            self.path = node_1.path(self.start_node) + [node_2.pos] + node_2_path
            self.path_idx = 0
            return True
        elif node_1 == self.end_node:
            self.path = node_1.path(self.start_node)
            self.path_idx = 0
            return True
        elif node_2 == self.start_node:
            node_2_path = node_2.path(self.end_node)
            list.reverse(node_2_path)
            self.path = node_2_path
            self.path_idx = 0
            return True

        if node_1 != self.start_node and node_1 != self.end_node:
            self.tmp_map[node_1.pos[0]][node_1.pos[1]] = MAP_YELLOW

        if node_2 != self.start_node and node_2 != self.end_node:
            self.tmp_map[node_2.pos[0]][node_2.pos[1]] = MAP_ORANGE
        
        child_nodes_1 = self.get_child_nodes(node_1.pos)
        child_nodes_2 = self.get_child_nodes(node_2.pos)

        count_1 = 0
        for child in child_nodes_1:
            node_1_h = abs(node_1.pos[0] - self.end_node.pos[0]) + abs(node_1.pos[1] - self.end_node.pos[1])
            node_1_g = node_1.f - node_1_h
            child_1_g = node_1_g + 1
            child_1_h = abs(child[0] - self.end_node.pos[0]) + abs(child[1] - self.end_node.pos[1])
            f = child_1_g + child_1_h
            if self.tmp_map[child[0]][child[1]] == MAP_WHITE or \
                self.tmp_map[child[0]][child[1]] == MAP_ORANGE or \
                self.tmp_map[child[0]][child[1]] == MAP_PURPLE:
                count_1 += 1
                self.b_a_star_open_1.push(Node(child, node_1, f))
                self.tmp_map[child[0]][child[1]] = MAP_BLUE
            elif self.tmp_map[child[0]][child[1]] == MAP_GREEN:
                count_1 += 1
                self.b_a_star_open_1.push(Node(child, node_1, f))
            else:
                if self.tmp_map[child[0]][child[1]] != MAP_BLACK:
                    loc = self.b_a_star_open_1.find(Node(child, node_1, f)) 
                    if loc is not None:
                        if self.b_a_star_open_1.compare_and_replace(loc, Node(child, node_1, f)):
                            count_1 += 1

        if count_1 == 0:
            self.tmp_map[node_1.pos[0]][node_1.pos[1]] = MAP_PINK

        count_2 = 0
        for child in child_nodes_2:
            node_2_h = abs(node_2.pos[0] - self.end_node.pos[0]) + abs(node_2.pos[1] - self.end_node.pos[1])
            node_2_g = node_2.f - node_2_h
            child_2_g = node_2_g + 1
            child_2_h = abs(child[0] - self.end_node.pos[0]) + abs(child[1] - self.end_node.pos[1])
            f = child_2_g + child_2_h
            if self.tmp_map[child[0]][child[1]] == MAP_WHITE or \
                self.tmp_map[child[0]][child[1]] == MAP_YELLOW or \
                self.tmp_map[child[0]][child[1]] == MAP_BLUE:
                count_2 += 1
                self.b_a_star_open_2.push(Node(child, node_2, f))
                self.tmp_map[child[0]][child[1]] = MAP_PURPLE
            elif self.tmp_map[child[0]][child[1]] == MAP_RED:
                count_2 += 1
                self.b_a_star_open_2.push(Node(child, node_2, f))
            else:
                if self.tmp_map[child[0]][child[1]] != MAP_BLACK:
                    loc = self.b_a_star_open_2.find(Node(child, node_2, f)) 
                    if loc is not None:
                        if self.b_a_star_open_2.compare_and_replace(loc, Node(child, node_2, f)):
                            count_2 += 1

        if count_2 == 0:
            self.tmp_map[node_2.pos[0]][node_2.pos[1]] = MAP_PINK

        return False

    def initialize_id_a_star(self) -> (None):
        if self.id_a_star_initialized:
            return

        self.set_tmp_map()
        self.start_node.f = abs(self.start_node.pos[0] - self.end_node.pos[0]) + \
                            abs(self.start_node.pos[1] - self.end_node.pos[1])

        self.id_a_star_open = PriorityQueue(self.start_node)
        self.id_a_star_closed = Set()
        self.id_a_star_closed.add(self.start_node.pos)

        self.id_a_star_initialized = True
    
    def depth_limited_a_star_search(self) -> (bool):
        if self.id_a_star_open.empty():
            return True

        node = self.id_a_star_open.pop()
        self.id_a_star_closed.add(node.pos)

        if node == self.end_node:
            self.end_node.prev = node.prev
            self.path = self.end_node.path(self.start_node)
            self.path_idx = 0
            return True

        if node != self.start_node and node != self.end_node:
            self.tmp_map[node.pos[0]][node.pos[1]] = MAP_YELLOW

        node_depth = len(node.path(self.start_node))

        if node_depth > self.id_a_star_depth:
            self.tmp_map[node.pos[0]][node.pos[1]] = MAP_BLUE
            return False
        
        child_nodes = self.get_child_nodes(node.pos)
        count = 0
        for child in child_nodes:
            node_h = abs(node.pos[0] - self.end_node.pos[0]) + abs(node.pos[1] - self.end_node.pos[1])
            node_g = node.f - node_h
            child_g = node_g + 1
            child_h = abs(child[0] - self.end_node.pos[0]) + abs(child[1] - self.end_node.pos[1])
            f = child_g + child_h
            if self.tmp_map[child[0]][child[1]] == MAP_WHITE:
                count += 1
                self.id_a_star_open.push(Node(child, node, f))
                self.tmp_map[child[0]][child[1]] = MAP_BLUE
            elif self.tmp_map[child[0]][child[1]] == MAP_GREEN:
                count += 1
                self.id_a_star_open.push(Node(child, node, f))
            else:
                if self.tmp_map[child[0]][child[1]] != MAP_BLACK:
                    loc = self.id_a_star_open.find(Node(child, node)) 
                    if loc is not None:
                        if self.id_a_star_open.compare_and_replace(loc, Node(child, node, f)):
                            count += 1

        if count == 0:
            self.tmp_map[node.pos[0]][node.pos[1]] = MAP_PINK

        return False

    def find_path_by_id_a_star(self) -> (bool):
        if self.depth_limited_a_star_search():
            if self.end_node.prev is not None:
                return True

            self.id_a_star_depth += 1
            self.set_tmp_map()
            self.start_node.f = abs(self.start_node.pos[0] - self.end_node.pos[0]) + \
                                abs(self.start_node.pos[1] - self.end_node.pos[1])
            self.id_a_star_open = PriorityQueue(self.start_node)
            self.id_a_star_closed = Set()
            self.id_a_star_closed.add(self.start_node.pos)
            return False
        
        return False

    def initialize_jps(self) -> (None):
        self.set_tmp_map()
        # TODO

    def find_path_by_jps(self) -> (bool):
        # TODO
        return True