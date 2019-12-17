import random
from abc import ABCMeta, abstractmethod
from PazaakConstants import *

neutralCards = range(1, 11)


def draw_card():
    return random.choice(neutralCards)


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

    stand_threshold = 0
    side_deck = [val for val in range(-5, 6) for _ in (0, 1) if val != 0]

    def __init__(self, name="Opponent", stand_threshold=OPPONENT_STAND_THRESHOLD):
        self.stand_threshold = stand_threshold
        super().__init__(name)


    def play_card_or_stand(self, player):
        player_score = player.get_score()
        opponent_score = self.get_score()

        # If we're at 20 points already, we stand
        if opponent_score == 20:
            self.stand()

        # If standing wins us the game, we just do it.
        elif player_score < opponent_score and opponent_score <= SCORE_GOAL and player.stands:
            self.stand()

        else:
            # Check whether we play a card
            # We always play if we reach 20
            for indx, card in enumerate(self.hand):
                if opponent_score + card == SCORE_GOAL:
                    self.play_card_at(indx)
                    opponent_score += card
                    break

                # We play to reach 19, but only if the player doesn't have 20 already
            else:
                for indx, card in enumerate(self.hand):
                    if opponent_score + card == SCORE_GOAL-1 and player_score != SCORE_GOAL:
                        self.play_card_at(indx)
                        opponent_score += card
                        break

            # Check whether we stand
            # We never stand if this would result in certain loss
            if player_score > opponent_score and player_score <= SCORE_GOAL and player.stands:
                pass

            # Else just check the threshold
            elif opponent_score > self.stand_threshold and opponent_score <= SCORE_GOAL:
                self.stand()

            # Check if we busted
            elif opponent_score > SCORE_GOAL:
                self.bust()
