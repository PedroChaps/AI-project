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

class Board:
    """Representação interna de um tabuleiro de Takuzu."""

    # Método para criar uma instância de tabuleiro
    def __init__(self, size, board, nrFreeSlots=None, rowsQuantities=None,
                 colQuantities=None):
        self.board = board
        self.size = size

        # Variáveis iniciais
        if nrFreeSlots is None or rowsQuantities is None or colQuantities is None:
            nrFreeSlots = self.size ** 2
            rowsQuantities = [0 for _ in range(self.size)]
            colQuantities = [0 for _ in range(self.size)]

            # Percorre o tabuleiro para contar o número de slots ocupados do
            # tabuleiro inicial, bem como a quantidade de números por linha e por
            # coluna
            for i in range(self.size):
                for j in range(self.size):
                    if self.get_number(i, j) != 2:
                        nrFreeSlots -= 1
                        rowsQuantities[i] += 1
                        colQuantities[j] += 1

        self.nrFreeSlots = nrFreeSlots
        self.rowsQuantities = rowsQuantities
        self.colQuantities = colQuantities

    # Método para mostrar a representação externa do tabuleiro
    def __str__(self):
        out = ""
        i = 1
        for nr in self.board:
            out += str(nr)
            if i % self.size == 0:
                out += "\n"
            else:
                out += "\t"
            i += 1
        # print(repr(out))
        return out[:-1] # Exclui um \n que está a mais no fim


    # FIXME remover depois, print diferente (que não é aceite no mooshak), em
    # que mostra os indices do tabuleiro
    def __str__2(self):

        out = "   "
        for i in range(self.size):
            out += f"{i}    "
        out += "\n"
        for _ in range(self.size * 5):
            out += "-"
        out += "\n"

        i = 1
        j = 1
        out += f"0| "
        for nr in self.board:

            if nr != 2:
                out += str(nr)
            else:
                out += " "
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


    def get_number(self, row: int, col: int):
        """Devolve o valor na respetiva posição do tabuleiro."""

        # Verifica se a linha ou coluna está fora do limite
        if row >= self.size or col >= self.size or row < 0 or col < 0:
            return None

        # Fancy math
        return self.board[self.size * row + col]

    def free_position(self, row: int, col: int):
        return self.get_number(row,col)==2

    def adjacent_vertical_numbers(self, row: int, col: int) -> (int, int):
        """Devolve os valores imediatamente abaixo e acima,
        respectivamente."""

        return self.get_number(row + 1, col), self.get_number(row - 1, col)


    def adjacent_horizontal_numbers(self, row: int, col: int) -> (int, int):
        """Devolve os valores imediatamente à esquerda e à direita,
        respectivamente."""

        return self.get_number(row, col - 1), self.get_number(row, col + 1)


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


    # Verifica se uma dada coluna fica toda preenchida com uma jogada
    def colBecomesFull(self, col: int):
        return self.colQuantities[col] == self.size - 1


    # Verifica se uma dada linha fica toda preenchida com uma jogada
    def rowBecomesFull(self, row: int):
        return self.rowsQuantities[row] == self.size - 1


    # Devolve uma lista com todas as colunas preenchidas
    def getFullCols(self, colToExclude: int):
        cols = []
        for i in range(self.size):
            if self.colQuantities[i] == self.size and i != colToExclude:
                cols.append(i)
        return cols


    # Devolve uma lista com todas as linhas preenchidas
    def getFullRows(self, rowToExclude: int):
        rows = []
        for i in range(self.size):
            if self.rowsQuantities[i] == self.size and i != rowToExclude:
                rows.append(i)
        return rows


    def getCol(self, col: int):
        colVec = []
        for i in range(self.size):
            colVec.append(self.get_number(i, col))
        return colVec

    def getRow(self, row: int):
        rowVec = []
        for i in range(self.size):
            rowVec.append(self.get_number(row, i))
        return rowVec


    # Verifica se duas colunas são iguais
    # Percorre ambas as colunas em paralelo e para de procurar assim que
    # encontra um número diferente nas duas
    def isSameCol(self, colVec: list, c2: int):
        for i in range(self.size):
            if colVec[i] != self.get_number(i, c2):
                return False
        return True


    # Verifica se duas linhas são iguais
    # Percorre ambas as linhas em paralelo e para de procurar assim que
    # encontra um número diferente nas duas
    def isSameRow(self, rowVec: list, r2: int):
        for i in range(self.size):
            if rowVec[i] != self.get_number(r2, i):
                return False
        return True


    # Insere um número numa dada posição
    def insert(self, row: int, col: int, number: int):
        if row >= self.size or col >= self.size or number not in (0, 1):
            return None
        self.board[self.size * row + col] = number


    # Faz uma jogada no tabuleiro, inserindo um número numa dada posição e
    # criando um novo tabuleiro (criam-se tabuleiros diferentes para cada um
    # poder ficar guardado num TakuzuState).
    def makePlay(self, row: int, col: int, number: int):

        # Calcula o novo número de slots livres, bem como as novas quantidades
        # de números na linha e coluna jogadas
        new_nrFreeSlots = self.nrFreeSlots - 1

        new_rowsQuantites = self.rowsQuantities.copy()
        new_rowsQuantites[row] += 1

        new_colQuantites = self.colQuantities.copy()
        new_colQuantites[col] += 1

        # Cria um novo tabuleiro (necessário ser um novo e não atualizar pois
        # queremos manter os vários tabuleiros distribuidos por todos os
        # estados)
        newBoard = Board(self.size,
                         self.board.copy(),
                         new_nrFreeSlots,
                         new_rowsQuantites,
                         new_colQuantites)

        # Insere o numero na posição certa do novo tabuleiro e devolve-o
        newBoard.insert(row, col, number)

        return newBoard



