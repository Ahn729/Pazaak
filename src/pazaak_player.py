"""This module contains two pazaak players: A human one (requiring keyboard
input) and a computer player. Computer players can use strategies as defined
in the computer_strategies module.
"""

import random
from abc import ABCMeta, abstractmethod
from pazaak_constants import SCORE_GOAL, HAND_SIZE
from computer_strategies import blackjack_like_strategy

NEUTRAL_CARDS = range(1, 11)


def draw_card():
    """Draw a card

    Returns:
        A random card chosen from the stack of neutral cards
    """
    return random.choice(NEUTRAL_CARDS)


class AbstractPlayer(metaclass=ABCMeta):
    """Abstract base class for pazaak players"""

    @property
    @abstractmethod
    def side_deck(self):
        """Abstract Side Deck property"""

    @abstractmethod
    def play_card_or_stand(self, opponent):
        """Determine whether to play a card and / or stand

        Args:
            opponent: Player's opponent
        """

    @classmethod
    def create_human(cls, name):
        """Creates a human player

        Args:
            name: Player's name
        """
        return HumanPlayer(name)

    @classmethod
    def create_computer(cls, name, strategy_func=blackjack_like_strategy):
        """Creates a computer player

        Args:
            name: Player's name
            strategy_func: computer strategy fuction to use
        """
        return ComputerPlayer(name, strategy_func)

    @classmethod
    def create(cls, name):
        """Creates class with given name"""
        return cls(name)

    def __init__(self, name):
        self.hand = []
        self.board = []
        self.stands = False
        self.sets_won = 0
        self.name = name

    def stand(self):
        """Used when a player decides to stand (not accepting any more cards)"""
        print(self.name + " stands.")
        self.stands = True

    def bust(self):
        """Used when a player busts (due to too high score)"""
        print(self.name + " busted.")
        self.stands = True

    def clear_board(self):
        """Clears the board for a new game"""
        self.board.clear()

    def get_score(self):
        """Computes player's score from the board

        Returns:
            player's score
        """
        return sum(self.board)

    def get_status_string(self):
        """Status string to print on console

        Returns:
            status string including board and score
        """
        return f"Board: {self.board}. Score: {self.get_score()}."

    def win_set(self):
        """Wins the set for the player

        Returns:
            the player
        """
        self.sets_won += 1
        return self

    def draw_hand(self):
        """Draw cards from the side deck to initiate a new set"""
        self.hand.extend(random.sample(self.side_deck, HAND_SIZE))

    def play_card_at(self, index):
        """Plays card at index

        Args:
            index: The index in player's hand of the card to play
        """
        if index < len(self.hand):
            value = self.hand.pop(index)
            self.board.append(value)
            print(f"{self.name} plays a {value}.", end=" ")
            print(self.get_status_string())

    def take_turn(self, opponent):
        """Take a turn: Player draws a card, plays a card from her hand if
        appropriate, stands if appropriate.

        Args:
            opponent: The player's opponent
        """
        print(f"{self.name}'s turn.")
        if not self.stands:
            card = draw_card()
            self.board.append(card)
            print(f"{self.name} drew a {card}. {self.get_status_string()}")
            self.play_card_or_stand(opponent)
        else:
            print(f"{self.name} stands. {self.get_status_string()}")


class HumanPlayer(AbstractPlayer):
    """Human pazaak player"""

    side_deck = [val for val in range(-5, 6) for _ in (0, 1) if val != 0]

    def __init__(self, name="Player"):
        self.name = name
        super().__init__(name)

    def play_card_or_stand(self, opponent):

        # If we're having 20 points, there's no point in playing a card
        if self.get_score() == SCORE_GOAL:
            self.stand()

        # Else, we ask the player to play a card
        else:
            print("Your hand:", self.hand)
            index = input("Play which card? ")
            if index.isdigit() and int(index) in range(1, len(self.hand) + 1):
                card_index = int(index)-1
                self.play_card_at(card_index)

            # If player busted or reached 20, she must stand
            if self.get_score() == SCORE_GOAL:
                self.stand()
            elif self.get_score() > SCORE_GOAL:
                self.bust()

            # else we ask her whether to stand
            else:
                stand = input("Stand? ")
                if stand in ('y', 'ye', 'yes', '1'):
                    self.stand()


class ComputerPlayer(AbstractPlayer):
    """Computer pazaak player"""

    side_deck = [val for val in range(-5, 6) for _ in (0, 1) if val != 0]

    def __init__(self, name="Opponent", strategy_func=blackjack_like_strategy):
        self.strategy_func = strategy_func
        super().__init__(name)

    def play_card_or_stand(self, opponent):
        play_card, card_index, stand = self.strategy_func(
            self.hand, self.get_score(), opponent.get_score(), opponent.stands)

        if play_card:
            self.play_card_at(card_index)

        # Check if we busted
        if self.get_score() > SCORE_GOAL:
            self.bust()
        elif stand:
            self.stand()
