import unittest

from tic import best_move


class TicTacToeTests(unittest.TestCase):
    def test_takes_immediate_winning_move(self):
        self.assertEqual(best_move("XX OO    ", "X"), 2)

    def test_blocks_opponent_winning_move(self):
        self.assertEqual(best_move("OO  X X  ", "X"), 2)

    def test_returns_minus_one_for_full_board(self):
        self.assertEqual(best_move("XOXOOXXXO", "X"), -1)


if __name__ == "__main__":
    unittest.main()
