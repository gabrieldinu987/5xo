class Board:
    """
    Reprezintă tabla de joc.
    """

    SIZE = 50

    def __init__(self):
        self.reset()

    def reset(self):
        """
        Creează o tablă goală.
        """
        self.grid = [
            [None for _ in range(self.SIZE)]
            for _ in range(self.SIZE)
        ]

    def is_inside(self, row, col):
        """
        Verifică dacă poziția este în limitele tablei.
        """
        return (
            0 <= row < self.SIZE
            and
            0 <= col < self.SIZE
        )

    def is_empty(self, row, col):
        """
        Verifică dacă o celulă este liberă.
        """
        return self.grid[row][col] is None

    def place_symbol(self, row, col, symbol):
        """
        Plasează X sau O.
        """

        if not self.is_inside(row, col):
            raise ValueError("Poziție invalidă.")

        if not self.is_empty(row, col):
            raise ValueError("Celula este deja ocupată.")

        self.grid[row][col] = symbol