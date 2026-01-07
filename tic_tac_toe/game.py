"""Core Tic-Tac-Toe game logic."""
from typing import List, Optional

WIN_LINES = (
    (0, 1, 2),
    (3, 4, 5),
    (6, 7, 8),
    (0, 3, 6),
    (1, 4, 7),
    (2, 5, 8),
    (0, 4, 8),
    (2, 4, 6),
)


class Board:
    def __init__(self):
        self.cells: List[str] = [" "] * 9

    def reset(self) -> None:
        self.cells = [" "] * 9

    def make_move(self, index: int, player: str) -> bool:
        """Place player's mark ('X' or 'O') at index 0-8. Returns True if move succeeded."""
        if 0 <= index < 9 and self.cells[index] == " ":
            self.cells[index] = player
            return True
        return False

    def available_moves(self) -> List[int]:
        return [i for i, v in enumerate(self.cells) if v == " "]

    def is_winner(self, player: str) -> bool:
        return any(all(self.cells[i] == player for i in line) for line in WIN_LINES)

    def is_full(self) -> bool:
        return all(c != " " for c in self.cells)

    def is_draw(self) -> bool:
        return self.is_full() and not (self.is_winner("X") or self.is_winner("O"))

    def clone(self) -> "Board":
        b = Board()
        b.cells = self.cells.copy()
        return b

    def __str__(self) -> str:
        rows = []
        for r in range(3):
            row = " | ".join(self.cells[r * 3 : r * 3 + 3])
            rows.append(row)
        return "\n---------\n".join(rows)


class Game:
    def __init__(self, board: Optional[Board] = None):
        self.board = board or Board()
        self.current = "X"

    def play_move(self, index: int) -> bool:
        ok = self.board.make_move(index, self.current)
        if ok:
            self.current = "O" if self.current == "X" else "X"
        return ok

    def finished(self) -> bool:
        return self.board.is_winner("X") or self.board.is_winner("O") or self.board.is_draw()
