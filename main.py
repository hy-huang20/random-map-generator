import sys
import time
import pygame

from random_map import *

WIDTH = 700
HEIGHT = 700

# second(s)
SHOW_PATH_TIME = 5

INITIAL = 0
GENERATE_MAP = 1
FIND_PATH = 2
# Breadth First Search
FIND_PATH_BY_BFS = 3
# Depth First Search
FIND_PATH_BY_DFS = 4
# Iterative Deepening Search
FIND_PATH_BY_IDS = 5
# Bidirectional Breadth First Search
FIND_PATH_BY_BBFS = 6
# Bidirectional Depth First Search
FIND_PATH_BY_BDFS = 7
# Bidirectional Iterative Deepening Search
FIND_PATH_BY_BIDS = 8
# Uniform Cost Search
FIND_PATH_BY_UCS = 9
# Greedy Best First Search
FIND_PATH_BY_GBFS = 10
# A Star Search
FIND_PATH_BY_A_STAR = 11
# Bidirectional A Star Search
FIND_PATH_BY_B_A_STAR = 12
# Iterative Deepening A Star Search
FIND_PATH_BY_ID_A_STAR = 13
# Jump Point Search
FIND_PATH_BY_JPS = 14

SHOW_PATH = 15
END = 16


class Game:
    def __init__(self):
        pygame.init()
        self.surface = pygame.display.set_mode((WIDTH, HEIGHT))
        self.caption = 'Random Map Generator'
        pygame.display.set_caption(self.caption)
        pygame.display.flip()
        self.surface.fill((0, 0, 0))

        self.switch_cases = {
            INITIAL: self.initial,
            GENERATE_MAP: self.generate_map,
            FIND_PATH: self.find_path,
            FIND_PATH_BY_BFS: self.find_path_by_bfs,
            FIND_PATH_BY_DFS: self.find_path_by_dfs,
            FIND_PATH_BY_IDS: self.find_path_by_ids,
            FIND_PATH_BY_BBFS: self.find_path_by_bbfs,
            FIND_PATH_BY_BDFS: self.find_path_by_bdfs,
            FIND_PATH_BY_BIDS: self.find_path_by_bids,
            FIND_PATH_BY_UCS: self.find_path_by_ucs,
            FIND_PATH_BY_GBFS: self.find_path_by_gbfs,
            FIND_PATH_BY_A_STAR: self.find_path_by_a_star,
            FIND_PATH_BY_B_A_STAR: self.find_path_by_b_a_star,
            FIND_PATH_BY_ID_A_STAR: self.find_path_by_id_a_star,
            FIND_PATH_BY_JPS: self.find_path_by_jps,
            SHOW_PATH: self.show_path,
            END: self.end
        }

        self.color_cases = {
            MAP_WHITE: (255, 255, 255), 
            MAP_BLACK: (0, 0, 0),       
            MAP_RED: (255, 0, 0),       
            MAP_GREEN: (0, 255, 0),     
            MAP_PINK: (212, 115, 212),  
            MAP_YELLOW: (255, 255, 0),  
            MAP_BLUE: (0, 0, 255),      
            MAP_CYAN: (0, 255, 255),    
            MAP_ORANGE: (255, 165, 0),  
            MAP_PURPLE: (128, 0, 128),  
        }

        self.state = INITIAL
        self.next_state = INITIAL
        self.random_map = RandomMap()

    def start(self):
        self.random_map.initialize()
        while True:
            self.event()
            self.paint()
            self.update()    

    def event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
    def paint(self):
        """
        Paint the map
        """
        if self.state > FIND_PATH and self.state < END:
            the_map = self.random_map.tmp_map
        else:
            the_map = self.random_map.my_map
        
        for i in range(MAP_SIZE):
            for j in range(MAP_SIZE):
                rect_color = self.color_cases.get(the_map[i][j])
                
                width = min(WIDTH, HEIGHT) // MAP_SIZE
                height = HEIGHT // MAP_SIZE
                pygame.draw.rect(
                    self.surface, rect_color, 
                    (i * width, j * height, width, height)
                )

    def update(self):
        func = self.switch_cases.get(self.state)
        func()
                
        pygame.display.update()

    def initial(self) -> (None):
        self.state = GENERATE_MAP

    def generate_map(self) -> (None):
        pygame.display.set_caption(self.caption + ' - BFS Map Generating ...')
        
        if self.random_map.generate():
            self.state = FIND_PATH

            self.random_map.set_start_and_end_node()
            self.random_map.eliminate_big_blanks()
            self.random_map.show_start_and_end_node()
            self.random_map.set_tmp_map()
    
    def find_path(self) -> (None):
        self.state = FIND_PATH_BY_BFS

    def find_path_by_bfs(self) -> (None):
        pygame.display.set_caption(self.caption + ' - Breadth First Search')

        self.random_map.initialize_bfs()
        if self.random_map.find_path_by_bfs():
            self.state = SHOW_PATH
            self.next_state = FIND_PATH_BY_DFS

    def find_path_by_dfs(self) -> (None):
        pygame.display.set_caption(self.caption + ' - Depth First Search')

        self.random_map.initialize_dfs()
        if self.random_map.find_path_by_dfs():
            self.state = SHOW_PATH
            self.next_state = FIND_PATH_BY_IDS

    def find_path_by_ids(self) -> (None):
        pygame.display.set_caption(self.caption + ' - Iterative Deepening Search')

        self.random_map.initialize_ids()
        if self.random_map.find_path_by_ids():
            self.state = SHOW_PATH
            self.next_state = FIND_PATH_BY_BBFS

    def find_path_by_bbfs(self) -> (None):
        pygame.display.set_caption(self.caption + ' - Bidirectional Breadth First Search')

        self.random_map.initialize_bbfs()
        if self.random_map.find_path_by_bbfs():
            self.state = SHOW_PATH
            self.next_state = FIND_PATH_BY_BDFS

    def find_path_by_bdfs(self) -> (None):
        pygame.display.set_caption(self.caption + ' - Bidirectional Depth First Search')

        self.random_map.initialize_bdfs()
        if self.random_map.find_path_by_bdfs():
            self.state = SHOW_PATH
            self.next_state = FIND_PATH_BY_BIDS

    def find_path_by_bids(self) -> (None):
        pygame.display.set_caption(self.caption + ' - Bidirectional Iterative Deepening Search')

        self.random_map.initialize_bids()
        if self.random_map.find_path_by_bids():
            self.state = SHOW_PATH
            self.next_state = FIND_PATH_BY_UCS

    def find_path_by_ucs(self) -> (None):
        pygame.display.set_caption(self.caption + ' - Uniform Cost Search')

        self.random_map.initialize_ucs()
        if self.random_map.find_path_by_ucs():
            self.state = SHOW_PATH
            self.next_state = FIND_PATH_BY_GBFS

    def find_path_by_gbfs(self) -> (None):
        pygame.display.set_caption(self.caption + ' - Greedy Best First Search')

        self.random_map.initialize_gbfs()
        if self.random_map.find_path_by_gbfs():
            self.state = SHOW_PATH
            self.next_state = FIND_PATH_BY_A_STAR

    def find_path_by_a_star(self) -> (None):
        pygame.display.set_caption(self.caption + ' - A* Search')

        self.random_map.initialize_a_star()
        if self.random_map.find_path_by_a_star():
            self.state = SHOW_PATH
            self.next_state = FIND_PATH_BY_B_A_STAR

    def find_path_by_b_a_star(self) -> (None):
        pygame.display.set_caption(self.caption + ' - Bidirectional A* Search')
        
        self.random_map.initialize_b_a_star()
        if self.random_map.find_path_by_b_a_star():
            self.state = SHOW_PATH
            self.next_state = FIND_PATH_BY_ID_A_STAR

    def find_path_by_id_a_star(self) -> (None):
        pygame.display.set_caption(self.caption + ' - Iterative Deepening A* Search')

        self.random_map.initialize_id_a_star()
        if self.random_map.find_path_by_id_a_star():
            self.state = SHOW_PATH
            self.next_state = FIND_PATH_BY_JPS

    def find_path_by_jps(self) -> (None):
        return
        pygame.display.set_caption(self.caption + ' - Jump Point Search')

        self.random_map.initialize_jps()
        if self.random_map.find_path_by_jps():
            self.state = SHOW_PATH
            self.next_state = END

    def show_path(self) -> (None):
        sleep_time = SHOW_PATH_TIME / len(self.random_map.path)
        time.sleep(sleep_time)
        if self.random_map.show_path():
            self.state = self.next_state
    
    def end(self) -> (None):
        pass


if __name__ == '__main__':
    game = Game()
    game.start()