class TakuzuState:
    state_id = 0

    def __init__(self,  board: Board):
        self.board = board
        self.id = TakuzuState.state_id
        TakuzuState.state_id += 1

    def __lt__(self, other):
        return self.id < other.id


class Takuzu(Problem):

    def __init__(self, board: Board):
        """O construtor especifica o estado inicial."""

        initial_state= TakuzuState(board)
        super().__init__(initial_state)
        self.size = board.size


    def actions2(self, state: TakuzuState):
        """Retorna uma lista de ações que podem ser executadas a
        partir do estado passado como argumento."""




        ##### ISTO É A PARTE DEPOIS DAS JOGADAS OBRIGATORIAS
        board = state.board
        size = board.size
        rows = board.rowsQuantities
        cols = board.colQuantities

        #Encontrar primeira posicao livre- a que tem a coluna e linha nao totalmente preenchida
        for x in range(size):
            if rows[x] < size:
                free_spot_row=x  
                break
        for x in range(size):
            if board.free_position(free_spot_row,x):
                free_spot_col = x
                break

        actions = []
        #Ou jogo 0
        if not self.conflict(state,0,free_spot_row,free_spot_col):
            actions.extend([(free_spot_row,free_spot_col,0)])
        #Ou jogo 1
        if not self.conflict(state,1,free_spot_row,free_spot_col):
            actions.extend([(free_spot_row,free_spot_col,1)])

        return actions


    def actions(self, state: TakuzuState):

        firstPlay = None
        actions = []

        board = state.board
        size = board.size
        rows = board.rowsQuantities
        cols = board.colQuantities

        for i in range(size):
            for j in range(size):
                if board.free_position(i, j):
                    for val in (0, 1):
                        if not self.conflict(state, val, i, j):
                            actions.extend([(i, j, val)])
                    # Se existir apenas uma jogada possivel para a posição atual,
                    # significa que é uma jogada obrigatória. Então, joga-a
                    if len(actions) == 1:
                        return actions
                    # Se for a primeira jogada possivel, guardo-a para mais logo
                    # a utilizar, caso não existam jogadas obrigatórias
                    elif firstPlay is None:
                        firstPlay = actions.copy()
                    # Faço reset às ações possiveis
                    actions = []

        # Se não encontrei nenhuma jogada obrigatória, então retorno a primeira
        # jogada possivel, por questões de eficiência

        return firstPlay



    def result(self, state: TakuzuState, action):
        """Retorna o estado resultante de executar a 'action' sobre
        'state' passado como argumento. A ação a executar deve ser uma
        das presentes na lista obtida pela execução de
        self.actions(state)."""

        # Extrai a informação da ação
        row, col, val = action

        # Cria um novo tabuleiro, fazendo uma jogada com a respetiva linha,
        # coluna e valor
        newBoard = state.board.makePlay(row, col, val)
        return TakuzuState(newBoard)


    def goal_test(self, state: TakuzuState):
        """Retorna True se e só se o estado passado como argumento é
        um estado objetivo. Deve verificar se todas as posições do tabuleiro
        estão preenchidas com uma sequência de números adjacentes."""

        # Como vamos verificando as regras sempre que fazemos cada jogada,
        # tem-se a certeza que todas as peças colocadas num tabuleiro
        # são válidas. Então, apenas se verifica se existe alguma
        # peça livre no tabuleiro.
    
        return state.board.nrFreeSlots == 0


    def conflict(self, state: TakuzuState, val, row, col):
        """
        Verifica se colocar um valor val numa
        posicação (row, col) gera conflitos.
        """
        return (self.numberAlreadyThere(state.board, row, col) or
                self.conflictInCol(state.board, val, row, col) or
                self.conflictInRow(state.board, val, row, col) or
                self.repeatedCol(state.board, val, row, col) or
                self.repeatedRow(state.board, val, row, col)
                )

    @staticmethod
    def numberAlreadyThere(board: Board, row: int, col: int):
        return not board.free_position(row,col)


    @staticmethod
    def conflictInRow(board: Board, val: int, row: int, col: int):
        """
        Verifica se não há mais do que dois números iguais adjacentes e se
        a diferença entre 1s e 0s é maior que um numa dada linha.
        """

        # Vê se não há mais do que dois números iguais adjacentes
        leftLeft = board.get_number(row, col - 2)
        left = board.get_number(row, col - 1)
        rightRight = board.get_number(row, col + 2)
        right = board.get_number(row, col + 1)

        if (leftLeft == left == val or  # -> [1, 1, _]
                left == val == right or  # -> [1, _, 1]
                val == right == rightRight):  # -> [_, 1, 1]
            return True

        # Conta o número de 0s e 1s
        # subtrai-se 1 ao nr de vazios porque estamos a imaginar que colocamos o
        # 'val' no lugar
        nr0s = 0
        nr1s = 0
        nr_s = board.size - board.rowsQuantities[row] - 1

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

        # FIXME DEBUG apagar este print
        # print(nr0s, nr1s, nr_s)

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


    @staticmethod
    def conflictInCol(board: Board, val: int, row: int, col: int):
        """
        Verifica se não há mais do que dois números iguais adjacentes e se
        a diferença entre 1s e 0s é maior que um numa dada coluna.
        """

        # Vê se não há mais do que dois números iguais adjacentes
        topTop = board.get_number(row - 2, col)
        top = board.get_number(row - 1, col)
        botBot = board.get_number(row + 2, col)
        bot = board.get_number(row + 1, col)

        if (topTop == top == val or
                top == val == bot or
                val == bot == botBot):
            return True

        # Conta o número de 0s e 1s
        # subtrai-se 1 ao nr de vazios porque estamos a imaginar que colocamos o
        # 'val' no lugar
        nr0s = 0
        nr1s = 0
        nr_s = board.size - board.colQuantities[col] - 1

        if val == 1:
            nr1s += 1
        elif val == 0:
            nr0s += 1

        for i in range(board.size):
            nr = board.get_number(i, col)
            if nr == 0:
                nr0s += 1
            elif nr == 1:
                nr1s += 1

        # FIXME DEBUG apagar este print
        #print(nr0s, nr1s, nr_s)

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


    @staticmethod
    # Verifica se a coluna col está repetida no tabuleiro board
    def repeatedCol(board: Board, val: int, row: int, col: int):

        # Se a coluna não ficar toda preenchida, não faz sentido verificar
        # se está repetida
        if not board.colBecomesFull(col):
            return False

        # Busca o conjunto de colunas já preenchidas, excluido a atual
        fullCols = board.getFullCols(col)

        # Busca um vetor com a coluna atual e simula a jogada
        colVec = board.getCol(col)
        colVec[row] = val

        # Compara todas as colunas preenchidas com a atual
        for c in fullCols:
            # Se forem iguais, então existe conflito
            if board.isSameCol(colVec, c):
                return True

        return False


    @staticmethod
    # Verifica se a linha row está repetida no tabuleiro board
    def repeatedRow(board: Board, val: int, row: int, col: int):

        # Se a linha não ficar toda preenchida, não faz sentido verificar
        # se está repetida
        if not board.rowBecomesFull(row):
            return False

        # Busca o conjunto de linhas já preenchidas, excluido a atual
        fullRows = board.getFullRows(row)

        # Busca um vetor com a linha atual e simula a jogada
        rowVec = board.getRow(row)
        rowVec[col] = val

        # Compara todas as linhas preenchidas com a atual
        for r in fullRows:
            # Se forem iguais, então existe conflito
            if board.isSameRow(rowVec, r):
                return True

        return False


    def h(self, node: Node):
        """Função heuristica utilizada para a procura A*."""
        # TODO
        pass




