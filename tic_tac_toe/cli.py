"""Command-line interface for Tic-Tac-Toe."""
from .game import Game, Board
from .ai import best_move


def prompt_move(board: Board) -> int:
    moves = board.available_moves()
    while True:
        s = input(f"Enter move (0-8). Available: {moves}: ")
        try:
            idx = int(s)
            if idx in moves:
                return idx
        except ValueError:
            pass
        print("Invalid move, try again.")


def main():
    print("Tic-Tac-Toe")
    mode = input("Choose mode: 1) Two players  2) Play vs AI: ").strip()
    ai_enabled = mode == "2"
    ai_player = "O" if input("Do you want to play as X or O? (X/O): ").strip().upper() == "X" else "X"
    if ai_enabled:
        human_player = "O" if ai_player == "X" else "X"
    game = Game()

    while not game.finished():
        print(game.board)
        if ai_enabled and game.current == ai_player:
            m = best_move(game.board, ai_player)
            print(f"AI ({ai_player}) chooses {m}")
            game.play_move(m)
        else:
            m = prompt_move(game.board)
            game.play_move(m)

    print(game.board)
    if game.board.is_winner("X"):
        print("X wins!")
    elif game.board.is_winner("O"):
        print("O wins!")
    else:
        print("Draw!")


if __name__ == "__main__":
    main()
