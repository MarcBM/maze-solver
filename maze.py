import time
from graphics import Window, Line, Point

class Maze():
    def __init__(self, x1, y1, num_rows, num_cols, cell_size_x, cell_size_y, animation_delay, window):
        self.__x1 = x1
        self.__y1 = y1
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.__cell_size_x = cell_size_x
        self.__cell_size_y = cell_size_y
        self.__animation_delay = animation_delay
        self.__win = window
        self.__cells = []
        self.__create_cells()

    def __create_cells(self):
        for x in range(self.num_cols):
            self.__cells.append([])
            for y in range(self.num_rows):
                self.__cells[x].append(Cell(self.__win))
                self.__draw_cell(x, y)
    
    def __draw_cell(self, i, j):
        x1 = self.__x1 + i * self.__cell_size_x
        x2 = x1 + self.__cell_size_x
        y1 = self.__y1 + j * self.__cell_size_y
        y2 = y1 + self.__cell_size_y

        self.__cells[i][j].draw(x1, y1, x2, y2)
        self.__animate()

    def __animate(self):
        self.__win.redraw()
        time.sleep(self.__animation_delay)


class Cell():
    def __init__(self, window):
        self.has_left_wall = True
        self.has_right_wall = True
        self.has_top_wall = True
        self.has_bottom_wall = True
        self.__x1 = -1
        self.__x2 = -1
        self.__y1 = -1
        self.__y2 = -1
        self.__win = window

    def draw(self, x1, y1, x2, y2):
        self.__x1 = x1
        self.__y1 = y1
        self.__x2 = x2
        self.__y2 = y2

        if self.has_left_wall:
            self.draw_wall(x1, y1, x1, y2)
        if self.has_right_wall:
            self.draw_wall(x2, y1, x2, y2)
        if self.has_top_wall:
            self.draw_wall(x1, y1, x2, y1)
        if self.has_bottom_wall:
            self.draw_wall(x1, y2, x2, y2)

    def draw_wall(self, x1, y1, x2, y2):
        p1 = Point(x1, y1)
        p2 = Point(x2, y2)
        line = Line(p1, p2)
        self.__win.draw_line(line)

    def draw_move(self, to_cell, undo=False):
        line = Line(self.get_centre(), to_cell.get_centre())
        if undo:
            colour = "gray"
        else:
            colour = "red"
        self.__win.draw_line(line, colour)

    def get_centre(self):
        return Point((self.__x1 + self.__x2) / 2, (self.__y1 + self.__y2) / 2)