# FIXME Funções de testes, apagar depois da entrega
# \/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/
# /\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\


def tempExemplo1():
    board = Board.parse_instance_from_stdin()
    print("Initial:\n", board, sep="")

    print(board.adjacent_vertical_numbers(3, 3))
    print(board.adjacent_horizontal_numbers(3, 3))

    print(board.adjacent_vertical_numbers(1, 1))
    print(board.adjacent_horizontal_numbers(1, 1))


def tempTeste1():
    board = Board(4, [1, 1, 2, 2, 2, 2, 0, 2, 2, 0, 1, 2, 1, 1, 2, 0])
    print("Initial:\n", board, sep="")

    problem = Takuzu(board)
    initial_state = TakuzuState(board)

    print(initial_state.board.get_number(2, 2))

    print(problem.conflictInCol(board, 1, 0, 3))  # True
    print(problem.conflictInCol(board, 0, 0, 3))  # False
    print(problem.conflictInCol(board, 1, 3, 2))  # True
    print(problem.conflictInCol(board, 1, 1, 1))  # True
    print(problem.conflictInCol(board, 0, 1, 1))  # True
    print(problem.conflictInCol(board, 0, 2, 0))  # True

def testingResult():
    board = Board(4, [1, 1, 2, 2, 2, 2, 0, 2, 2, 0, 1, 2, 1, 1, 2, 0])

    print("Initial:\n", board, sep="")
    print("row:", board.rowsQuantities, " col:", board.colQuantities, " free:",
          board.nrFreeSlots)

    problem = Takuzu(board)
    initial_state = TakuzuState(board)

    final_state = problem.result(initial_state, (0, 2, 1))
    board2 = final_state.board
    print("Final:\n", board2, sep="")
    print("row:", board2.rowsQuantities, " col:", board2.colQuantities,
          " free:", board2.nrFreeSlots)


