"""A simple implementation of KotOR's blackjack-inspired minigame"""

import random
import time
from pazaak_player import AbstractPlayer as Player
from pazaak_constants import SCORE_GOAL, SLEEP_TIME, \
    WINNING_SETS, REQUIRE_INPUT_AFTER_SET
from computer_strategies import decision_tree_strategy

# Change player config here!
player = Player.create_human("Alice")
opponent = Player.create_computer("Bob", strategy_func=decision_tree_strategy)


def set_is_over():
    """Determines whether a set is over

    Returns:
        True is set is over (both players either busted or stand), else False
    """
    return(
        player.get_score() > SCORE_GOAL
        or opponent.get_score() > SCORE_GOAL
        or (player.stands and opponent.stands))


def game_is_over():
    """Determine whether the game is over

    Returns:
        True if game is over (a player has won enough sets), else False
    """
    return WINNING_SETS in (player.sets_won, opponent.sets_won)


def get_winner():
    """Determine the winner of the game

    Returns:
        The winning player, or None if game isn't over yet
    """
    if player.sets_won == WINNING_SETS:
        return player
    if opponent.sets_won == WINNING_SETS:
        return opponent
    return None


def setup_game():
    """Sets up the geame"""
    player.draw_hand()
    opponent.draw_hand()


def determine_winner():
    """Determine the winner of the set

    Returns:
        The winning player
    """
    player_score = player.get_score()
    opponent_score = opponent.get_score()
    print(f"Set over. {player.name}'s score: {player_score}, "
          f"{opponent.name}'s score: {opponent_score}")

    if player_score > SCORE_GOAL:
        return opponent.win_set()
    if opponent_score > SCORE_GOAL:
        return player.win_set()
    if opponent_score > player_score:
        return opponent.win_set()
    if opponent_score < player_score:
        return player.win_set()
    return None


def prepare_next_set():
    """Cleanup boards and prepare for for next set"""
    player.stands, opponent.stands = False, False
    player.clear_board()
    opponent.clear_board()


def prepare_next_game():
    """Cleanup board and players to prepare next game"""
    prepare_next_set()
    player.sets_won, opponent.sets_won = 0, 0


def play_a_set(active_player, inactive_player, sleep_time=SLEEP_TIME):
    """Plays a single set of Pazaak

    Args:
        active_player: First player to take a turn
        inactive_player: Her opponent
        sleep_time: Time to elapse between turns in seconds

    Returns:
        The winning player
    """
    while not set_is_over():
        active_player.take_turn(inactive_player)
        time.sleep(sleep_time)
        active_player, inactive_player = inactive_player, active_player
    return determine_winner()


def play_a_game(require_input_after_set=REQUIRE_INPUT_AFTER_SET):
    """Plays a single game of Pazaak

    Args:
        require_input_after_set: Requires user input after set is over in order
            to suspend game progress

    Returns:
        The winning player
    """
    setup_game()
    active_player, inactive_player = random.sample([player, opponent], 2)
    while not game_is_over():
        winner = play_a_set(active_player, inactive_player)
        if winner is not None:
            print(winner.name, "wins the set.")
            # Winner starts next set
            if winner is not active_player:
                active_player, inactive_player = inactive_player, active_player
        else:
            print("Set ends with a draw.")

        if require_input_after_set:
            input(f"Sets won: {player.name}: {player.sets_won}, "
                  f"{opponent.name}: {opponent.sets_won}.")
        else:
            print(f"Sets won: {player.name}: {player.sets_won}, "
                  f"{opponent.name}: {opponent.sets_won}.")
        prepare_next_set()
    print(f"Game over. {get_winner().name} won. Congratulations!")
    return get_winner()


# Main #
def main():
    """Main entry point of the game"""
    play_a_game()


if __name__ == "__main__":
    main()
