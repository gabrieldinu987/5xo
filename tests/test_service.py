import pytest

from game.service import GameService


class TestGameService:

    def test_new_game_starts_with_x(self):
        """
        Jocul începe cu X.
        """

        service = GameService()

        assert service.current_player == "X"

        assert service.game_over is False

        assert service.winner is None


    def test_first_move_places_x(self):
        """
        Prima mutare trebuie să fie X.
        """

        service = GameService()

        service.play(10, 10)

        assert service.board.grid[10][10] == "X"


    def test_player_switches_after_first_move(self):
        """
        După prima mutare urmează O.
        """

        service = GameService()

        service.play(10, 10)

        assert service.current_player == "O"


    def test_player_switches_back_to_x(self):
        """
        După două mutări urmează din nou X.
        """

        service = GameService()

        service.play(10, 10)

        service.play(10, 11)

        assert service.current_player == "X"


    def test_cannot_play_on_same_cell(self):
        """
        Nu putem juca pe aceeași celulă.
        """

        service = GameService()

        service.play(5, 5)

        with pytest.raises(ValueError):

            service.play(5, 5)


    def test_reset_restores_initial_state(self):
        """
        Resetarea revine la starea inițială.
        """

        service = GameService()

        service.play(1, 1)

        service.play(2, 2)

        service.reset()

        assert service.current_player == "X"

        assert service.game_over is False

        assert service.winner is None

        for row in service.board.grid:

            for cell in row:

                assert cell is None


    def test_horizontal_win(self):
        """
        X câștigă pe orizontală.
        """

        service = GameService()

        service.play(10, 0)   # X
        service.play(0, 0)    # O

        service.play(10, 1)   # X
        service.play(0, 1)    # O

        service.play(10, 2)
        service.play(0, 2)

        service.play(10, 3)
        service.play(0, 3)

        service.play(10, 4)

        assert service.game_over is True

        assert service.winner == "X"


    def test_no_move_after_game_finished(self):
        """
        După victorie nu se mai poate juca.
        """

        service = GameService()

        service.play(10, 0)
        service.play(0, 0)

        service.play(10, 1)
        service.play(0, 1)

        service.play(10, 2)
        service.play(0, 2)

        service.play(10, 3)
        service.play(0, 3)

        service.play(10, 4)

        with pytest.raises(ValueError):

            service.play(20, 20)


    def test_get_state_returns_dictionary(self):
        """
        get_state trebuie să întoarcă un dicționar.
        """

        service = GameService()

        state = service.get_state()

        assert isinstance(state, dict)

        assert "board" in state

        assert "current_player" in state

        assert "winner" in state

        assert "game_over" in state