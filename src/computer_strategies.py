"""Collection of strategies to be used by Computer Player"""

import random
from pazaak_constants import SCORE_GOAL, OPPONENT_STAND_THRESHOLD


def random_strategy(self_hand, self_score, opp_score, opp_stands):
    """Random strategy (all actions are performed at random)

    Args:
        self_hand: Player's hand (list of card values)
        self_score: Player's current score
        opp_score: Opponent's Score
        opp_stands: Whether or not opponent player opp_stands

    Returns:
        A tuple (play_card, card_index, stand), where
        play_card indicates whether a card is played,
        card_index incicates the index of the card to play (if any),
        stand indicates whether the player stands.
    """

    play_card, card_index, stand = False, 0, False

    if self_hand:
        play_card = random.choice([True, False])
        card_index = random.randrange(0, len(self_hand))

    stand = random.choice([True, False])

    return (play_card, card_index, stand)


def blackjack_like_strategy(self_hand, self_score, opp_score, opp_stands):
    """Blackjack-like strategy (dealer draws to 16 stands on 17)

    Args:
        self_hand: Player's hand (list of card values)
        self_score: Player's current score
        opp_score: Opponent's Score
        opp_stands: Whether or not opponent player opp_stands

    Returns:
        A tuple (play_card, card_index, stand), where
        play_card indicates whether a card is played,
        card_index incicates the index of the card to play (if any),
        stand indicates whether the player stands.
    """

    current_score = self_score
    play_card, card_index, stand = False, 0, False

    # If we're at 20 already, or standing wins us the set,
    # we do it and won't consider playing a card.
    if (self_score == SCORE_GOAL
            or opp_score < self_score <= SCORE_GOAL and opp_stands):
        stand = True

    # else check whether we play a card
    else:
        # We always play if we reach 20 or if it results in certain win
        for indx, card in enumerate(self_hand):
            if (self_score + card == SCORE_GOAL
                    or opp_score < self_score + card <= SCORE_GOAL
                    and opp_stands):
                play_card, card_index = True, indx
                current_score += card
                break

        # We play to reach 19, but only if the opponent doesn't have 20 already
        else:
            for indx, card in enumerate(self_hand):
                if (self_score + card == SCORE_GOAL - 1
                        and opp_score != SCORE_GOAL):
                    play_card, card_index = True, indx
                    current_score += card
                    break

            # If we're about to bust, 18 is fine as well
            else:
                for indx, card in enumerate(self_hand):
                    if (self_score > 20
                            and self_score + card == SCORE_GOAL - 2
                            and opp_score <= SCORE_GOAL - 2):
                        play_card, card_index = True, indx
                        current_score += card
                    break

    # Check whether we stand
    # We never stand if this would result in certain loss
    if current_score < opp_score <= SCORE_GOAL and opp_stands:
        pass
    # We always stand if standing wins us the game now.
    elif opp_score < current_score <= SCORE_GOAL and opp_stands:
        stand = True
    # Else just check the threshold
    elif current_score > OPPONENT_STAND_THRESHOLD:
        stand = True

    return (play_card, card_index, stand)
