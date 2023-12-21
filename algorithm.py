import heapq

# Algoritmo A*
# f(n) = g(n) + h(n)
#
# g(n) = custo do caminho do nó inicial até o nó n
# h(n) = heurística do nó n até o nó final
# f(n) = custo total do caminho do nó inicial até o nó final passando pelo nó n

# celula do grid
class Cell:
    def __init__(self, pos, parent=None):
        self.pos = pos
        self.parent = parent
        self.g = 0 # custo do caminho do nó inicial até o nó n
        self.h = 0 # heurística do nó n até o nó final
        self.f = 0 # custo total do caminho do nó inicial até o nó final passando pelo nó n

    def __eq__(self, other):
        return self.pos == other.pos

    def __lt__(self, other):
        return self.f < other.f

    def __repr__(self):
        return f"Cell({self.pos}, {self.f})"

def a_star(start, end, grid):
    # Inicializa a célula de início e fim
    start_cell = Cell(start)
    end_cell = Cell(end)

    # Inicializa a lista aberta e fechada
    open_list = []
    closed_list = set()

    # Adiciona a célula de início na lista aberta
    heapq.heappush(open_list, start_cell)
    explored = set()

    # Loop até que a lista aberta esteja vazia
    while open_list:
        # Obter o nó com menor f da lista aberta
        current_cell = heapq.heappop(open_list)
        closed_list.add(current_cell.pos)
        explored.add(current_cell.pos)

        # Verifica se alcançou o objetivo
        if current_cell == end_cell:
            path = []
            while current_cell:
                path.append(current_cell.pos)
                current_cell = current_cell.parent
            return path[::-1], explored  # Retorna o caminho invertido

        # Gera os vizinhos do nó atual
        for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
            node_position = (current_cell.pos[0] + new_position[0], current_cell.pos[1] + new_position[1])

            # Verifica se a nova posição é válida e não é um obstáculo
            if 0 <= node_position[0] < len(grid) and 0 <= node_position[1] < len(grid[0]) and not grid[node_position[0]][node_position[1]]:
                if node_position in closed_list:
                    continue

                new_cell = Cell(node_position, current_cell)

                # Calcula os custos g, h e f
                new_cell.g = current_cell.g + 1
                new_cell.h = abs(node_position[0] - end[0]) + abs(node_position[1] - end[1])
                new_cell.f = new_cell.g + new_cell.h

                # Adiciona a nova célula na lista aberta se não estiver lá
                if not any(cell for cell in open_list if cell.pos == new_cell.pos and cell.f <= new_cell.f):
                    heapq.heappush(open_list, new_cell)

    return None, explored  # Se não encontrar um caminho
