from tkinter import Tk, BOTH, Canvas

class Window():
    def __init__(self, width, height):
        self.root_widget = Tk()
        self.root_widget.title = "Maze Solver"
        self.canvas = Canvas(master=self.root_widget, bg="white", height=height, width=width)
        self.canvas.pack(fill=BOTH, expand=1)
        self.running = False
        self.root_widget.protocol("WM_DELETE_WINDOW", self.close)
    
    def redraw(self):
        self.root_widget.update_idletasks()
        self.root_widget.update()

    def wait_for_close(self):
        self.running = True
        while self.running:
            self.redraw()
        print("Window closed...")
    
    def close(self):
        self.running = False
    
    def draw_line(self, line, fill_colour="black"):
        line.draw(self.canvas, fill_colour)

class Point():
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Line():
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def draw(self, canvas, fill_colour="black"):
        canvas.create_line(self.a.x, self.a.y, self.b.x, self.b.y, fill=fill_colour, width=2)
