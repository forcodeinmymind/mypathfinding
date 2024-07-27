import sys
import os

import pygame

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import csv2d
import csv2dxt
import mypathfinding
import pygwrapper
import grid

state_color = {"default": (pygame.Color("darkslategray3"), pygame.Color("darkslategrey")), \
               "start": (pygame.Color("seagreen1"), pygame.Color("seagreen4")), \
               "dest": (pygame.Color("deepskyblue1"), pygame.Color("dodgerblue3")), \
               "blockade": (pygame.Color("coral"), pygame.Color("coral4")), \
               "path": (pygame.Color("gold"), pygame.Color("goldenrod3")), \
               "mouseover": (pygame.Color("fuchsia"), pygame.Color("hotpink4"))}

class Sprite(pygwrapper.Sprite):

    def __init__(self, *groups):
        super().__init__(*groups)
        self.fgcolor = pygame.Color("darkslategray3")
        self.bgcolor = pygame.Color("darkslategrey")

    def set_image(self, id: int, coord: tuple[int, int], size: tuple[int, int]):
        self.image = pygame.Surface(size)
        self.rect.size = self.image.get_size()
        self.image.fill(self.bgcolor)
        pygame.draw.rect(self.image, self.fgcolor, (0, 0) + self.rect.size, 1)
        pygwrapper.draw.text(self.image, (6, 4), "%d\n%s" % (id, coord), self.fgcolor)


class Application(pygwrapper.Pygame):
    
    def __init__(self, size=(1366, 768)):
        super().__init__(size)
        self.grid = grid.Grid((12, 10), (64, 64))
        self.pathfinding = mypathfinding.Pathfinder(None, csv2d.create(self.grid.get_size(), 0))
        self.start = 0
        self.dest = len(self.grid) - 1
        self.mouseover = None
        self.csv_blockade: tuple[tuple[int]] = csv2d.load("tilemap12x10.csv")

    def new(self):
        for i in range(len(self.grid)):
            self.add_sprite(Sprite())
            self.set_state_color(i, self.get_state(i))
            self.all_sprites.sprites()[-1].set_image(i, self.grid.conv_index_to_coord(i), self.grid.get_cell_size())
            self.all_sprites.sprites()[-1].rect.topleft = self.grid.conv_index_to_pos(i)
        self.start = 0
        self.set_state_color(self.start, "start")
        self.dest = len(self.grid) - 1
        self.set_state_color(self.dest, "dest")

    def update(self) -> None:
        # inputhandling
        ## mouseover
        new_mouseover = None
        for sprite in self.all_sprites:
            if sprite.rect.collidepoint(pygame.mouse.get_pos()):
                new_mouseover = self.grid.conv_pos_to_index(pygame.mouse.get_pos())
        if new_mouseover != self.mouseover:
            prev_mouseover = self.mouseover
            self.mouseover = new_mouseover
            if prev_mouseover is not None:
                self.set_state_color(prev_mouseover, self.get_state(prev_mouseover))
            if new_mouseover is not None:
                self.set_state_color(new_mouseover, self.get_state(new_mouseover))
        if pygame.mouse.get_pressed()[0]:
            for sprite in self.all_sprites:
                if sprite.rect.collidepoint(pygame.mouse.get_pos()) and \
                   csv2d.get_item(self.csv_blockade, self.grid.conv_pos_to_index(pygame.mouse.get_pos())) == 0:
                    prev_start = self.start
                    self.start = self.grid.conv_pos_to_index(pygame.mouse.get_pos())
                    self.set_state_color(prev_start, self.get_state(prev_start))
                    self.set_state_color(self.start, self.get_state(self.start))


    def set_state_color(self, index: int = 0, state: str = "default"):
        self.all_sprites.sprites()[index].fgcolor = state_color[state][0]
        self.all_sprites.sprites()[index].bgcolor = state_color[state][1]
        if index == self.mouseover:
            self.all_sprites.sprites()[index].fgcolor = state_color["mouseover"][0]
        self.all_sprites.sprites()[index].set_image(index, \
                                                    self.grid.conv_index_to_coord(index), \
                                                    self.all_sprites.sprites()[index].rect.size)

    def get_state(self, index: int):
        if index in csv2dxt.get_indices(self.csv_blockade, 1):
            return "blockade"
        elif index in self.pathfinding.path:
            return "path"
        elif index == self.start:
            return "start"
        elif index == self.dest:
            return "dest"
        else:
            return "default"


pygwrapper.draw.drawtext.font_default.size = 14
app = Application()
app.init()
app.new()
app.main()
