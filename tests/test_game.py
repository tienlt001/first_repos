import pytest
from tic_tac_toe.game import Board, Game
from tic_tac_toe.ai import best_move


def test_make_move_and_win():
    b = Board()
    assert b.make_move(0, "X")
    assert b.make_move(1, "X")
    assert b.make_move(2, "X")
    assert b.is_winner("X")


def test_draw():
    b = Board()
    # Fill to a draw
    moves = [0,1,2,4,3,5,7,6,8]
    players = ["X","O"] * 5
    for i, m in enumerate(moves):
        b.make_move(m, players[i])
    assert b.is_draw()


def test_ai_blocks():
    b = Board()
    # Human X threatens to win at 2, AI O must block
    b.make_move(0, "X")
    b.make_move(4, "O")
    b.make_move(1, "X")
    move = best_move(b, "O")
    assert move == 2
