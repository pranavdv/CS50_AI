"""
Tic Tac Toe Player
"""

import math
import copy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    cnt = 0
    for row in board:
        for cell in row : 
            cnt += (cell==EMPTY)
    return X if cnt%2 else O
    raise NotImplementedError


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    res = set()
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY: res.add((i,j))
    return res
    raise NotImplementedError


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    new = copy.deepcopy(board)
    (i,j) = action
    turn = player(board)
    new[i][j] = turn
    return new
    raise NotImplementedError


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    # check horizontally 
    for i in range(3):
        if board[i][0]==board[i][1]==board[i][2]:
            return board[i][0]   
    # check vertically
    for j in range(3):
            if board[0][j]==board[1][j]==board[2][j]:
                return board[0][j]
    # positive diagonal
    if board[2][0]==board[1][1]==board[0][2]:
        return board[1][1]
    # negative diagonal
    if board[0][0] == board[1][1] == board[2][2]:
        return board[1][1]
    return None
    raise NotImplementedError


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    cnt = 0
    for row in board:
        for cell in row : cnt+=(cell==EMPTY)
    if not cnt or (winner(board) is not None):
        return True
    return False
    raise NotImplementedError


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    res = winner(board)
    if res is not None : 
        return 1 if res==X else -1
    return 0
    raise NotImplementedError


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return utility(board),None
    turn = player(board)
    act = actions(board)
    if turn == X:
        # max player
        mx = -math.inf
        op = (-1,-1)
        for move in act :
            new = result(board,move)
            temp,_ = minimax(new)
            if(mx < temp):
                mx= temp
                op=move
        return mx,op
    else:
        # min player
        mn = math.inf
        op = (-1,-1)
        for move in act:
            new = result(board,move)
            temp,_ = minimax(new)
            if(mn>temp):
                mn=temp
                op=move
        return mn,op
    raise NotImplementedError