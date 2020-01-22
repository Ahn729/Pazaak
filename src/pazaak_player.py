import random
from abc import ABCMeta, abstractmethod
from pazaak_constants import SCORE_GOAL
from computer_strategies import blackjack_like_strategy

NEUTRAL_CARDS = range(1, 11)


def draw_card():
    return random.choice(NEUTRAL_CARDS)


class AbstractPlayer(metaclass=ABCMeta):
    """Abstract base class for pazaak players"""

    @property
    @abstractmethod
    def side_deck(self):
        pass

    @abstractmethod
    def play_card_or_stand(self, opponent):
        pass

    @classmethod
    def create_human(cls, name):
        return HumanPlayer(name)

    @classmethod
    def create_comupter(cls, name):
        return ComputerPlayer(name)

    @classmethod
    def create(cls, name):
        return cls(name)

    def __init__(self, name):
        self.hand = []
        self.board = []
        self.stands = False
        self.sets_won = 0
        self.name = name

    def stand(self):
        print(self.name + " stands.")
        self.stands = True

    def bust(self):
        print(self.name + " busted.")
        self.stands = True

    def clear_board(self):
        self.board.clear()

    def get_score(self):
        return sum(self.board)

    def get_status_string(self):
        return f"Board: {self.board}. Score: {self.get_score()}."

    def win_set(self):
        self.sets_won += 1
        return self

    def draw_hand(self):
        self.hand.extend(random.sample(self.side_deck, 4))

    def play_card_at(self, index):
        if index < len(self.hand):
            value = self.hand.pop(index)
            self.board.append(value)
            print(f"{self.name} plays a {value}.", end=" ")
            print(self.get_status_string())

    def take_turn(self, opponent):
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
            if index in ('1', '2', '3', '4'):
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

    strategy_func = blackjack_like_strategy
    side_deck = [val for val in range(-5, 6) for _ in (0, 1) if val != 0]

    def __init__(self, name="Opponent", strategy_func=blackjack_like_strategy):
        self.strategy_func = strategy_func
        super().__init__(name)

    def play_card_or_stand(self, opponent):
        play_card, card_index, stand = blackjack_like_strategy(
            self.hand, self.get_score(), opponent.get_score(), opponent.stands)

        if play_card:
            self.play_card_at(card_index)

        if stand:
            self.stand()

        # Check if we busted
        if self.get_score() > SCORE_GOAL:
            self.bust()
