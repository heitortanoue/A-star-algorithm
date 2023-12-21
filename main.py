from window import AStarSimulator
import tkinter as tk

def main():
    root = tk.Tk()

    grid_size = 20
    AStarSimulator(root, grid_size=grid_size)
    root.mainloop()

if __name__ == '__main__':
    main()