def testingRepeatedCol():
    board = Board(4, [1, 1, 1, 2,
                      0, 1, 0, 2,
                      1, 0, 1, 2,
                      1, 1, 1, 0])

    print("Initial:\n", board, sep="")
    print("row:", board.rowsQuantities, " col:", board.colQuantities, " free:",
          board.nrFreeSlots)

    problem = Takuzu(board)
    initial_state = TakuzuState(board)

    print(problem.repeatedCol(board, 0))


def testingRepeatedRow():
    board = Board(4, [1, 1, 1, 1,
                      0, 1, 0, 1,
                      0, 1, 0, 1,
                      1, 1, 1, 0])

    print("Initial:\n", board, sep="")
    print("row:", board.rowsQuantities, " col:", board.colQuantities, " free:",
          board.nrFreeSlots)

    problem = Takuzu(board)
    initial_state = TakuzuState(board)

    print(problem.repeatedRow(board, 0))


def testingAction1():
    ## Nao ha jogada possivel,porque posicao(0,3) nao pode ser 0, nem 1

    board = Board(4, [1, 1, 1, 2,
                      0, 1, 0, 2,
                      1, 0, 1, 2,
                      1, 1, 1, 0])

    print("Initial:\n", board, sep="")
    print("row:", board.rowsQuantities, " col:", board.colQuantities, " free:",
          board.nrFreeSlots)

    problem = Takuzu(board)
    initial_state = TakuzuState(board)

    print(problem.actions(initial_state))

