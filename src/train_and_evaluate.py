"""Wrapper module to train different models and let them play"""
import sys, os
from timeit import default_timer as timer

from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor, ExtraTreesRegressor
import pandas as pd

from computer_learn import train_model
from pazaak_player import AbstractPlayer as Player
import pazaak
from computer_strategies import blackjack_like_strategy, decision_tree_strategy


def main():
    """Trains a model, then plays against computer"""

    results = pd.DataFrame(columns=['model', 'test_score', 'win_pctg'])

    models = {
        'DT_4': DecisionTreeRegressor(max_depth=4, random_state=42),
        'DT_5': DecisionTreeRegressor(max_depth=5, random_state=42),
        'DT_6': DecisionTreeRegressor(max_depth=6, random_state=42),
        'DT_7': DecisionTreeRegressor(max_depth=7, random_state=42),
        'RF_5': RandomForestRegressor(n_estimators=10, max_depth=5,
                                      random_state=42),
        'RF_6': RandomForestRegressor(n_estimators=10, max_depth=6,
                                      random_state=42),
        'RF_7': RandomForestRegressor(n_estimators=10, max_depth=7,
                                      random_state=42),
        'ET_5': ExtraTreesRegressor(n_estimators=10, max_depth=5,
                                    random_state=42),
        'ET_6': ExtraTreesRegressor(n_estimators=10, max_depth=6,
                                    random_state=42),
        'ET_7': ExtraTreesRegressor(n_estimators=10, max_depth=7,
                                    random_state=42)
    }

    for model_name in models:
        model = models[model_name]
        if isinstance(model, DecisionTreeRegressor):
            n_games = 5000
        else:
            n_games = 1000

        start = timer()
        test_score = train_model(models[model_name])
        pazaak.player = Player.create_computer("MLTrainee",
                                               decision_tree_strategy)
        pazaak.opponent = Player.create_computer("Opponent",
                                                 blackjack_like_strategy)
        with open(os.devnull, "w") as devnull:
            tmp = sys.stdout
            sys.stdout = devnull
            games_won = pazaak.play_n_games(n_games)
            sys.stdout = tmp
        end = timer()
        duration = int(end - start)
        gps = int(n_games / duration)
        print(f"{model_name} won {games_won} games out of {n_games} "
              f"in {duration} seconds ({gps} games per second)")
        results = results.append({
            'model': model_name,
            'test_score': test_score,
            'win_pctg': games_won / n_games
        }, ignore_index=True)

    print(results)


if __name__ == '__main__':
    main()
