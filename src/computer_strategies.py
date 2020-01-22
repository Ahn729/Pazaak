"""Collection of strategies to be used by Computer Player"""

from pazaak_constants import SCORE_GOAL, OPPONENT_STAND_THRESHOLD


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

    # If standing wins us the game, we do it and won't consider playing a card.
    if opp_score < self_score <= SCORE_GOAL and opp_stands:
        stand = True

    else:
        # Check whether we play a card

        # We always play if we reach 20 or if it results in certain win
        for indx, card in enumerate(self_hand):
            if (self_score + card == SCORE_GOAL
                    or opp_score < self_score + card <= SCORE_GOAL and opp_stands):
                play_card, card_index = True, indx
                current_score += card
                break

        # We play to reach 19, but only if the opponent doesn't have 20 already
        else:
            for indx, card in enumerate(self_hand):
                if self_score + card == SCORE_GOAL - 1 and opp_score != SCORE_GOAL:
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
