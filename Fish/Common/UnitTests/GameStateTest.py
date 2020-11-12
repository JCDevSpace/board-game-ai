import unittest

from Common.state import GameState
from Common.board import Board

class TestGameStateGetGameState(unittest.TestCase):
    def test_no_change_state(self):
        b = Board(3, 3, [[1, 2, 0], [0, 2, 5], [0, 0, 4]])
        player1 = 'red'
        player2 = 'brown'
        gs = GameState(b, [player1, player2])
        board_list = [[1, 2, 0], [0, 2, 5], [0, 0, 4]]
        players_in_order = ['red', 'brown']
        player_penguins = {player1: [], player2: []}
        turn = 0
        scores = {player1: 0, player2: 0}
        self.assertEqual(gs.get_game_state(), (board_list, players_in_order, player_penguins, turn, scores))

    def test_after_adding_penguin(self):
        b = Board(3, 3, [[1, 2, 3], [0, 2, 5], [0, 0, 4]])
        player1 = 'red'
        player2 = 'brown'
        gs = GameState(b, [player1, player2])

        gs.place_penguin(player1, (0, 0))

        board_list = [[1, 2, 3], [0, 2, 5], [0, 0, 4]]
        players_in_order = ['red', 'brown']
        player_penguins = {player1: [(0, 0)], player2: []}
        turn = 1
        scores = {player1: 0, player2: 0}

        self.assertEqual(gs.get_game_state(), (board_list, players_in_order, player_penguins, turn, scores))

    def test_after_move_penguin(self):
        b = Board(3, 3, [[1, 2, 0], [0, 2, 5], [0, 0, 4]])
        player1 = 'red'
        player2 = 'brown'
        gs = GameState(b, [player1, player2])

        gs.place_penguin(player1, (0, 1))
        gs.place_penguin(player2, (2, 2))
        gs.move_penguin(player1, (0, 1), (1, 1))

        board_list = [[1, 0, 0], [0, 2, 5], [0, 0, 4]]
        players_in_order = ['red', 'brown']
        player_penguins = {player1: [(1, 1)], player2: [(2, 2)]}
        turn = 1
        scores = {player1: 2, player2: 0}
        self.assertEqual(gs.get_game_state(), (board_list, players_in_order, player_penguins, turn, scores))


class TestGameStateCurrentPlayer(unittest.TestCase):

    def test_get_current_player_in_order(self):
        b = Board(3, 3, [[1, 2, 0], [-1, 2, 5], [-1, -1, 4]])
        player1 = 'red'
        player2 = 'brown'
        gs = GameState(b, [player1, player2])
        self.assertEqual(player1, gs.get_current_color())

    def test_get_current_player_different_order(self):
        b = Board(3, 3, [[1, 2, 0], [-1, 2, 5], [-1, -1, 4]])
        player1 = 'red'
        player2 = 'brown'
        gs = GameState(b, [player2, player1])
        self.assertEqual(player2, gs.get_current_color())


