"""
astar pathfinding
astar pathfinding_Sebastian Lague_YouTube_2014-12-16
"""

import logging
logging.basicConfig(level=logging.DEBUG, filename=f"{__name__}.log", filemode="w", format="%(message)s")
# format="%(asctime)s - %(levelname)s - %(message)s")

ATTR_G = 0
ATTR_H = 1
ATTR_F = 2
ATTR_PARENT = 3


class Pathfinder:
    """
    A* pathfinding algorithm for 2D square grid maps

    Attributes
    ----------
    map_csv : tuple
    nodes : dict
        dict of node data: {cell_id: (g_value, h_value, f_value, parent_id)}
    """
    def __init__(self, grid, map_csv) -> None:
        self.grid = grid
        self.map_csv = map_csv
        self.nodes = dict()
        self.start = 0
        self.end = 0
        self.open = list()
        self.closed = list()
        self.loop_ctr = 0
        self.path = list()

    def __str__(self):
        return f"<Pathfinder, grid={self.grid}>"

    def init_find(self, start: tuple[int, int], end: tuple[int, int]):
        self.start = self.grid.conv_index(*start)
        self.end = self.grid.conv_index(*end)
        self.add_node(self.start, \
                      0, \
                      self.get_h(self.start), \
                      self.get_h(self.start), \
                      -1)
        self.open = [self.start]
        self.closed = list()
        self.loop_ctr = 0

    def find_path(self, start: tuple[int, int], end: tuple[int, int]):
        logging.debug(f"{__name__}.find_path({start=}, {end=}")
        self.init_find(start, end)
        while not self.close_next():
            pass

    def close_next(self) -> bool:
        if len(self.open) > 0:
            logging.debug(f"start iteration: {self.loop_ctr}")
            self.sort_open()
            self.closed.append(self.open.pop(0))
            logging.debug(f"closed add: {self.str_node(self.closed[-1])}")
        else:
            return True
        if self.closed[-1] == self.end:
            path = list()
            cur_node = self.end
            while self.nodes[cur_node][ATTR_PARENT] > -1:
                path.append(cur_node)
                cur_node = self.nodes[cur_node][ATTR_PARENT]
            path.append(self.start)
            path.reverse()
            self.path = path
            return True
        else:
            # add adjoin nodes
            for _dir, adjoin in enumerate(self.grid.get_adjoins(self.closed[-1])):
                if adjoin is None:
                    pass
                elif adjoin in self.closed:
                    pass
                elif self.is_blocked(adjoin):
                    # not traversable
                    # add to closed
                    pass
                elif adjoin in self.open:
                    # check; update?
                    if self.nodes[adjoin][ATTR_G] > self.nodes[self.closed[-1]][ATTR_G] + self.get_g(_dir):
                        g_value = self.nodes[self.closed[-1]][ATTR_G] + self.get_g(_dir)
                        self.add_node(adjoin, \
                                      g_value, \
                                      self.nodes[adjoin][ATTR_H], \
                                      g_value + self.nodes[adjoin][ATTR_H], \
                                      self.closed[-1])
                else:
                    self.open.append(adjoin)
                    g_value = self.nodes[self.closed[-1]][ATTR_G] + self.get_g(_dir)
                    h_value = self.get_h(adjoin)
                    self.add_node(adjoin, \
                                  g_value, \
                                  h_value, \
                                  g_value + h_value, \
                                  self.closed[-1])
        self.loop_ctr +=1
        return False

    def add_node(self, node_id: int, g_value: int, h_value: int, f_value: int, parent_id: int):
        """g_value = distance from start
           h_value = distance from end
           f_value = g_value + h_value
           parent_id
        """
        self.nodes[node_id] = (g_value, h_value, f_value, parent_id)

    def get_g(self, direction_id: int) -> int:
        """convert vector to g cost
        """
        if self.grid.is_ortho_dir_id(direction_id):
            return 10
        else:
            return 14

    def get_h(self, node_id: int) -> int:
        d_ortho, d_diag = self.grid.get_heuristic(self.grid.conv_coord(node_id), \
                                                  self.grid.conv_coord(self.end))
        return d_ortho * 10 + d_diag * 14

    def is_blocked(self, node_id: int) -> bool:
        return bool(self.map_csv[self.grid.conv_coord(node_id)[1]][self.grid.conv_coord(node_id)[0]])

    def sort_open(self):
        # open_sorted_f = sorted(self.open, key=lambda x: self.nodes[x][ATTR_F])
        min_f = min(self.nodes[node_id][ATTR_F] for node_id in self.open)
        min_f_nodes = [node_id for node_id in self.open if self.nodes[node_id][ATTR_F] == min_f]
        for node_id in min_f_nodes:
            del self.open[self.open.index(node_id)]
        if len(min_f_nodes) == 1:
            self.open.insert(0, min_f_nodes[0])
        else:
            min_h = sorted(min_f_nodes, key=lambda x: self.nodes[x][ATTR_H], reverse=True)
            for node_id in min_h:
                self.open.insert(0, node_id)

    def sort_nodes(self, column: int, reverse: bool):
        self.nodes = dict(sorted(self.nodes.items(), key=lambda items: items[1][column], reverse=reverse))

    def str_node(self, node_id: int):
        PAD_VALUE = 3
        string = "".join((f"<Node, {self.grid.str_cell(node_id)}, ", \
                          f"g={self.nodes[node_id][ATTR_G]:{PAD_VALUE}}, ", \
                          f"h={self.nodes[node_id][ATTR_H]:{PAD_VALUE}}, ", \
                          f"f={self.nodes[node_id][ATTR_F]:{PAD_VALUE}}, ", \
                          f"p={self.nodes[node_id][ATTR_PARENT]:{PAD_VALUE}}, ", \
                          f"{"open" if node_id in self.open else "closed"}>"))
        return string

    def str_diagnose(self):
        string = f"{self}\n"
        for node_id in self.nodes:
            string += f"{self.str_node(node_id)}\n"
        return string

    def get_cell_state(self, cell_id: int):
        if cell_id in self.path:
            return "path"
        elif cell_id in self.open:
            return "open"
        elif cell_id in self.closed:
            return "closed"
        elif self.is_blocked(cell_id):
            return "blocked"
        else:
            return "none"

if __name__ == "__main__":
    from constants import map_0_10x7
    grid = None
    _pathfinder = Pathfinder(grid, map_0_10x7)
    pass
