"""Wrapper module to train different models and let them play"""

from timeit import default_timer as timer

from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor

import pandas as pd

from computer_learn import train_model
from pazaak_player import AbstractPlayer as Player
import pazaak
from computer_strategies import blackjack_like_strategy, decision_tree_strategy
from misc import suppress_stdout


def main():
    """Trains a model, then plays against computer"""

    function_start = timer()
    results = pd.DataFrame(columns=['model', 'test_score', 'win_pctg'])

    # Your favourite model goes here:
    models = {
        'DT_3': DecisionTreeRegressor(max_depth=3, random_state=42),
        'DT_4': DecisionTreeRegressor(max_depth=4, random_state=42),
        'DT_5': DecisionTreeRegressor(max_depth=5, random_state=42),
        'RF_3': RandomForestRegressor(n_estimators=10, max_depth=3,
                                      random_state=42),
        'RF_4': RandomForestRegressor(n_estimators=10, max_depth=4,
                                      random_state=42),
        'RF_5': RandomForestRegressor(n_estimators=10, max_depth=5,
                                      random_state=42),
    }

    pazaak.player = Player.create_computer("MLTrainee",
                                           decision_tree_strategy)
    pazaak.opponent = Player.create_computer("Opponent",
                                             blackjack_like_strategy)

    for model_name in models:
        model = models[model_name]
        # Since our random forests use 10 decision tree estimators, the
        # decision trees are ~10x faster
        if isinstance(model, DecisionTreeRegressor):
            n_games = 1000
        else:
            n_games = 200

        for rand_percentage in [80, 85, 90, 95]:
            train_file_name = f"resources/result_50k_{rand_percentage}.csv"
            model_desc = f"{model_name}_{rand_percentage}"

            start = timer()
            print(f"Training model {model_name} on {train_file_name}")
            test_score = train_model(model, train_file_name)

            with suppress_stdout():
                games_won = pazaak.play_n_games(n_games)
            end = timer()
            duration = int(end - start)
            gps = int(n_games / duration)
            print(f"{model_name} won {games_won} games out of {n_games} "
                  f"in {duration} seconds ({gps} games per second)")
            results = results.append({
                'model': model_desc,
                'test_score': test_score,
                'win_pctg': games_won / n_games
            }, ignore_index=True)

    total_duration = int(timer() - function_start)
    print(f"Total execution took {total_duration} seconds. Results:")
    results.sort_values(by='win_pctg', ascending=False).to_csv('resources/model_scores.csv')


if __name__ == '__main__':
    main()
