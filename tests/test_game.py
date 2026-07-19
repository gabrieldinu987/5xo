from game.game import Game


class TestGame:

    def test_new_game_starts_with_x(self):
        """
        Jocul nou începe cu jucătorul X.
        """

        game = Game()

        state = game.get_state()

        assert state["current_player"] == "X"

        assert state["winner"] is None

        assert state["game_over"] is False


    def test_play_places_symbol(self):
        """
        O mutare trebuie să fie salvată pe tablă.
        """

        game = Game()

        game.play(10, 10)

        state = game.get_state()

        assert state["board"][10][10] == "X"


    def test_turn_changes_after_move(self):
        """
        După o mutare, jucătorul trebuie schimbat.
        """

        game = Game()

        game.play(0, 0)

        state = game.get_state()

        assert state["current_player"] == "O"


    def test_reset_clears_board(self):
        """
        Resetarea golește tabla.
        """

        game = Game()

        game.play(5, 5)

        game.reset()

        state = game.get_state()

        for row in state["board"]:

            for cell in row:

                assert cell is None


    def test_reset_sets_current_player_to_x(self):
        """
        După reset, jocul începe din nou cu X.
        """

        game = Game()

        game.play(0, 0)

        game.reset()

        state = game.get_state()

        assert state["current_player"] == "X"


    def test_reset_clears_winner(self):
        """
        După reset nu trebuie să existe câștigător.
        """

        game = Game()

        game.reset()

        state = game.get_state()

        assert state["winner"] is None

        assert state["game_over"] is False