class WinnerChecker:

    DIRECTIONS = (
        (0, 1),    # orizontal
        (1, 0),    # vertical
        (1, 1),    # diagonala \
        (1, -1),   # diagonala /
    )

    @classmethod
    def check(cls, board, row, col):
        """
        Verifică dacă ultima mutare produce victoria.
        """

        symbol = board.grid[row][col]

        if symbol is None:
            return False

        for dr, dc in cls.DIRECTIONS:

            total = 1

            total += cls.count_direction(
                board,
                row,
                col,
                dr,
                dc,
                symbol
            )

            total += cls.count_direction(
                board,
                row,
                col,
                -dr,
                -dc,
                symbol
            )

            if total >= 5:
                return True

        return False

    @staticmethod
    def count_direction(board, row, col, dr, dc, symbol):
        """
        Numără simbolurile consecutive într-o direcție.
        """

        count = 0

        r = row + dr
        c = col + dc

        while board.is_inside(r, c):

            if board.grid[r][c] != symbol:
                break

            count += 1

            r += dr
            c += dc

        return count