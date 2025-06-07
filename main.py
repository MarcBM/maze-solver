from graphics import Window
from maze import Maze

def main():
    win = Window(800, 600)

    maze = Maze(50, 50, 20, 28, 25, 25, animation_delay=0.01, window=win)
    # maze = Maze(50, 50, 10, 14, 50, 50, animation_delay=0.01, window=win)
    
    maze.solve()

    win.wait_for_close()



if __name__ == "__main__":
    main()