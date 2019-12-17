import random
import time
from PazaakPlayer import AbstractPlayer as Player
from PazaakConstants import *

# Change player config here!
player = Player.create_human("Alfons")
opponent = Player.create_comupter("Bob")


def set_is_over():
    return(
        player.get_score() > SCORE_GOAL
        or opponent.get_score() > SCORE_GOAL
        or (player.stands and opponent.stands))


def game_is_over():
    return WINNING_SETS in (player.sets_won, opponent.sets_won)


def get_winner():
    if player.sets_won == WINNING_SETS:
        return player
    elif opponent.sets_won == WINNING_SETS:
        return opponent


def setup_game():
    player.draw_hand()
    opponent.draw_hand()


def determine_winner():
    player_score = player.get_score()
    opponent_score = opponent.get_score()
    print(f"Set over. {player.name}'s score: {player_score}, {opponent.name}'s score: {opponent_score}")

    if player_score > SCORE_GOAL:
        return opponent.win_set()
    elif opponent_score > SCORE_GOAL:
        return player.win_set()
    elif opponent_score > player_score:
        return opponent.win_set()
    elif opponent_score < player_score:
        return player.win_set()
    else:
        return None


def prepare_next_set():
    player.stands, opponent.stands = False, False
    player.clear_board()
    opponent.clear_board()


# Main #
def main():
    setup_game()
    active_player, inactive_player = random.sample([player, opponent], 2)

    while not game_is_over():
        while not set_is_over():
            active_player.take_turn(inactive_player)
            time.sleep(SLEEP_TIME)
            active_player, inactive_player = inactive_player, active_player

        winner = determine_winner()
        if winner is not None:
            print(winner.name, "wins the set.")
            # Winner starts next set
            if winner is not active_player:
                active_player, inactive_player = inactive_player, active_player
        else:
            print("Set ends with a draw.")

        input(f"Sets won: {player.name}: {player.sets_won}, {opponent.name}: {opponent.sets_won}.")
        prepare_next_set()
    print(f"Game over. {get_winner().name} won. Congratulations!")


if __name__ == "__main__":
    main()
