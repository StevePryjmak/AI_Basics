import numpy as np
import random
from constants import *
from copy import deepcopy

def basic_ev_func(board, is_black_turn):
    h=0
    for row in range(len(board.board)):
        for col in range(len(board.board[row])):
            piece = board.board[row][col]
            if piece is not None:
                if piece.is_black():
                    if piece.is_king():
                        h -= 10
                    else:
                        h -= 1
                elif piece.is_white():
                    if piece.is_king():
                        h += 10
                    else:
                        h += 1   
    return h   


def get_neighbors(row, col):
    neighbors = [[row+1, col+1], [row+1, col-1], [row-1, col+1], [row-1, col-1]]
    return [[r, c] for r, c in neighbors if r >= 0 and r < BOARD_HEIGHT and c >= 0 and c < BOARD_WIDTH]

#nagrody jak w wersji podstawowej + nagroda za stopieĹ zwartoĹci grupy        
def group_prize_ev_func(board, is_black_turn):
    h=basic_ev_func(board, is_black_turn)
    for row in range(len(board.board)):
        for col in range(len(board.board[row])):
            piece = board.board[row][col]
            neighbors = get_neighbors(row, col)
            for row, col in neighbors:
                piece_neigh = board.board[row][col]
                if piece_neigh.is_black() == piece.is_black():
                    h += 0.5
                elif piece_neigh.is_white() == piece.is_white():
                    h -= 0.5
            if piece.is_black():
                h -= 4-len(neighbors)
            elif piece.is_white():
                h += 4-len(neighbors)
    return h         

#za kaĹźdy pion na wĹasnej poĹowie planszy otrzymuje siÄ 5 nagrody, na poĹowie przeciwnika 7, a za kaĹźdÄ damkÄ 10.
def push_to_opp_half_ev_func(board, is_black_turn):
    h=0
    for row in range(len(board.board)):
        for col in range(len(board.board[row])):
            piece = board.board[row][col]
            if piece is not None:
                if piece.is_black():
                    if piece.is_king():
                        h -= 10
                    else:
                        h -= 5 if row <= 3 else 7
                elif piece.is_white():
                    if piece.is_king():
                        h += 10
                    else:
                        h += 5 if row >= 4 else 7
    return h              


#za kaĹźdy nasz pion otrzymuje siÄ nagrodÄ w wysokoĹci: (5 + numer wiersza, na ktĂłrym stoi pion) (im jest bliĹźej wroga tym lepiej), a za kaĹźdÄ damkÄ dodtakowe: 10. 
def push_forward_ev_func(board, is_black_turn):
    h=0
    for row in range(len(board.board)):
        for col in range(len(board.board[row])):
            piece = board.board[row][col]
            if piece is not None:
                if piece.is_black():
                    if piece.is_king():
                        h -= 10
                    h -= 5 + row
                elif piece.is_white():
                    if piece.is_king():
                        h += 10
                    h += 5 + (BOARD_HEIGHT-1-row)
    return h              

#f. called from main    
def minimax_a_b(board, depth, plays_as_black, ev_func):
    possible_moves = board.get_possible_moves(plays_as_black)
    if len(possible_moves)==0:
        board.white_won = plays_as_black
        board.is_running=False
        return None
        
    a = -np.inf
    b = np.inf
    moves_marks = []
    for possible_move in possible_moves:
        new_board = deepcopy(board)
        new_board.make_move(possible_move)
        eval = minimax_a_b_recurr(new_board, depth -1, plays_as_black, a, b, ev_func)
        moves_marks.append(eval)
        if not plays_as_black:
            a = max(a, eval)
        else:
            b = min(b, eval)
    target = min(moves_marks) if plays_as_black else max(moves_marks)
    heights_mark_moves = [move for move, eval in zip(possible_moves, moves_marks) if eval == target]

    return random.choice(heights_mark_moves)

#recursive function, called from minimax_a_b
def minimax_a_b_recurr(board, depth, move_max, a, b, ev_func):
    possible_moves = board.get_possible_moves(not move_max)
    if board.end(): 
        if board.white_won:
            return WON_PRIZE
        elif board.black_won:
            return -WON_PRIZE
        else:
            return 0
    if len(possible_moves) == 0:
        return -WON_PRIZE if move_max else WON_PRIZE
        
    if depth == 0:
        return ev_func(board, move_max)
    
    
    if move_max:
        max_eval = -np.inf
        for move in possible_moves:
            new_board = deepcopy(board)
            new_board.make_move(move)
            eval = minimax_a_b_recurr(new_board, depth - 1, False, a, b, ev_func)
            max_eval = max(max_eval, eval)
            a = max(a, eval)
            if b <= a:
                break
            #print(f"max: {max_eval} a: {a}  b: {b} move: {move}")
        return max_eval
    else:
        min_eval = np.inf
        for move in possible_moves:
            new_board = deepcopy(board)
            new_board.make_move(move)
            eval = minimax_a_b_recurr(new_board, depth - 1, True, a, b, ev_func)
            min_eval = min(min_eval, eval)
            b = min(b, eval)
            if b <= a:
                break
            #print(f"min: {min_eval} a: {a}  b: {b} move: {move}")
        return min_eval
    
