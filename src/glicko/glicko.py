"""This module implements the Glicko rating system.

The rating system is described in detail here: https://www.glicko.net/glicko/glicko.pdf
"""

import math
from collections import defaultdict

from .models import Match
from .models import PlayerRating

# Constants
Q = math.log(10) / 400  # Glicko constant
C = 50  # Governs the increase in uncertainty between rating periods


def g(rd: float) -> float:
    """Calculates the quantity g as given in the Glicko paper.

    Args:
        rd: Ratings deviation, the standard deviation of the player's rating.

    Returns:
        The quantity g as given in the Glicko paper.
    """
    return 1.0 / math.sqrt(1 + (3 * Q**2 * rd**2) / math.pi**2)


def e(player_rating: float, opponent: PlayerRating) -> float:
    """Calculates the quantity E(s|r,rj,RDj) as given in the Glicko paper."""
    g_rd_opponent = g(opponent.rd)
    return 1 / (1 + 10 ** (-g_rd_opponent * (player_rating - opponent.rating) / 400.0))


def d_squared(player_rating: float, opponents_rating: list[PlayerRating]) -> float:
    """Calculates the quantity d^2 as given in the Glicko paper"""
    d2_inv = 0.0
    for opponent in opponents_rating:
        g_rd_opponent = g(opponent.rd)
        e_val = e(player_rating, opponent)
        d2_inv += Q**2 * g_rd_opponent**2 * e_val * (1 - e_val)
    return 1.0 / d2_inv if d2_inv != 0 else float("inf")


def win_probability(player: PlayerRating, opponent: PlayerRating) -> float:
    """Calculates the expected score for a match between two players."""
    g_rd = g(math.sqrt(player.rd**2 + opponent.rd**2))
    return 1 / (1 + 10 ** (-g_rd * (player.rating - opponent.rating) / 400.0))


def update_player(
    player: PlayerRating, opponent_data: list[tuple[PlayerRating, float]]
) -> PlayerRating:
    if not opponent_data:
        # No games, increase RD to reflect uncertainty (e.g., add C=50)
        return PlayerRating(player.rating, min(math.sqrt(player.rd**2 + C**2), 350))

    opponents_rating = [rating for rating, _ in opponent_data]

    d2 = d_squared(player.rating, opponents_rating)
    pre_factor = Q / (1 / player.rd**2 + 1 / d2)

    delta_sum = 0
    for opponent, score in opponent_data:
        e_val = e(player.rating, opponent)
        g_rd_opponent = g(opponent.rd)
        delta_sum += g_rd_opponent * (score - e_val)

    new_r = player.rating + pre_factor * delta_sum
    new_rd = math.sqrt(1 / (1 / player.rd**2 + 1 / d2))

    return PlayerRating(new_r, new_rd)


def update_all_players(
    player_ratings: dict[str, PlayerRating], match_results: list[Match]
) -> dict[str, PlayerRating]:
    # Collect all games played by each player
    games_by_player = defaultdict(list)
    for match in match_results:
        player1_rating = player_ratings[match.player1]
        player2_rating = player_ratings[match.player2]
        games_by_player[match.player1].append((player2_rating, match.score()))
        games_by_player[match.player2].append((player1_rating, 1 - match.score()))

    return {
        player_name: update_player(player_rating, games_by_player[player_name])
        for player_name, player_rating in player_ratings.items()
    }
