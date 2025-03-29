from pytest import approx

from glicko.glicko import update_all_players
from glicko.models import Match
from glicko.models import PlayerRating


class TestUpdateAllPlayers:

    # Testing with the example data and solution given in the paper
    def test_example_from_paper(self):
        # Arrange
        player_ratings = {
            "player0": PlayerRating(1500, 200),
            "player1": PlayerRating(1400, 30),
            "player2": PlayerRating(1550, 100),
            "player3": PlayerRating(1700, 300),
        }
        match_results = [
            Match("player0", "player1", "2-1"),
            Match("player0", "player2", "1-3"),
            Match("player3", "player0", "4-2"),
        ]

        # Act
        updated_ratings = update_all_players(player_ratings, match_results)

        # Assert
        assert len(updated_ratings) == 4
        assert "player0" in updated_ratings
        assert "player1" in updated_ratings
        assert "player2" in updated_ratings
        assert "player3" in updated_ratings

        # Verify ratings have changed
        assert updated_ratings["player0"].rating != player_ratings["player0"].rating
        assert updated_ratings["player1"].rating != player_ratings["player1"].rating
        assert updated_ratings["player2"].rating != player_ratings["player2"].rating
        assert updated_ratings["player3"].rating != player_ratings["player3"].rating

        # Verify the result of the calculations is within +- 0.2 from the values in the paper
        assert updated_ratings["player0"].rating == approx(1464, abs=0.2)
        assert updated_ratings["player0"].rd == approx(151.4, abs=0.2)
