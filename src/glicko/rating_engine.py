import pandas as pd

from .models import Match
from .models import PlayerRating


def create_rating_periods(
    match_df: pd.DataFrame, strategy: str, rating_periods: int
) -> pd.DataFrame:
    """Create rating periods based on the match data and a spe cified strategy."""
    if strategy == "rounds":
        # Assign the "RatingPeriod" column by grouping rounds into bins
        match_df["RatingPeriod"] = pd.cut(
            match_df["Round"],
            bins=rating_periods,
            labels=range(1, rating_periods + 1),
            include_lowest=True,
        )
    return match_df


def extract_matches(df: pd.DataFrame, period: int | None = None) -> list[Match]:
    """Extracts matches from a dataframe, filtered by an optional rating period.

    Args:
        df: Input DataFrame containing match information. It must have
            columns "RatingPeriod", "HomeTeam", "AwayTeam", and "Result".
        period: The specific rating period for which matches need to be
            extracted, optional.

    Returns:
        A list of `Match` objects representing the matches.
    """
    if period is not None:
        df_match = df.loc[
            df["RatingPeriod"] == period, ["HomeTeam", "AwayTeam", "Result"]
        ]
    else:
        df_match = df[["HomeTeam", "AwayTeam", "Result"]]
    return [Match(home, away, result) for home, away, result in df_match.to_numpy()]


def print_ratings(player_ratings: dict[str, PlayerRating]) -> None:
    """Print player ratings sorted by the largest rating first."""
    sorted_ratings = sorted(
        player_ratings.items(), key=lambda x: x[1].rating, reverse=True
    )
    max_player_name_length = max(len(player) for player in player_ratings)
    print("---------------------------------------------")
    for player, rating in sorted_ratings:
        print(f"{player:<{max_player_name_length}}: {rating}")
