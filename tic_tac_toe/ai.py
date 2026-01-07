"""Simple minimax-based AI for Tic-Tac-Toe."""
from typing import Tuple
from .game import Board


def score_for(board: Board, ai_player: str, depth: int) -> int:
    human = "O" if ai_player == "X" else "X"
    if board.is_winner(ai_player):
        return 10 - depth
    if board.is_winner(human):
        return depth - 10
    return 0


def minimax(board: Board, player: str, ai_player: str, depth: int = 0) -> Tuple[int, int]:
    """Returns (best_score, best_move_index)."""
    if board.is_winner(ai_player) or board.is_winner("O" if ai_player == "X" else "X") or board.is_draw():
        return score_for(board, ai_player, depth), -1

    best_move = -1
    if player == ai_player:
        best_score = -999
        for m in board.available_moves():
            newb = board.clone()
            newb.make_move(m, player)
            score, _ = minimax(newb, "O" if player == "X" else "X", ai_player, depth + 1)
            if score > best_score:
                best_score = score
                best_move = m
    else:
        best_score = 999
        for m in board.available_moves():
            newb = board.clone()
            newb.make_move(m, player)
            score, _ = minimax(newb, "O" if player == "X" else "X", ai_player, depth + 1)
            if score < best_score:
                best_score = score
                best_move = m

    return best_score, best_move


def best_move(board: Board, ai_player: str) -> int:
    _, move = minimax(board, ai_player, ai_player)
    return move
