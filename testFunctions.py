# Funções para testar o código escrito

from takuzu import *

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


if __name__ == "__main__":
    exemplo4()