class TestGameStatePlacePenguin(unittest.TestCase):

    def test_place_regular(self):
        b = Board(3, 3, [[1, 2, 1], [0, 2, 5], [0, 0, 4]])
        player1 = 'red'
        player2 = 'brown'
        gs = GameState(b, [player1, player2])

        self.assertEqual([[1, 2, 1], [0, 2, 5], [0, 0, 4]], gs.get_game_state()[0])
        self.assertEqual({player1: [], player2: []}, gs.get_game_state()[2])
        self.assertEqual({player1: 0, player2: 0}, gs.get_game_state()[4])

        gs.place_penguin(player1, (1, 1))

        self.assertEqual([[1, 2, 1], [0, 2, 5], [0, 0, 4]], gs.get_game_state()[0])
        self.assertEqual({player1: [(1, 1)], player2: []}, gs.get_game_state()[2])
        self.assertEqual({player1: 0, player2: 0}, gs.get_game_state()[4])

    def test_place_out_of_bounds(self):
        b = Board(3, 3, [[1, 2, 1], [0, 2, 5], [0, 0, 4]])
        player1 = 'red'
        player2 = 'brown'
        gs = GameState(b, [player1, player2])

        self.assertEqual([[1, 2, 1], [0, 2, 5], [0, 0, 4]], gs.get_game_state()[0])
        self.assertEqual({player1: [], player2: []}, gs.get_game_state()[2])

        with self.assertRaises(ValueError):
            gs.place_penguin(player1, (-1, 1))

    def test_place_on_hole(self):
        b = Board(3, 3, [[1, 2, 0], [-1, 2, 5], [-1, -1, 4]])
        player1 = 'red'
        player2 = 'brown'
        gs = GameState(b, [player1, player2])

        self.assertEqual([[1, 2, 0], [-1, 2, 5], [-1, -1, 4]], gs.get_game_state()[0])
        self.assertEqual({player1: [], player2: []}, gs.get_game_state()[2])

        with self.assertRaises(ValueError):
            gs.place_penguin(player1, (1, 0))

    def test_place_on_penguin(self):
        b = Board(3, 3, [[1, 2, 0], [-1, 2, 5], [-1, -1, 4]])
        player1 = 'red'
        player2 = 'brown'
        gs = GameState(b, [player1, player2])

        self.assertEqual([[1, 2, 0], [-1, 2, 5], [-1, -1, 4]], gs.get_game_state()[0])
        self.assertEqual({player1: [], player2: []}, gs.get_game_state()[2])

        with self.assertRaises(ValueError):
            gs.place_penguin(player1, (0, 2))


class TestGameStateMovePenguin(unittest.TestCase):

    def test_move_penguin_valid(self):
        b = Board(3, 3, [[1, 2, 1], [0, 2, 5], [0, 0, 4]])
        player1 = 'red'
        player2 = 'brown'
        gs = GameState(b, [player1, player2])
        gs.place_penguin(player1, (1, 1))
        self.assertEqual([[1, 2, 1], [0, 2, 5], [0, 0, 4]], gs.get_game_state()[0])
        self.assertEqual({player1: [(1, 1)], player2: []}, gs.get_game_state()[2])
        self.assertEqual(1, gs.get_game_state()[3])
        self.assertEqual({player1: 0, player2: 0}, gs.get_game_state()[4])
        gs.place_penguin(player2, (2, 2))
        gs.move_penguin(player1, (1, 1), (0, 1))

        self.assertEqual([[1, 2, 1], [0, 0, 5], [0, 0, 4]], gs.get_game_state()[0])
        self.assertEqual({player1: [(0, 1)], player2: [(2, 2)]}, gs.get_game_state()[2])
        self.assertEqual(1, gs.get_game_state()[3])
        self.assertEqual({player1: 2, player2: 0}, gs.get_game_state()[4])

    def test_move_penguin_not_valid_movement(self):
        b = Board(3, 3, [[1, 2, 1], [0, 2, 5], [0, 0, 4]])
        player1 = 'red'
        player2 = 'brown'
        gs = GameState(b, [player1, player2])
        gs.place_penguin(player1, (1, 1))
        self.assertEqual([[1, 2, 1], [0, 2, 5], [0, 0, 4]], gs.get_game_state()[0])
        self.assertEqual({player1: [(1, 1)], player2: []}, gs.get_game_state()[2])

        with self.assertRaises(ValueError):
            gs.move_penguin(player1, (1, 1), (0, 0))

    def test_move_penguin_into_hole(self):
        b = Board(3, 3, [[1, 2, 1], [0, 2, 5], [0, 0, 4]])
        player1 = 'red'
        player2 = 'brown'
        gs = GameState(b, [player1, player2])
        gs.place_penguin(player1, (1, 1))
        self.assertEqual([[1, 2, 1], [0, 2, 5], [0, 0, 4]], gs.get_game_state()[0])
        self.assertEqual({player1: [(1, 1)], player2: []}, gs.get_game_state()[2])

        with self.assertRaises(ValueError):
            gs.move_penguin(player1, (1, 1), (2, 1))

    def test_move_penguin_into_penguin(self):
        b = Board(3, 3, [[1, 2, 1], [0, 2, 5], [0, 0, 4]])
        player1 = 'red'
        player2 = 'brown'
        gs = GameState(b, [player1, player2])
        gs.place_penguin(player1, (1, 1))
        gs.place_penguin(player2, (0, 2))
        self.assertEqual([[1, 2, 1], [0, 2, 5], [0, 0, 4]], gs.get_game_state()[0])
        self.assertEqual({player1: [(1, 1)], player2: [(0, 2)]}, gs.get_game_state()[2])

        with self.assertRaises(ValueError):
            gs.move_penguin(player1, (1, 1), (0, 2))

    def test_move_penguin_wrong_turn(self):
        b = Board(3, 3, [[1, 2, 1], [0, 2, 5], [0, 0, 4]])
        player1 = 'red'
        player2 = 'brown'
        gs = GameState(b, [player1, player2])
        gs.place_penguin(player1, (0, 2))
        gs.place_penguin(player2, (1, 1))
        previous_game_state = gs.get_game_state()

        with self.assertRaises(ValueError):
            gs.move_penguin(player2, (1, 1), (0, 1))

        self.assertEqual(previous_game_state, gs.get_game_state())


