# takuzu.py: Template para implementação do projeto de Inteligência Artificial 2021/2022.
# Devem alterar as classes e funções neste ficheiro de acordo com as instruções do enunciado.
# Além das funções e classes já definidas, podem acrescentar outras que considerem pertinentes.

# Grupo 29:
# 99184 Bernardo Prata
# 99298 Pedro Chaparro

import sys
from search import (
    Problem,
    Node,
    astar_search,
    breadth_first_tree_search,
    compare_searchers,
    depth_first_tree_search,
    greedy_search,
    recursive_best_first_search,
    breadth_first_graph_search,
    depth_first_graph_search
)


class Board:
    """Representação interna de um tabuleiro de Takuzu."""

    def __init__(self, size, board, nrFreeSlots=None, rowsQuantities=None,
                 colQuantities=None):
        """Método para criar uma instância de tabuleiro"""
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


    def __str__(self):
        """Método para mostrar a representação externa do tabuleiro"""
        out = ""
        i = 1
        for nr in self.board:
            out += str(nr)
            if i % self.size == 0:
                out += "\n"
            else:
                out += "\t"
            i += 1

        return out[:-1]  # Exclui um \n que está a mais no fim


    def get_number(self, row: int, col: int):
        """Devolve o valor na respetiva posição do tabuleiro."""

        # Verifica se a linha ou coluna está fora do limite
        if row >= self.size or col >= self.size or row < 0 or col < 0:
            return None

        # Fancy math
        return self.board[self.size * row + col]


    def free_position(self, row: int, col: int):
        """Verifica se uma posição está livre"""
        return self.get_number(row, col) == 2


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


    def colBecomesFull(self, col: int):
        """Verifica se uma dada coluna fica toda preenchida com uma jogada"""
        return self.colQuantities[col] == self.size - 1


    def rowBecomesFull(self, row: int):
        """Verifica se uma dada linha fica toda preenchida com uma jogada"""
        return self.rowsQuantities[row] == self.size - 1


    def getFullCols(self, colToExclude: int):
        """Devolve uma lista com todas as colunas preenchidas, excluindo uma
        coluna"""
        cols = []
        for i in range(self.size):
            if self.colQuantities[i] == self.size and i != colToExclude:
                cols.append(i)
        return cols


    def getFullRows(self, rowToExclude: int):
        """Devolve uma lista com todas as linhas preenchidas"""
        rows = []
        for i in range(self.size):
            if self.rowsQuantities[i] == self.size and i != rowToExclude:
                rows.append(i)
        return rows


    def getCol(self, col: int):
        """Devolve um vetor que representa uma dada coluna"""
        colVec = []
        for i in range(self.size):
            colVec.append(self.get_number(i, col))
        return colVec


    def getRow(self, row: int):
        """Devolve um vetor que representa uma dada linha"""
        rowVec = []
        for i in range(self.size):
            rowVec.append(self.get_number(row, i))
        return rowVec


    def isSameCol(self, colVec: list, c2: int):
        """Verifica se duas colunas são iguais"""
        # Percorre ambas as colunas em paralelo e para de procurar assim que
        # encontra um número diferente nas duas
        for i in range(self.size):
            if colVec[i] != self.get_number(i, c2):
                return False
        return True


    def isSameRow(self, rowVec: list, r2: int):
        """Verifica se duas linhas são iguais"""
        # Percorre ambas as linhas em paralelo e para de procurar assim que
        # encontra um número diferente nas duas
        for i in range(self.size):
            if rowVec[i] != self.get_number(r2, i):
                return False
        return True


    def insert(self, row: int, col: int, number: int):
        """Insere um número numa dada posição"""
        if row >= self.size or col >= self.size or number not in (0, 1):
            return None
        self.board[self.size * row + col] = number


    def makePlay(self, row: int, col: int, number: int):
        """Faz uma jogada no tabuleiro, inserindo um número numa dada posição e
           criando um novo tabuleiro (criam-se tabuleiros diferentes para cada
           um poder ficar guardado num TakuzuState)."""

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

    def __init__(self, board: Board):
        self.board = board
        self.id = TakuzuState.state_id
        TakuzuState.state_id += 1

    def __lt__(self, other):
        return self.id < other.id


