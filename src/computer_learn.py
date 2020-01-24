"""Collection of strategies to be used by Computer Player"""

import random
import pandas as pd
import numpy as np
from sklearn.tree import DecisionTreeRegressor
from sklearn.model_selection import train_test_split
from joblib import dump

from computer_strategies import blackjack_like_strategy as bls
from computer_strategies import random_strategy as rds
import pazaak
from pazaak_player import AbstractPlayer as Player
from pazaak_constants import DATASET_FILE_NAME, MODEL_FILE_NAME

dataset = pd.DataFrame(
        columns=['self_score', 'opp_score', 'opp_stands',
                 'result_card_val', 'result_stand', 'score'],
        dtype=float)


def create_dataset():
    """Creates the dataset supplied to a machine learning model

    Uses record_results_strategy to obtain a pandas dataframe containing
    parameters, actions taken and score. We assign the following score
    values:
     * If the set was won, 1 point for the last action, .5 for all others
     * If the set was lost, -1 point for the last action, -.5 for all others
     Writes the results in 'result.csv' file
    """

    pazaak.player = Player.create_computer(
        "MLTrainee", strategy_func=record_results_rand_strategy)
    pazaak.opponent = Player.create_computer("Opponent", strategy_func=bls)

    sets_won = 0

    for _ in range(1, 10000):
        # TODO: Handle draws
        winner = pazaak.play_a_game()
        if winner.name == "MLTrainee":
            dataset.fillna(.5, inplace=True)
            dataset.iloc[-1, 5] = 1
            sets_won += 1
        else:
            dataset.fillna(-.5, inplace=True)
            dataset.iloc[-1, 5] = -1
        pazaak.prepare_next_game()

    dataset.to_csv(DATASET_FILE_NAME, index=False)
    print(f"MLTrainee won {sets_won} sets")


def train_model():
    """Trains a model with the dataset obtained by create_dataset

    Currently uses a decision tree without further optimization. There's
    certainly a lot of space for improvement here.
    """
    dataset = pd.read_csv(DATASET_FILE_NAME)

    # A minumum amount of feature engineering: The player's and opponent's
    # exact score may not be that important for our decisions. The difference,
    # however, certainly is.
    dataset['score_difference'] = dataset.self_score - dataset.opp_score
    dataset.drop(columns=['opp_score'], inplace=True)

    # Strategy will be to let our model predict the score for different actions.
    # Hence, we're going to train the model on that now
    X, y = dataset.drop(columns='score'), dataset.score
    X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=42)
    regressor = DecisionTreeRegressor(max_depth=5, min_samples_leaf=5)
    regressor.fit(X_train, y_train)
    print(f"Score on the test set: {regressor.score(X_test, y_test)}")

    # For persistence, we export the generated model_selection
    dump(regressor, MODEL_FILE_NAME)


def record_results_rand_strategy(self_hand, self_score, opp_score, opp_stands):
    """Plays using a random strategy and records the results"""
    global dataset

    # We want our trainee to make mistakes. However, too many mistakes may not
    # result in a valuable learn dataset. Hence, we're chosing our blackjack
    # strategy over a coplete random strategy, depending on a random value
    strategy_func = bls if random.random() < 0.9 else rds
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