class TestGameStateIncrementTurn(unittest.TestCase):
    def test_increment_turn(self):
        b = Board(3, 3, [[1, 2, 0], [-1, 2, 5], [-1, -1, 4]])
        player1 = 'red'
        player2 = 'brown'
        gs = GameState(b, [player1, player2])

        self.assertEqual(0, gs.get_game_state()[3])
        gs.increment_turn()
        self.assertEqual(1, gs.get_game_state()[3])
        gs.increment_turn()
        self.assertEqual(0, gs.get_game_state()[3])
        gs.increment_turn()
        self.assertEqual(1, gs.get_game_state()[3])
        gs.increment_turn()



class TestGameStateGameOver(unittest.TestCase):
    def test_game_over_false(self):
        b = Board(3, 3, [[1, 2, 1], [0, 2, 5], [0, 0, 4]])
        player1 = 'red'
        player2 = 'brown'
        gs = GameState(b, [player1, player2])
        gs.place_penguin(player1, (1, 1))
        self.assertEqual([[1, 2, 1], [0, 2, 5], [0, 0, 4]], gs.get_game_state()[0])
        self.assertEqual({player1: [(1, 1)], player2: []}, gs.get_game_state()[2])
        self.assertFalse(gs.game_over())

    def test_game_over_one_penguin_cannot(self):
        """
        1   2   0      1    2   0
          -1  2  5  ->    0   0  5     (2, 2) bottom right has no valid moves
        0  -1  4      0   0   4
        """
        b = Board(3, 3, [[1, 2, 0], [0, 2, 5], [0, 0, 4]])
        player1 = "red"
        player2 = "brown"
        gs = GameState(b, [player2, player1])
        gs.place_penguin(player2, (1, 2))
        gs.place_penguin(player1, (1, 1))
        gs.place_penguin(player2, (2, 2))
        self.assertEqual([[1, 2, 0], [0, 2, 5], [0, 0, 4]], gs.get_game_state()[0])
        self.assertEqual({player1: [(1, 1)], player2: [(1, 2), (2, 2)]}, gs.get_game_state()[2])
        self.assertFalse(gs.has_moves_left(player2))
        self.assertFalse(gs.game_over())

    def test_game_over_true(self):
        """
        0   0   0     0  0   0
          0  2  0  ->   0   2    0     (1, 1) center has no valid moves
        0  0  0      0   0   0            and since its the only penguin, game is over
        """
        b = Board(3, 3, [[0, 0, 0], [0, 2, 0], [0, 0, 0]])
        player1 = 'red'
        player2 = 'brown'
        gs = GameState(b, [player1, player2])
        gs.place_penguin(player1, (1, 1))
        self.assertEqual([[0, 0, 0], [0, 2, 0], [0, 0, 0]], gs.get_game_state()[0])
        self.assertEqual({player1: [(1, 1)], player2: []}, gs.get_game_state()[2])
        self.assertTrue(gs.game_over())