class Takuzu(Problem):

    def __init__(self, board: Board):
        """O construtor especifica o estado inicial."""

        initial_state = TakuzuState(board)
        super().__init__(initial_state)
        self.size = board.size


    def actions(self, state: TakuzuState):
        """Retorna uma lista de ações que podem ser executadas a
           partir do estado passado como argumento."""

        # Primeira jogada, inicialmente nula, e lista de ações
        firstPlay = None
        actions = []

        # tabuleiro e tamanho do tabuleiro (para tornar mais claro)
        board = state.board
        size = board.size

        # Percorre todas as posições procurando as livres
        for i in range(size):
            for j in range(size):
                # Apenas faz algo quando encontra uma posição livre
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
        return not board.free_position(row, col)


    @staticmethod
    def conflictInRow(board: Board, val: int, row: int, col: int):
        """
        Verifica se não há mais do que dois números iguais adjacentes e se
        a diferença entre 1s e 0s é maior que um numa dada linha.
        """

        # Verifica se não existem mais do que dois números iguais adjacentes
        leftLeft = board.get_number(row, col - 2)
        left = board.get_number(row, col - 1)
        rightRight = board.get_number(row, col + 2)
        right = board.get_number(row, col + 1)

        if (leftLeft == left == val or  # -> [1, 1, _]
                left == val == right or  # -> [1, _, 1]
                val == right == rightRight):  # -> [_, 1, 1]
            return True

        # Conta o número de 0s e 1s
        # subtrai-se 1 ao número de posições vazias porque simula-se que se
        # coloca o valor 'val' nessa posição
        nr0s = 0
        nr1s = 0
        nr_s = board.size - board.rowsQuantities[row] - 1

        if val == 1:
            nr1s += 1
        elif val == 0:
            nr0s += 1

        # Conta o número de 0s e 1s na linha
        for i in range(board.size):
            nr = board.get_number(row, i)
            if nr == 0:
                nr0s += 1
            elif nr == 1:
                nr1s += 1

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

        # Verifica se não existem mais do que dois números iguais adjacentes
        topTop = board.get_number(row - 2, col)
        top = board.get_number(row - 1, col)
        botBot = board.get_number(row + 2, col)
        bot = board.get_number(row + 1, col)

        if (topTop == top == val or
                top == val == bot or
                val == bot == botBot):
            return True

        # Conta o número de 0s e 1s
        # subtrai-se 1 ao número de posições vazias porque simula-se que se
        # coloca o valor 'val' nessa posição
        nr0s = 0
        nr1s = 0
        nr_s = board.size - board.colQuantities[col] - 1

        if val == 1:
            nr1s += 1
        elif val == 0:
            nr0s += 1

        # Conta o número de 0s e 1s na coluna
        for i in range(board.size):
            nr = board.get_number(i, col)
            if nr == 0:
                nr0s += 1
            elif nr == 1:
                nr1s += 1


        # Verifica primeiro se a linha ficaria toda preenchida
        #   A diferença entre o número de 0s e 1s tem que ser no máximo 1.
        #   Se for maior que 1 então há confitos.
        # Se a coluna não estiver preenchida, vê se o número de espaços vazios
        # chega para a diferença entre o número de 0s e 1s ser no máximo 1.
        if nr0s + nr1s == board.size:
            return abs(nr1s - nr0s) > 1
        else:
            if val == 1:
                return nr1s - (nr0s + nr_s) > 1
            elif val == 0:
                return nr0s - (nr1s + nr_s) > 1


    @staticmethod
    def repeatedCol(board: Board, val: int, row: int, col: int):
        """Verifica se a coluna col está repetida no tabuleiro board"""

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
    def repeatedRow(board: Board, val: int, row: int, col: int):
        """Verifica se a linha row está repetida no tabuleiro board"""

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
        actions = self.actions(node.state)
        if (actions==None or len(actions)==0):
            return node.state.board.nrFreeSlots * 2 
        return node.state.board.nrFreeSlots + len(actions) - 1 
        #minimo passos possiveis é preenhcer todas as slots vazias sempre com len(actions)==1, e os dois valores para a atual
        # UPDATE 20:00 -its not ;( but we still got the implementation xD



def compare_graph_searchers():
    """Prints a table of search results."""
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
    compare_searchers(problems=[problem],header=['Searcher','Takuzu'],
                        searchers=[breadth_first_tree_search,
                                 breadth_first_graph_search,
                                 depth_first_graph_search,astar_search
                                ])

if __name__ == "__main__":
    #board = Board(4, [1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,0])
    #problem = Takuzu(board)
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
    #solution = depth_first_graph_search(problem)
    solution = astar_search(problem, lambda node: problem.h(node))
    print(solution.state.board)
    #compare_graph_searchers()