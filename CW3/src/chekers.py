import numpy as np
import pygame
from pieces import *
from constants import *
from board import Board
from game import Game
from evaluator import basic_ev_func, push_forward_ev_func, push_to_opp_half_ev_func, \
                    group_prize_ev_func, minimax_a_b


def main():
    board = Board()
    window = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    is_running = True
    clock = pygame.time.Clock()
    game = Game(window, board)


    FPS = 5
    while is_running:
        clock.tick(FPS)

        if game.board.white_turn:
            move = minimax_a_b( game.board, 1, True, basic_ev_func)
            #move = minimax_a_b( game.board, MINIMAX_DEPTH, True, push_forward_ev_func)
            #move = minimax_a_b( game.board, MINIMAX_DEPTH, True, push_to_opp_half_ev_func)
            #move = minimax_a_b( game.board, 5, True, group_prize_ev_func)
        else:
            move = minimax_a_b( game.board, 5, False, basic_ev_func)
            #move = minimax_a_b( game.board, MINIMAX_DEPTH, False, push_forward_ev_func)
            #move = minimax_a_b( game.board, MINIMAX_DEPTH, False, push_to_opp_half_ev_func)
            #move = minimax_a_b( game.board, 5, False, group_prize_ev_func)


        #print(move)
        if move is not None:
            board.register_move(move)
            board.make_move(move)
        else:
            if board.white_turn:
                board.black_won=True
            else:
                board.white_won=True
            is_running = False
        if board.end():
            is_running = False


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                game.clicked_at(pos)

        game.update()
    print("black_won:", board.black_won )
    print("white_won:", board.white_won )

    pygame.quit()



def ai_vs_ai(black_depth=5, white_depth=5, black_ev_func=basic_ev_func, white_ev_func=basic_ev_func):
    board = Board()
    is_running = True
 
    while is_running:
        if board.white_turn:
            move = minimax_a_b( board, white_depth, not board.white_turn, white_ev_func)
        else:
            move = minimax_a_b( board, black_depth, not board.white_turn, black_ev_func)
            #move = minimax_a_b( board, 5, not board.white_turn, push_forward_ev_func)
            #move = minimax_a_b( board, 5, not board.white_turn, push_to_opp_half_ev_func)
            #move = minimax_a_b( board, 5, not board.white_turn, group_prize_ev_func)
            
        if move is not None:
            board.register_move(move)
            board.make_move(move)
        else:
            if board.white_turn:
                board.black_won=True
            else:
                board.white_won=True
            is_running = False
        if board.end():
            is_running = False
    print("black_won:", board.black_won )
    print("white_won:", board.white_won )


def ai_vs_ai_visual(white_depth, white_ev_func, black_depth, black_ev_func):
    board = Board()
    window = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    is_running = True
    clock = pygame.time.Clock()
    game = Game(window, board)
    while is_running:
        clock.tick(FPS)
        if board.white_turn:
            move = minimax_a_b( board, white_depth, not board.white_turn, white_ev_func)
        else:
            move = minimax_a_b( board, black_depth, not board.white_turn, black_ev_func)
            #move = minimax_a_b( board, black_depth, not board.white_turn, push_forward_ev_func)
            #move = minimax_a_b( board, black_depth, not board.white_turn, push_to_opp_half_ev_func)
            #move = minimax_a_b( board, black_depth, not board.white_turn, group_prize_ev_func)
            
        if move is not None:
            board.register_move(move)
            board.make_move(move)
        else:
            if board.white_turn:
                board.black_won=True
            else:
                board.white_won=True
            is_running = False
        if board.end():
            is_running = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False
        game.update()
        #input()

    print("black_won:", board.black_won )
    print("white_won:", board.white_won )
    if board.black_won and board.white_won:
        return 0
    if board.black_won:
        return -1
    if board.white_won:
        return 1
    pygame.quit()

if __name__ == "__main__":
    #main()

    # for i in range(1, 6):
        # print("depth:", i)
        # ai_vs_ai(i, i, basic_ev_func, basic_ev_func)
        #ai_vs_ai(i, i, push_forward_ev_func, push_forward_ev_func)
        #ai_vs_ai(i, i, push_to_opp_half_ev_func, push_to_opp_half_ev_func)
        #ai_vs_ai(i, i, group_prize_ev_func, group_prize_ev_func)
    iter = [basic_ev_func, push_forward_ev_func, push_to_opp_half_ev_func, group_prize_ev_func]
    for ev1 in iter:
        for ev2 in iter:
            print(ev1.__name__, ev2.__name__)
            white_won = 0
            draws = 0
            black_won = 0
            for i in range(1, 6):
                result = ai_vs_ai_visual(4, ev1, 4, ev2)
                if result == 1:
                    white_won += 1
                elif result == -1:
                    black_won += 1
                else:
                    draws += 1
            print("white_won:", white_won)
            print("draws:", draws)
            print("black_won:", black_won)
            #ai_vs_ai_visual(4, basic_ev_func, 4, push_forward_ev_func)