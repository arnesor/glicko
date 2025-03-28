import re
from dataclasses import dataclass


@dataclass(frozen=True)
class Match:
    player1: str
    player2: str
    result: str

    def __post_init__(self):
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
    rating: float = 1500.0
    rd: float = 350.0