class TestGameStateHasMovesLeft(unittest.TestCase):
    def test_has_moves_left_false(self):
        """
               1   2   0      1    2   0
                 0  2  0  ->    0   2   0     (2, 2) bottom right has no valid moves
               0  0  4      0   0   4
               """
        b = Board(3, 3, [[1, 2, 0], [0, 2, 0], [0, 0, 4]])
        player1 = 'red'
        player2 = 'brown'
        gs = GameState(b, [player1, player2])
        gs.place_penguin(player1, (1, 1))
        gs.place_penguin(player2, (2, 2))
        self.assertEqual([[1, 2, 0], [0, 2, 0], [0, 0, 4]], gs.get_game_state()[0])
        self.assertEqual({player1: [(1, 1)], player2: [(2, 2)]}, gs.get_game_state()[2])
        self.assertFalse(gs.has_moves_left(player2))

    def test_has_moves_left_true(self):
        """
               1   2   0      1    2   0
                 0  2  0  ->   0   2    0     (1, 1) center has valid moves (0, 1)
               0  0  4      0  0   4
               """
        b = Board(3, 3, [[1, 2, 0], [0, 2, 0], [0, 0, 4]])
        player1 = 'red'
        player2 = 'brown'
        gs = GameState(b, [player1, player2])
        gs.place_penguin(player1, (1, 1))
        gs.place_penguin(player2, (2, 2))
        self.assertEqual([[1, 2, 0], [0, 2, 0], [0, 0, 4]], gs.get_game_state()[0])
        self.assertEqual({player1: [(1, 1)], player2: [(2, 2)]}, gs.get_game_state()[2])
        self.assertTrue(gs.has_moves_left(player1))

class TestGameStateValidMovesForCurrPlayer(unittest.TestCase):

    def test_has_moves(self):
        """
           1   2  0
              0  2  0       (1, 1) center has valid moves (0, 1)
           0  0  4
           """
        b = Board(3, 3, [[1, 2, 0], [0, 2, 0], [0, 0, 4]])
        player1 = 'red'
        player2 = 'brown'
        gs = GameState(b, [player1, player2])
        gs.place_penguin(player1, (1, 1))
        gs.place_penguin(player2, (2, 2))
        self.assertEqual([[1, 2, 0], [0, 2, 0], [0, 0, 4]], gs.get_game_state()[0])
        self.assertEqual({player1: [(1, 1)], player2: [(2, 2)]}, gs.get_game_state()[2])
        moves = [(player1, (1, 1), (0, 1))]
        self.assertEqual(moves, gs.get_current_player_valid_moves())


    def test_no_moves(self):
        """
           1   2  0
              0  2  0  ->       (1, 1) center has valid moves (0, 1)
           0  0  0
           """
        b = Board(3, 3, [[1, 2, 0], [0, 2, 0], [0, 0, 4]])
        player1 = 'red'
        player2 = 'brown'
        gs = GameState(b, [player1, player2])
        gs.place_penguin(player1, (1, 1))
        gs.place_penguin(player2, (2, 2))
        self.assertEqual([[1, 2, 0], [0, 2, 0], [0, 0, 4]], gs.get_game_state()[0])
        self.assertEqual({player1: [(1, 1)], player2: [(2, 2)]}, gs.get_game_state()[2])
        gs.increment_turn() # set turn to player2's
        moves = [(player2, False)]
        self.assertEqual(moves, gs.get_current_player_valid_moves())


if __name__ == '__main__':
    unittest.main()