def testingAction2():
    ## Jogada possivel e (0, 2, 0), porque se fosse 1 iria ter coluna repetida 
    board = Board(4, [1, 1, 2, 2, 2, 2, 0, 2, 2, 0, 1, 2, 1, 1, 2, 0])

    print("Initial:\n", board, sep="")
    print("row:", board.rowsQuantities, " col:", board.colQuantities, " free:",
          board.nrFreeSlots)

    problem = Takuzu(board)
    initial_state = TakuzuState(board)

    print(problem.actions(initial_state))

def testingAction3():
    ## Jogada possivel e (1,0,0), ter tres 1s e apenas um 0
    board = Board(4, [1, 1, 0, 1, 2, 2, 0, 2, 0, 2, 1, 2, 1, 1, 2, 0])

    print("Initial:\n", board, sep="")
    print("row:", board.rowsQuantities, " col:", board.colQuantities, " free:",
          board.nrFreeSlots)

    problem = Takuzu(board)
    initial_state = TakuzuState(board)

    print(problem.actions(initial_state))


def test_search():
    board = Board(4, [2,1,2,0,2,2,0,2,2,0,2,2,1,1,2,0])
    # Criar uma instância de Takuzu:
    problem = Takuzu(board)

    print("Initial:\n", problem.initial.board, sep="")

    # Obter o nó solução usando a procura em profundidade:
    goal_node = depth_first_tree_search(problem)
    if goal_node == None:
        print("No solution found")
    # Verificar se foi atingida a solução
    print("Is goal?", problem.goal_test(goal_node.state))
    print("Solution:\n", goal_node.state.board, sep="")

# Igual ao test_search() mas a ler do input
def exemplo4():
    # Ler tabuleiro do ficheiro 'i1.txt' (Figura 1):
    # $ python3 takuzu < i1.txt
    board = Board.parse_instance_from_stdin()
    # Criar uma instância de Takuzu:
    problem = Takuzu(board)
    # Obter o nó solução usando a procura em profundidade:
    goal_node = depth_first_tree_search(problem)
    # Verificar se foi atingida a solução
    print("Is goal?", problem.goal_test(goal_node.state))
    print("Solution:\n", goal_node.state.board, sep="")


# O Formato do mooshak é só mostrar o tabuleiro
def solveWithMooshakFormat():
    board = Board.parse_instance_from_stdin()
    problem = Takuzu(board)
    goal_node = depth_first_tree_search(problem)
    print(goal_node.state.board, sep="")
    return 0


def debuggarInput03():
    board = Board(8, [2, 2, 2, 0, 0, 2, 2, 0,
                      1, 2, 2, 2, 2, 0, 2, 2,
                      2, 0, 2, 0, 1, 2, 2, 1,
                      2, 2, 2, 2, 2, 1, 2, 2,
                      2, 2, 1, 2, 1, 2, 0, 0,
                      0, 2, 2, 2, 2, 2, 0, 1,
                      2, 0, 2, 2, 0, 2, 2, 2,
                      2, 2, 2, 1, 1, 2, 0, 2])

    # Criar uma instância de Takuzu:
    problem = Takuzu(board)

    print("Initial:\n", problem.initial.board, sep="")

    # Obter o nó solução usando a procura em profundidade:
    goal_node = depth_first_tree_search(problem)
    if goal_node == None:
        print("No solution found")
    # Verificar se foi atingida a solução
    print("Is goal?", problem.goal_test(goal_node.state))
    print("Solution:\n", goal_node.state.board, sep="")

# \/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/
# /\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\


if __name__ == "__main__":

    # tempExemplo1()
    # tempTeste1()
    # testingResult()
    #testingRepeatedCol()
    #testingRepeatedRow()
    
    #testingAction1()
    #testingAction2()
    #testingAction3()
    
    #test_search()

    #exemplo4()

    solveWithMooshakFormat()

    #debuggarInput03()

    # TODO: Usar uma técnica de procura para resolver a instância,
    # TODO: Retirar a solução a partir do nó resultante,
    # TODO: Imprimir para o standard output no formato indicado.


