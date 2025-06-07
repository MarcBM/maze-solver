import time
import random
from graphics import Window, Line, Point

class Maze():
    def __init__(self, x1, y1, num_rows, num_cols, cell_size_x, cell_size_y, seed=None, animation_delay=0.05, window=None):
        self.__x1 = x1
        self.__y1 = y1
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.__cell_size_x = cell_size_x
        self.__cell_size_y = cell_size_y
        self.__seed = seed
        if self.__seed is not None:
            random.seed(self.__seed)
        self.__animation_delay = animation_delay
        self.__win = window
        self.__cells = []
        self.__create_cells()
        self.__break_entrance_and_exit()
        self.__break_walls_r(0, 0)
        self.__reset_cells_visited()

    def __create_cells(self):
        for x in range(self.num_cols):
            self.__cells.append([])
            for y in range(self.num_rows):
                self.__cells[x].append(Cell(self.__win))
                self.__draw_cell(x, y)
                
    def __break_entrance_and_exit(self):
        self.__cells[0][0].has_top_wall = False
        self.__draw_cell(0, 0)
        self.__cells[self.num_cols - 1][self.num_rows - 1].has_bottom_wall = False
        self.__draw_cell(self.num_cols - 1, self.num_rows - 1)
    
    def __break_walls_r(self, i, j):
        self.__cells[i][j].visited = True
        directions = [(0, -1), (1, 0), (0, 1), (-1, 0)]
        random.shuffle(directions)
        for di, dj in directions:
            ni, nj = i + di, j + dj
            if 0 <= ni < self.num_cols and 0 <= nj < self.num_rows:
                if not self.__cells[ni][nj].visited:
                    if di == 0 and dj == -1:
                        self.__cells[i][j].has_top_wall = False
                        self.__cells[ni][nj].has_bottom_wall = False
                    elif di == 1 and dj == 0:
                        self.__cells[i][j].has_right_wall = False
                        self.__cells[ni][nj].has_left_wall = False
                    elif di == 0 and dj == 1:
                        self.__cells[i][j].has_bottom_wall = False
                        self.__cells[ni][nj].has_top_wall = False
                    elif di == -1 and dj == 0:
                        self.__cells[i][j].has_left_wall = False
                        self.__cells[ni][nj].has_right_wall = False
                    self.__break_walls_r(ni, nj)
        self.__draw_cell(i, j)
        
    def __reset_cells_visited(self):
        for i in range(self.num_cols):
            for j in range(self.num_rows):
                self.__cells[i][j].visited = False
                
    def solve(self):
        return self.__solve_r(0, 0)
        
    def __solve_r(self, i, j):
        self.__animate()
        self.__cells[i][j].visited = True
        if i == self.num_cols - 1 and j == self.num_rows - 1:
            return True
        directions = [(1, 0), (0, 1), (0, -1), (-1, 0)]
        # random.shuffle(directions)
        for di, dj in directions:
            ni, nj = i + di, j + dj
            if 0 <= ni < self.num_cols and 0 <= nj < self.num_rows:
                if not self.__cells[ni][nj].visited:
                    if di == 0 and dj == -1 and not self.__cells[i][j].has_top_wall:
                        self.__cells[i][j].draw_move(self.__cells[ni][nj])
                        if self.__solve_r(ni, nj):
                            return True
                        else:
                            self.__cells[i][j].draw_move(self.__cells[ni][nj], undo=True)
                    elif di == 1 and dj == 0 and not self.__cells[i][j].has_right_wall:
                        self.__cells[i][j].draw_move(self.__cells[ni][nj])
                        if self.__solve_r(ni, nj):
                            return True
                        else:
                            self.__cells[i][j].draw_move(self.__cells[ni][nj], undo=True)
                    elif di == 0 and dj == 1 and not self.__cells[i][j].has_bottom_wall:
                        self.__cells[i][j].draw_move(self.__cells[ni][nj])
                        if self.__solve_r(ni, nj):
                            return True
                        else:
                            self.__cells[i][j].draw_move(self.__cells[ni][nj], undo=True)
                    elif di == -1 and dj == 0 and not self.__cells[i][j].has_left_wall:
                        self.__cells[i][j].draw_move(self.__cells[ni][nj])
                        if self.__solve_r(ni, nj):
                            return True
                        else:
                            self.__cells[i][j].draw_move(self.__cells[ni][nj], undo=True)
        return False
    
    def __draw_cell(self, i, j):
        x1 = self.__x1 + i * self.__cell_size_x
        x2 = x1 + self.__cell_size_x
        y1 = self.__y1 + j * self.__cell_size_y
        y2 = y1 + self.__cell_size_y

        self.__cells[i][j].draw(x1, y1, x2, y2)
        self.__animate()

    def __animate(self):
        if self.__win is not None:
            self.__win.redraw()
            time.sleep(self.__animation_delay)


class Cell():
    def __init__(self, window=None):
        self.has_left_wall = True
        self.has_right_wall = True
        self.has_top_wall = True
        self.has_bottom_wall = True
        self.__x1 = -1
        self.__x2 = -1
        self.__y1 = -1
        self.__y2 = -1
        self.__win = window
        self.visited = False

    def draw(self, x1, y1, x2, y2):
        self.__x1 = x1
        self.__y1 = y1
        self.__x2 = x2
        self.__y2 = y2

        self.draw_wall(x1, y1, x1, y2, self.has_left_wall)
        self.draw_wall(x2, y1, x2, y2, self.has_right_wall)
        self.draw_wall(x1, y1, x2, y1, self.has_top_wall)
        self.draw_wall(x1, y2, x2, y2, self.has_bottom_wall)

    def draw_wall(self, x1, y1, x2, y2, showing=True):
        if self.__win is not None:
            p1 = Point(x1, y1)
            p2 = Point(x2, y2)
            line = Line(p1, p2)
            colour = "black" if showing else "white"
            self.__win.draw_line(line, colour)

    def draw_move(self, to_cell, undo=False):
        if self.__win is not None:
            line = Line(self.get_centre(), to_cell.get_centre())
            if undo:
                colour = "gray"
            else:
                colour = "red"
            self.__win.draw_line(line, colour)

    def get_centre(self):
        return Point((self.__x1 + self.__x2) / 2, (self.__y1 + self.__y2) / 2)