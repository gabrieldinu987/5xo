from game.board import Board
from game.winner import WinnerChecker


class TestWinnerChecker:

    def test_no_winner_on_empty_board(self):
        """
        Tabla goală nu are câștigător.
        """

        board = Board()

        assert WinnerChecker.check(board, 0, 0) is False


    def test_horizontal_win(self):
        """
        Cinci simboluri pe orizontală.
        """

        board = Board()

        for col in range(5):
            board.place_symbol(10, col, "X")

        assert WinnerChecker.check(board, 10, 4)


    def test_vertical_win(self):
        """
        Cinci simboluri pe verticală.
        """

        board = Board()

        for row in range(5):
            board.place_symbol(row, 20, "O")

        assert WinnerChecker.check(board, 4, 20)


    def test_main_diagonal_win(self):
        """
        Diagonala principală.
        """

        board = Board()

        for i in range(5):
            board.place_symbol(i, i, "X")

        assert WinnerChecker.check(board, 4, 4)


    def test_secondary_diagonal_win(self):
        """
        Diagonala secundară.
        """

        board = Board()

        for i in range(5):
            board.place_symbol(i, 10 - i, "O")

        assert WinnerChecker.check(board, 4, 6)


    def test_four_horizontal_is_not_win(self):
        """
        Patru simboluri nu sunt suficiente.
        """

        board = Board()

        for col in range(4):
            board.place_symbol(15, col, "X")

        assert WinnerChecker.check(board, 15, 3) is False


    def test_four_vertical_is_not_win(self):
        """
        Patru simboluri pe verticală.
        """

        board = Board()

        for row in range(4):
            board.place_symbol(row, 12, "O")

        assert WinnerChecker.check(board, 3, 12) is False


    def test_six_horizontal_is_win(self):
        """
        Șase simboluri consecutive.
        """

        board = Board()

        for col in range(6):
            board.place_symbol(30, col, "X")

        assert WinnerChecker.check(board, 30, 5)


    def test_broken_horizontal_line(self):
        """
        Linia întreruptă nu produce victorie.
        """

        board = Board()

        board.place_symbol(10, 0, "X")
        board.place_symbol(10, 1, "X")
        board.place_symbol(10, 2, "X")
        board.place_symbol(10, 3, "O")
        board.place_symbol(10, 4, "X")

        assert WinnerChecker.check(board, 10, 4) is False


    def test_horizontal_win_at_left_edge(self):
        """
        Victorie la marginea stângă.
        """

        board = Board()

        for col in range(5):
            board.place_symbol(0, col, "X")

        assert WinnerChecker.check(board, 0, 4)


    def test_vertical_win_at_top_edge(self):
        """
        Victorie la marginea superioară.
        """

        board = Board()

        for row in range(5):
            board.place_symbol(row, 0, "O")

        assert WinnerChecker.check(board, 4, 0)


    def test_horizontal_win_at_right_edge(self):
        """
        Victorie la marginea dreaptă.
        """

        board = Board()

        for col in range(45, 50):
            board.place_symbol(20, col, "X")

        assert WinnerChecker.check(board, 20, 49)


    def test_vertical_win_at_bottom_edge(self):
        """
        Victorie la marginea inferioară.
        """

        board = Board()

        for row in range(45, 50):
            board.place_symbol(row, 25, "O")

        assert WinnerChecker.check(board, 49, 25)


    def test_last_move_completes_line(self):
        """
        Ultima mutare completează cele cinci simboluri.
        """

        board = Board()

        for col in range(4):
            board.place_symbol(12, col, "X")

        board.place_symbol(12, 4, "X")

        assert WinnerChecker.check(board, 12, 4)


    def test_single_symbol_is_not_win(self):
        """
        Un singur simbol nu produce victorie.
        """

        board = Board()

        board.place_symbol(25, 25, "X")

        assert WinnerChecker.check(board, 25, 25) is False