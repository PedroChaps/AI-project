# takuzu.py: Template para implementação do projeto de Inteligência Artificial 2021/2022.
# Devem alterar as classes e funções neste ficheiro de acordo com as instruções do enunciado.
# Além das funções e classes já definidas, podem acrescentar outras que considerem pertinentes.

# Grupo 00:
# 00000 Nome1
# 00000 Nome2

import sys
from search import (
    Problem,
    Node,
    astar_search,
    breadth_first_tree_search,
    depth_first_tree_search,
    greedy_search,
    recursive_best_first_search,
)


class TakuzuState:
    state_id = 0

    def __init__(self, board):
        self.board = board
        self.id = TakuzuState.state_id
        TakuzuState.state_id += 1

    def __lt__(self, other):
        return self.id < other.id

    # TODO: outros metodos da classe


class Board:
    """Representação interna de um tabuleiro de Takuzu."""

    # Método para criar uma instância de tabuleiro
    def __init__(self, size, board):
        self.board = board
        self.size = size


    # Método para mostrar a representação externa do tabuleiro
    def __str__2(self):
        out = ""
        i = 1
        for nr in self.board:
            out += str(nr)
            if i % self.size == 0:
                out += "\n"
            else:
                out += "\t"
            i += 1
        return out

    # FIXME remover depois, print diferente (que não é aceite no mooshak), em
    # que mostra os indices do tabuleiro
    def __str__(self):

        out = "   "
        for i in range(self.size):
            out += f"{i}    "
        out += "\n"
        for _ in range(self.size*5):
            out += "-"
        out += "\n"

        i = 1
        j = 1
        out += f"0| "
        for nr in self.board:

            out += str(nr)
            if i % self.size == 0:
                out += "\n"
                out += f"{j}| "
                j += 1
            else:
                out += "    "
            i += 1
        out = out[:-4]
        out += "\n"
        return out


    def get_number(self, row: int, col: int) -> int:
        """Devolve o valor na respetiva posição do tabuleiro."""

        # Verifica se a linha ou coluna está fora do limite
        if row >= self.size or col >= self.size:
            return None

        # Fancy math
        return self.board[self.size*row + col]


    def adjacent_vertical_numbers(self, row: int, col: int) -> (int, int):
        """Devolve os valores imediatamente abaixo e acima,
        respectivamente."""

        return self.get_number(row+1, col), self.get_number(row-1, col)


    def adjacent_horizontal_numbers(self, row: int, col: int) -> (int, int):
        """Devolve os valores imediatamente à esquerda e à direita,
        respectivamente."""

        return self.get_number(row, col-1), self.get_number(row, col+1)


    @staticmethod
    def parse_instance_from_stdin():
        """Lê o test do standard input (stdin) que é passado como argumento
        e retorna uma instância da classe Board.

        Por exemplo:
            $ python3 takuzu.py < input_T01

            > from sys import stdin
            > stdin.readline()
        """

        board = []

        # Lê as linhas
        lines = sys.stdin.readlines()
        size, values = int(lines[0]), lines[1:]

        # Adiciona os valores ao tabuleiro
        for line in values:
            line = line.split("\t")
            for nr in line:
                board.append(int(nr))

        return Board(size, board)

    # TODO: outros metodos da classe



class Takuzu(Problem):
    def __init__(self, board: Board):
        """O construtor especifica o estado inicial."""
        # TODO
        pass

    def actions(self, state: TakuzuState):
        """Retorna uma lista de ações que podem ser executadas a
        partir do estado passado como argumento."""
        # TODO
        pass

    def result(self, state: TakuzuState, action):
        """Retorna o estado resultante de executar a 'action' sobre
        'state' passado como argumento. A ação a executar deve ser uma
        das presentes na lista obtida pela execução de
        self.actions(state)."""
        # TODO
        pass

    def goal_test(self, state: TakuzuState):
        """Retorna True se e só se o estado passado como argumento é
        um estado objetivo. Deve verificar se todas as posições do tabuleiro
        estão preenchidas com uma sequência de números adjacentes."""
        # TODO
        pass

    def h(self, node: Node):
        """Função heuristica utilizada para a procura A*."""
        # TODO
        pass

    # TODO: outros metodos da classe


