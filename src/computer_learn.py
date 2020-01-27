"""Collection of strategies to be used by Computer Player"""

import random
from timeit import default_timer as timer
import functools
from joblib import dump

import pandas as pd
import numpy as np
from sklearn.tree import DecisionTreeRegressor, export_graphviz
from sklearn.model_selection import train_test_split

from computer_strategies import blackjack_like_strategy as bls
from computer_strategies import random_strategy as rds
import pazaak
from pazaak_player import AbstractPlayer as Player
from pazaak_constants import DATASET_FILE_NAME, MODEL_FILE_NAME, \
    GRAPHVIZ_FILE_NAME

dataset = pd.DataFrame(
        columns=['self_score', 'opp_score', 'opp_stands',
                 'result_card_val', 'result_stand', 'score'],
        dtype=float)


def create_dataset(learning_sets=1000, strategy_func=None):
    """Creates the dataset supplied to a machine learning model

    Args:
        learning_sets: Number of sets to play in order to create the
            dataset. Default: 1000
        strategy_func: Strategy function to use by player. If None is passed,
            it will be chosen at random in every iteration

    Uses record_results_strategy to obtain a pandas dataframe containing
    parameters, actions taken and score. We assign the following score
    values:
     * If the set was won, 1 point for the last action, .5 for all others
     * If the set ends with a draw, 0 points for all actions
     * If the set was lost, -1 point for the last action, -.5 for all others
     Writes the results in DATASET_FILE_NAME (result.csv) file
    """

    player_strategy_func = functools.partial(record_results,
                                             strategy_func=strategy_func)

    pazaak.player = Player.create_computer(
        "MLTrainee", strategy_func=player_strategy_func)
    pazaak.opponent = Player.create_computer("Opponent", strategy_func=bls)

    sets_won, draws, sets_lost = 0, 0, 0
    start = timer()

    pazaak.setup_game()

    for _ in range(0, learning_sets):
        winner = pazaak.play_a_set(
            *random.sample([pazaak.player, pazaak.opponent], 2), sleep_time=0)
        if winner is None:
            dataset.fillna(0, inplace=True)
            draws += 1
        elif winner.name == "MLTrainee":
            dataset.fillna(.5, inplace=True)
            dataset.iloc[-1, 5] = 1
            sets_won += 1
        else:
            dataset.fillna(-.5, inplace=True)
            dataset.iloc[-1, 5] = -1
            sets_lost += 1
        pazaak.prepare_next_game()

    dataset.to_csv(DATASET_FILE_NAME, index=False)
    end = timer()
    total_time = int(end - start)
    sets_per_sec = learning_sets / total_time

    print(f"MLTrainee won {sets_won} sets. Draws: {draws}. Lost: {sets_lost}")
    print(f"Played a total of {learning_sets} sets in {total_time} seconds. "
          f"This accounts to {sets_per_sec} sets per second)")


def train_model(regressor=DecisionTreeRegressor(max_depth=7, random_state=42)):
    """Trains a model with the dataset obtained by create_dataset

    Args:
        regressor: The model to use. Defalut: DecisionTreeRegressor

    Currently uses a decision tree without further optimization. There's
    certainly a lot of space for improvement here.
    """
    df = pd.read_csv(DATASET_FILE_NAME)

    # A minumum amount of feature engineering: The player's and opponent's
    # exact score may not be that important for our decisions. The difference,
    # however, certainly is. Moreover, the card value itself is not that
    # important. Here, the sum is.
    df['score_difference'] = df.self_score - df.opp_score
    df.drop(columns=['opp_score'], inplace=True)
    df['score_if_card_played'] = df.self_score + df.result_card_val
    df.drop(columns=['result_card_val'], inplace=True)

    # Strategy will be to let our model predict the score for different actions
    # Hence, we're going to train the model on that now
    X, y = df.drop(columns='score'), df.score
    X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=42)
    regressor.fit(X_train, y_train)

    feature_names = ['self_score', 'opp_stands', 'result_stand',
                     'score_difference', 'score_if_card_played']

    score = regressor.score(X_test, y_test)
    print(f"Score on the test set: {score}.")
    print("Feature importances:")
    print(pd.DataFrame(data=[regressor.feature_importances_],
                       columns=feature_names).to_string(index=False))
    if isinstance(regressor, DecisionTreeRegressor):
        export_graphviz(regressor, feature_names=feature_names,
                        out_file=GRAPHVIZ_FILE_NAME, filled=True)

    # For persistence, we export the generated model
    dump(regressor, MODEL_FILE_NAME)
    return score


def record_results(self_hand, self_score, opp_score, opp_stands,
                   strategy_func=None):
    """Plays using a random strategy and records the results

    Args:
        strategy_func: Strategy function to use by player. If None is passed,
            it will be chosen at random in every iteration
    """
    global dataset

    # We want our trainee to make mistakes. However, too many mistakes may not
    # result in a valuable learn dataset. Hence, we're chosing our blackjack
    # strategy over a coplete random strategy, depending on a random value
    if strategy_func is None:
        strategy_func = bls if random.random() < 0.95 else rds
    play_card, card_index, stand = strategy_func(
        self_hand, self_score, opp_score, opp_stands)
    dataset = dataset.append({
        'self_score': self_score,
        'opp_score': opp_score,
        'opp_stands': opp_stands,
        'result_card_val': self_hand[card_index] if play_card else 0,
        'result_stand': stand,
        'score': np.nan
    }, ignore_index=True)
    return (play_card, card_index, stand)
