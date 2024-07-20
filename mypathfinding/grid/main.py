"""
astar pathfinding
astar pathfinding_Sebastian Lague_YouTube_2014-12-16
"""


def get_size_array2d(array) -> tuple[int, int]:
    """Convert a 2D array to a tuple of (width, height)
       array = ((0, 0, 0, \
                 0, 0, 0)) -> size = (x=3, y=2)
    """
    return len(array[0]), len(array)

def get_value_array2d(array, x: int, y: int) -> int:
    return array[y][x]


class Grid:
    ortogdiagonal_vectors = ((1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1), (1, -1))
    def __init__(self, size: tuple[int, int], cell_size: tuple[int, int]) -> None:
        self.width = size[0]
        self.height = size[1]
        self.cell_width = cell_size[0]
        self.cell_height = cell_size[1]

    def __str__(self) -> str:
        return f"<Grid, ({self.width}, {self.height})>"

    def __len__(self) -> int:
        return self.width * self.height

    def get_size(self) -> tuple[int, int]:
        return self.width, self.height

    def get_cell_size(self) -> tuple[int, int]:
        return self.cell_width, self.cell_height

    def conv_index(self, x: int, y: int) -> int:
        return x + y * self.width

    def conv_coord(self, index: int) -> tuple[int, int]:
        x = index % self.width
        y = index // self.width
        return x, y

    def conv_coord_pos(self, pos: tuple[int, int]) -> tuple[int, int]:
        return pos[0] // self.cell_width, pos[1] // self.cell_height

    def conv_pos(self, x: int, y: int) -> tuple[int, int]:
        return x * self.cell_width, y * self.cell_height

    def get_coords(self):
        return [(x, y) for y in range(self.height) for x in range(self.width)]

    def in_grid(self, coord: tuple[int, int] | None) -> bool:
        if 0 <= coord[0] < self.width and 0 <= coord[1] < self.height:
            return True
        else:
            return False

    def get_adjoin_coords(self, coord: tuple[int, int]):
        # -> (coord, vector)
        for vector in Grid.ortogdiagonal_vectors:
            coord_adjoin = coord[0] + vector[0], coord[1] + vector[1]
            if self.in_grid(coord_adjoin):
                yield coord_adjoin
            else:
                yield None

    def get_adjoins(self, index: int):
        # -> (node_id, vector)
        for coord in self.get_adjoin_coords(self.conv_coord(index)):
            if coord is not None:
                yield self.conv_index(*coord)
            else:
                yield None

    def is_ortho_vector(self, vector: tuple[int, int]) -> bool:
        return abs(vector[0]) is not abs(vector[1])

    def is_ortho_dir_id(self, dir_id: int) -> bool:
        """direction id is orthogonal; not diagonal
           0 = E, 1 = SE, 2 = S
        """
        return bool((dir_id + 1) % 2)

    def get_vector_od(self, coord: tuple[int, int], dest: tuple[int, int]) -> tuple[int, int]:
        """returns orthodiagonal vector from coord to dest
           (1, 0) = E, (1, 1) = NE, ...
        """
        if dest[0] - coord[0] > 0:
            vx = 1
        elif dest[0] - coord[0] < 0:
            vx = -1
        else:
            vx = 0
        if dest[1] - coord[1] > 0:
            vy = 1
        elif dest[1] - coord[1] < 0:
            vy = -1
        else:
            vy = 0
        return vx, vy

    def get_heuristic(self, coord: tuple[int, int], dest: tuple[int, int]) -> tuple[int, int]:
        """Returns orthagonal and diagonal distance from coord to dest in coords
        """
        dx = abs(dest[0] - coord[0])
        dy = abs(dest[1] - coord[1])

        d_ortho = max(dx, dy) - min(dx, dy)
        d_diagonal = min(dx, dy)

        return d_ortho, d_diagonal

    def get_dist_coords(self, coord: tuple[int, int], dest: tuple[int, int]) -> tuple[int, int]:
        return dest[0] - coord[0], dest[1] - coord[1]

    def str_grid(self):
        string = str()
        pad_id = len(str(len(self)))
        pad_coord = len(str(max(self.width, self.height) - 1))
        for y in range(self.height):
            for x in range(self.width):
                string += f"[{self.conv_index(x, y):{pad_id}}({x:>{pad_coord}}, {y:>{pad_coord}})]"
            string += "\n"
        return string

    def str_cell(self, cell_id: int):
        pad_id = len(str(len(self)))
        pad_coord = len(str(max(self.width, self.height) - 1))
        x, y = self.conv_coord(cell_id)
        return f"<Cell, id={cell_id:{pad_id}}, ({x:>{pad_coord}}, {y:>{pad_coord}}))>"

if __name__ == "__main__":
    _grid = Grid((11, 8), (32, 32))
    _x = 9
    _y = 6
    print("\n" + _grid.str_grid() + "\n")
    print(f"{_grid.get_size()=}")
    print(f"{_grid.conv_index(_x, _y)=}")
    print(f"{_grid.conv_coord(_grid.conv_index(_x, _y))=}")
    print(f"{_grid.get_coords()=}")
    print(f"_grid.get_adjoins(_grid.conv_index({_x}, {_y}))")
    print([adjoin for adjoin in _grid.get_adjoins(_grid.conv_index(_x, _y))])