# FIXME apagar que isto é só para testar coisas
# Vou só "me inspirar" (a.k.a. copiar do search.py) no problema das NQueens e adaptar
class TakuzuTemp(Problem):

    def __init__(self, board: Board):
        """O construtor especifica o estado inicial."""
        super().__init__(board)
        self.size = board.size


    def actions(self, state: TakuzuState):
        """Retorna uma lista de ações que podem ser executadas a
        partir do estado passado como argumento."""
        # TODO
        pass


    def result(self, state: TakuzuState, action):
        """Retorna o estado resultante de executar a 'action' sobre
        'state' passado como argumento. A ação a executar deve ser uma
        das presentes na lista obtida pela execução de
        self.actions(state)."""
        # TODO
        pass


    def goal_test(self, state: TakuzuState):
        """Retorna True se e só se o estado passado como argumento é
        um estado objetivo. Deve verificar se todas as posições do tabuleiro
        estão preenchidas com uma sequência de números adjacentes."""
        # TODO
        pass


    def conflict(self, state: TakuzuState, val, row, col):
        """Verifica se colocar um valor val numa
        posicação (row, col) gera conflitos """
        return (self.conflictInCol(state.board, val, row, col) or
                self.conflictInRow(state.board, val, row, col) or
                self.repeatedCol(state.board, val, row, col) or
                self.repeatedRow(state.board, val, row, col)
                )


    def conflictInRow(self, board, val, row, col):
        """
        Verifica se há um número igual de 1s e 0s em cada coluna e
        se não há mais do que dois números iguais adjacentes
        """

        # Vê se não há mais do que dois números iguais adjacentes
        leftLeft = board.get_number(row, col-2)
        left = board.get_number(row, col-1)
        rightRight = board.get_number(row, col+2)
        right = board.get_number(row, col+1)

        if (leftLeft == left == val or         # -> [1, 1, _]
                left == val == right or        # -> [1, _, 1]
                val == right == rightRight):   # -> [_, 1, 1]
            return True


        # Conta o número de 0s e 1s
        # nr de vazios começa a 1 porque estamos a imaginar que colocamos o
        # 'val' no lugar
        nr0s = 0
        nr1s = 0
        nr_s = -1

        if val == 1:
            nr1s += 1
        elif val == 0:
            nr0s += 1

        for i in range(board.size):
            nr = board.get_number(row, i)
            if nr == 0:
                nr0s += 1
            elif nr == 1:
                nr1s += 1
            elif nr == 2:
                nr_s += 1


        # Verifica primeiro se a linha ficaria toda preenchida
        #   A diferença entre o número de 0s e 1s tem que ser no máximo 1.
        #   Se for maior que 1 então há confitos.
        # Se a linha não estiver preenchida, vê se o número de espaços vazios
        # chega para a diferença entre o número de 0s e 1s ser no máximo 1.
        if nr0s + nr1s == board.size:
            return abs(nr1s - nr0s) > 1
        else:
            if val == 1:
                return nr1s - (nr0s + nr_s) > 1
            elif val == 0:
                return nr0s - (nr1s + nr_s) > 1





    def h(self, node: Node):
        """Função heuristica utilizada para a procura A*."""
        # TODO
        pass

    # TODO: outros metodos da classe



# FIXME só para testar se os exemplos mostrados estão a funcionar bem
def tempExemplo1():
    board = Board.parse_instance_from_stdin()
    print("Initial:\n", board, sep="")

    print(board.adjacent_vertical_numbers(3, 3))
    print(board.adjacent_horizontal_numbers(3, 3))

    print(board.adjacent_vertical_numbers(1, 1))
    print(board.adjacent_horizontal_numbers(1, 1))

def tempTeste1():
    board = Board(4, [1, 1, 2, 2, 2, 2, 0, 2, 2, 0, 2, 2, 1, 1, 2, 0])
    print("Initial:\n", board, sep="")

    problem = TakuzuTemp(board)
    initial_state = TakuzuState(board)

    print(initial_state.board.get_number(2, 2))

    print(problem.conflictInRow(board, 1, 0, 3))  # True
    print(problem.conflictInRow(board, 0, 0, 3))  # False
    print(problem.conflictInRow(board, 1, 3, 2))  # True




if __name__ == "__main__":
    # TODO: Ler o ficheiro de input de sys.argv[1],

    #tempExemplo1()
    tempTeste1()




    # TODO: Usar uma técnica de procura para resolver a instância,
    # TODO: Retirar a solução a partir do nó resultante,
    # TODO: Imprimir para o standard output no formato indicado.


    pass
