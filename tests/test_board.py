import pytest

from game.board import Board


class TestBoard:

    def test_board_size(self):
        """
        Tabla trebuie să fie 50x50.
        """

        board = Board()

        assert len(board.grid) == 50

        assert len(board.grid[0]) == 50


    def test_new_board_is_empty(self):
        """
        Toate celulele trebuie să fie goale.
        """

        board = Board()

        for row in board.grid:

            for cell in row:

                assert cell is None


    def test_place_x_symbol(self):
        """
        Se poate plasa X.
        """

        board = Board()

        board.place_symbol(10, 15, "X")

        assert board.grid[10][15] == "X"


    def test_place_o_symbol(self):
        """
        Se poate plasa O.
        """

        board = Board()

        board.place_symbol(25, 40, "O")

        assert board.grid[25][40] == "O"


    def test_cell_is_not_empty_after_move(self):
        """
        Celula nu mai este goală după mutare.
        """

        board = Board()

        board.place_symbol(5, 5, "X")

        assert board.is_empty(5, 5) is False


    def test_reset_board(self):
        """
        Resetarea golește tabla.
        """

        board = Board()

        board.place_symbol(1, 1, "X")

        board.place_symbol(2, 2, "O")

        board.reset()

        for row in board.grid:

            for cell in row:

                assert cell is None


    def test_inside_returns_true(self):
        """
        Coordonate valide.
        """

        board = Board()

        assert board.is_inside(0, 0)

        assert board.is_inside(49, 49)

        assert board.is_inside(20, 35)


    def test_inside_returns_false(self):
        """
        Coordonate invalide.
        """

        board = Board()

        assert board.is_inside(-1, 0) is False

        assert board.is_inside(0, -1) is False

        assert board.is_inside(50, 0) is False

        assert board.is_inside(0, 50) is False


    def test_place_symbol_negative_row(self):
        """
        Linie negativă.
        """

        board = Board()

        with pytest.raises(ValueError):

            board.place_symbol(-1, 10, "X")


    def test_place_symbol_negative_column(self):
        """
        Coloană negativă.
        """

        board = Board()

        with pytest.raises(ValueError):

            board.place_symbol(10, -1, "X")


    def test_place_symbol_row_outside_board(self):
        """
        Linie prea mare.
        """

        board = Board()

        with pytest.raises(ValueError):

            board.place_symbol(50, 10, "X")


    def test_place_symbol_column_outside_board(self):
        """
        Coloană prea mare.
        """

        board = Board()

        with pytest.raises(ValueError):

            board.place_symbol(10, 50, "X")


    def test_place_symbol_twice(self):
        """
        Nu se poate suprascrie o mutare.
        """

        board = Board()

        board.place_symbol(10, 10, "X")

        with pytest.raises(ValueError):

            board.place_symbol(10, 10, "O")