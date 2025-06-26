import re
from dataclasses import dataclass


@dataclass(frozen=True)
class Match:
    """Represents a match between two players with a specific result format.

    A Match encapsulates the details of a game between two players and its result in a
    predefined format. The result must follow the format "<integer>-<integer>", where
    the first integer represents the score of player1 and the second integer represents
    the score of player2.

    Attributes:
        player1: The name of the first player in the match.
        player2: The name of the second player in the match.
        result: The result of the match in the format "integer-integer".
    """

    player1: str
    player2: str
    result: str

    def __post_init__(self) -> None:
        # Regular expression for format: integer-dash-integer (e.g., "13-2")
        if not re.fullmatch(r"\d+-\d+", self.result):
            raise ValueError(
                f"The result, {self.result}, must be in the format <integer>-<integer>"
            )

    def score(self, player: str | None = None) -> float:
        """The score of the match, based on result string.

        If the player argument is provided, the score of the player is returned.
        Otherwise, the score of the match as seen from player1 is returned.

        The function returns:
        - 1 if player1 or the given player won.
        - 0 if player1 or the given player lost.
        - 0.5 if the match is a draw.

        Args:
            player: The result for the given player, optional.

        Returns:
            1, 0, or 0.5 based on the result

        Raises:
            ValueError: If the player is not found in the match.
        """
        if player and player not in (self.player1, self.player2):
            raise ValueError(f"Player {player} not found in match.")

        player1_score, player2_score = map(int, self.result.split("-"))
        result = 0.5
        if player1_score > player2_score:
            result = 1.0
        elif player1_score < player2_score:
            result = 0.0

        if player and player == self.player2:
            result = 1 - result
        return result


@dataclass
class PlayerRating:
    """Represents a player's rating in a competitive system.

    This class is used to manage and encapsulate a player's rating and rating
    deviation (RD).

    Attributes:
        rating: The player's rating, typically at a default starting point of 1500.0.
        rd: The player's rating deviation, representing the uncertainty
            in the player's rating, defaulting to 350.0.
    """

    rating: float = 1500.0
    rd: float = 350.0

    def __str__(self) -> str:
        return f"PlayerRating(rating={self.rating:.1f}, rd={self.rd:.1f})"
