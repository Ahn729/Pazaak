"""Collection of strategies to be used by Computer Player"""

import random
import pandas as pd
import numpy as np
from computer_strategies import blackjack_like_strategy as bls
from computer_strategies import random_strategy as rds
import pazaak
from pazaak_player import AbstractPlayer as Player

dataset = pd.DataFrame(
        columns=['self_score', 'opp_score', 'opp_stands',
                 'result_card_val', 'result_stand', 'score'],
        dtype=float)


# Main #
def main():
    """Train the AI

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

    for _ in range(1, 10):
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

    dataset.to_csv('result.csv')
    print(f"MLTrainee won {sets_won} sets")


def record_results_rand_strategy(self_hand, self_score, opp_score, opp_stands):
    """Plays using a random strategy and records the results"""
    global dataset

    # We want our trainee to make mistakes. However, too many mistakes may not
    # result in a valuable learn dataset. Hence, we're chosing out blackjack
    # strategy over a coplete random strategy, depending on a random value
    strategy_func = bls if random.random() < 0.8 else rds
    play_card, card_index, stand = strategy_func(
        self_hand, self_score, opp_score, opp_stands)
    dataset = dataset.append({
        'self_score': self_score,
        'opp_score': opp_score,
        'opp_stands': opp_stands,
        'result_card_val': self_hand[card_index],
        'result_stand': stand,
        'score': np.nan
    }, ignore_index=True)
    return (play_card, card_index, stand)


if __name__ == "__main__":
    main()
