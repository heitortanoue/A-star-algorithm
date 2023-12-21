import tkinter as tk
from algorithm import a_star

class AStarSimulator:
    def __init__(self, master, grid_size=10):
        self.master = master
        master.title("Simulador A*")

        self.grid_size = grid_size
        self.cells = {}
        self.start_point = None
        self.end_point = None
        self.obstacles = set()
        self.setup_grid()
        self.setup_keybindings()


    def setup_grid(self):
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                frame = tk.Frame(master=self.master, relief=tk.RAISED, borderwidth=0)
                frame.grid(row=i, column=j)

                screen_height = self.master.winfo_screenheight()
                label_size = 20
                height = int(screen_height / label_size / (self.grid_size + 1))
                width = int(height * 2.5)
                cell = tk.Label(master=frame, bg='white', width=width, height=height)
                cell.pack(padx=1, pady=1)

                cell.bind("<Button-1>", self.on_left_click(i, j))
                cell.bind("<Button-2>", self.on_middle_click(i, j))  # Para usuários de Mac, isso pode precisar ser alterado para <Button-3>
                cell.bind("<Button-3>", self.on_right_click(i, j))
                self.cells[(i, j)] = cell

    def setup_keybindings(self):
        self.master.bind("<Return>", self.start_search)
        self.master.bind("<BackSpace>", self.clear_grid)
        self.master.bind("<Escape>", lambda event: self.master.destroy())

    def on_left_click(self, i, j):
        def handler(event):
            self.set_start(i, j)
        return handler

    def on_middle_click(self, i, j):
        def handler(event):
            self.set_obstacle(i, j)
        return handler

    def on_right_click(self, i, j):
        def handler(event):
            self.set_end(i, j)
        return handler

    def set_start(self, i, j):
        if self.start_point:
            self.cells[self.start_point].config(bg='white')
        self.clear_path()

        self.start_point = (i, j)
        self.cells[(i, j)].config(bg='green')

    def set_end(self, i, j):
        if self.end_point:
            self.cells[self.end_point].config(bg='white')
        self.clear_path()

        self.end_point = (i, j)
        self.cells[(i, j)].config(bg='red')

    def set_obstacle(self, i, j):
        if (i, j) in self.obstacles:
            self.cells[(i, j)].config(bg='white')
            self.obstacles.remove((i, j))
        else:
            self.cells[(i, j)].config(bg='black')
            self.obstacles.add((i, j))

    def start_search(self, event=None):
        if self.start_point is None or self.end_point is None:
            print("Ponto de início ou fim não definido!")
            return

        # Limpar o grid, mas manter pontos de início, fim e obstáculos
        self.clear_path()

        # Preparar o grid para o algoritmo A*
        grid = [[0 if (i, j) not in self.obstacles else 1 for j in range(self.grid_size)] for i in range(self.grid_size)]

        # Chamar o algoritmo A*
        alg_result = a_star(self.start_point, self.end_point, grid)

        path, explored = alg_result

        # Atualizar a interface gráfica com os nós explorados
        for position in explored:
            if position != self.start_point and position != self.end_point:
                self.cells[position].config(bg='lightgray')

        if path is None:
            print("Não foi possível encontrar um caminho.")
            return

        # Atualizar a interface gráfica com o caminho encontrado
        for position in path:
            if position != self.start_point and position != self.end_point:
                self.cells[position].config(bg='blue')

    def clear_path(self, event=None):
        for (i, j), cell in self.cells.items():
            if (i, j) not in self.obstacles and (i, j) != self.start_point and (i, j) != self.end_point:
                cell.config(bg='white')

    def clear_grid(self, event=None):
        for cell in self.cells.values():
            cell.config(bg='white')
        self.start_point = None
        self.end_point = None
        self.obstacles.clear()