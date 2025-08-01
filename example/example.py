from pathlib import Path

import pandas as pd

from glicko.glicko import update_all_players
from glicko.models import PlayerRating
from glicko.rating_engine import create_rating_periods
from glicko.rating_engine import extract_matches
from glicko.rating_engine import print_ratings

if __name__ == "__main__":
    data_dir = Path(__file__).parent.parent / "data"
    df = pd.read_csv(data_dir / "soccer_norway_level2_2024.csv")

    df_rating_periods = create_rating_periods(df, "rounds", 10)
    print(df_rating_periods.head())

    total_matches = extract_matches(df_rating_periods)
    players_in_total = {match.player1 for match in total_matches} | {
        match.player2 for match in total_matches
    }
    player_ratings = {player: PlayerRating() for player in players_in_total}

    start_period = df_rating_periods["RatingPeriod"].min()
    end_period = df_rating_periods["RatingPeriod"].max()
    for period in range(start_period, end_period + 1):
        period_matches = extract_matches(df_rating_periods, period)
        player_ratings = update_all_players(player_ratings, period_matches)
        print_ratings(player_ratings)
