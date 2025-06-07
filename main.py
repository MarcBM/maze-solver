from graphics import Window
from maze import Maze

def main():
    win = Window(800, 600)

    maze = Maze(50, 50, 20, 28, 25, 25, 0.01, win)

    win.wait_for_close()



if __name__ == "__main__":
    main()