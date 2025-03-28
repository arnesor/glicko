import math
from collections import defaultdict

from models import Match
from models import PlayerRating

# Constants
Q = math.log(10) / 400  # Glicko constant
C = 50


def g(rd: float) -> float:
    """Calculates the quantity g as given in the Glicko paper.

    Args:
        rd: Ratings deviation, the standard deviation of the player's rating.

    Returns:
        The quantity g as given in the Glicko paper.
    """
    return 1.0 / math.sqrt(1 + (3 * Q**2 * rd**2) / math.pi**2)


def e(r_player: float, r_opponent: float, rd_opponent: float) -> float:
    """Calculates the quantity e as given in the Glicko paper"""
    g_rd_opponent = g(rd_opponent)
    return 1 / (1 + 10 ** (-g_rd_opponent * (r_player - r_opponent) / 400.0))


def d_squared(r_player: float, opponents_rating: list[PlayerRating]) -> float:
    """Calculates the quantity d^2 as given in the Glicko paper"""
    d2_inv = 0.0
    for opponent in opponents_rating:
        g_rd_opponent = g(opponent.rd)
        e_val = e(r_player, opponent.rating, opponent.rd)
        d2_inv += Q**2 * g_rd_opponent**2 * e_val * (1 - e_val)
    return 1.0 / d2_inv if d2_inv != 0 else float("inf")


def expected_score(
    r_player: float, r_opponent: float, rd_player: float, rd_opponent: float
) -> float:
    """Calculates the expected score for a match between two players."""
    g_rd = g(math.sqrt(rd_player**2 + rd_opponent**2))
    return 1 / (1 + 10 ** (-g_rd * (r_player - r_opponent) / 400.0))


def update_player(
    player_rating: PlayerRating, opponent_data: list[tuple[float, float, float]]
) -> PlayerRating:
    if not opponent_data:
        # No games, increase RD to reflect uncertainty (e.g., add 50)
        return PlayerRating(
            player_rating.rating, min(math.sqrt(player_rating.rd**2 + C**2), 350)
        )

    opponents_rating = [PlayerRating(rating, rd) for rating, rd, _ in opponent_data]

    d2 = d_squared(player_rating.rating, opponents_rating)
    pre_factor = Q / (1 / player_rating.rd**2 + 1 / d2)

    delta_sum = 0
    for r_op, rd_op, score in opponent_data:
        e_val = e(player_rating.rating, r_op, rd_op)
        g_rd = g(rd_op)
        delta_sum += g_rd * (score - e_val)

    new_r = player_rating.rating + pre_factor * delta_sum
    new_rd = math.sqrt(1 / (1 / player_rating.rd**2 + 1 / d2))

    return PlayerRating(new_r, new_rd)


def get_player_matches(player: str, matches: list[Match]) -> list[Match]:
    """Returns all matches where the specified player is either player1 or player2.

    Args:
        player: The player to search for.
        matches: The list of Match objects.

    Returns:
        A list of Match objects where the player is either player1 or player2.
    """
    return [match for match in matches if player in (match.player1, match.player2)]


def update_all_players(
    player_ratings: dict[str, PlayerRating], match_results: list[Match]
) -> dict[str, PlayerRating]:
    # Collect all games played by each player
    games_by_player = defaultdict(list)
    for match in match_results:
        player1_rating = player_ratings[match.player1]
        player2_rating = player_ratings[match.player2]
        games_by_player[match.player1].append(
            (player2_rating.rating, player2_rating.rd, match.score())
        )
        games_by_player[match.player2].append(
            (player1_rating.rating, player1_rating.rd, 1 - match.score())
        )  # opponent's perspective

    # Update ratings
    new_ratings = {}
    for player, player_rating in player_ratings.items():
        new_ratings[player] = update_player(player_rating, games_by_player[player])
    return new_ratings


if __name__ == "__main__":
    player_r = 1500
    player_rd = 200
    opponent_r = 1700
    opponent_rd = 300
    player_ratings = {
        "0": PlayerRating(1500, 200),
        "1": PlayerRating(1400, 30),
        "2": PlayerRating(1550, 100),
        "3": PlayerRating(1700, 300),
    }
    matches = [
        Match("0", "1", "2-1"),
        Match("0", "2", "1-3"),
        Match("3", "0", "4-2"),
    ]
    result = update_all_players(player_ratings, matches)

    print("Updated player ratings:")
    for player, rating in result.items():
        print(f"{player}: {rating.rating:.1f} +/- {rating.rd:.1f}")
