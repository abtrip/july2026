"""Tic Tac Toe move selection using a minimax search."""

from functools import lru_cache

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


def _winner(board: str):
    """Return the winner token, draw marker, or None for an unfinished game."""
    for a, b, c in WIN_LINES:
        token = board[a]
        if token != " " and token == board[b] and token == board[c]:
            return token
    if " " not in board:
        return "D"
    return None


@lru_cache(maxsize=None)
def _solve(board: str, player: str) -> int:
    """Score a position for the current player: win=1, draw=0, loss=-1."""
    result = _winner(board)
    if result == "D":
        return 0
    if result is not None:
        return -1

    opponent = "O" if player == "X" else "X"
    best_score = -2
    for idx, token in enumerate(board):
        if token == " ":
            next_board = board[:idx] + player + board[idx + 1 :]
            score = -_solve(next_board, opponent)
            if score > best_score:
                best_score = score
                if best_score == 1:
                    break
    return 0 if best_score == -2 else best_score


def best_move(board: str, player: str) -> int:
    """Return the best move index for player, or -1 when no moves are available."""
    if len(board) != 9:
        raise ValueError("Board must be a 9-character string")
    if player not in {"X", "O"}:
        raise ValueError("Player must be 'X' or 'O'")

    opponent = "O" if player == "X" else "X"
    best_idx = -1
    best_score = -2

    for idx, token in enumerate(board):
        if token == " ":
            next_board = board[:idx] + player + board[idx + 1 :]
            score = -_solve(next_board, opponent)
            if score > best_score:
                best_score = score
                best_idx = idx

    return best_idx
