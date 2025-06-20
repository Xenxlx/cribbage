'''
This is my attempt at making a cribbage game!
Note that this was started as a means to learn OOP.
The goal is to make it functional before being stylistically correct.
'''
import hand_calc
from random import randint
DISCARDS = 2

# I could've made a card class but hand_calc takes has card property constants

class Deck:
    cards = [[rank, suit] for suit in hand_calc.SUIT_LST for rank in hand_calc.RANK_LST]
    left = len(cards)

    def __str__(self):
        cards = ""
        for i in range(len(self.cards)):
            cards += f"{self.cards[i]}\n"
        return f"{cards}"

    @classmethod
    def deal(cls):
        cls.left -= 1
        return cls.cards.pop(randint(0, cls.left - 1))
    
    @classmethod
    def reset(cls):
        cards = [[rank, suit] for suit in hand_calc.SUIT_LST for rank in hand_calc.RANK_LST]
        left = len(cards)

class Game:
    crib = []
    crib_points = 0
    peg_sequence = []
    peg_count = 0
    cut = None

    @classmethod
    def print_crib(cls):
        hand = ""
        for i in range(len(cls.crib)):
            # unsure if it's printing correctly/logically
            hand += f"{i+1}: " + "".join(cls.crib[i]) + "  "
        print(hand)
    
    @classmethod
    def get_cut(cls):
        cls.cut = Deck.deal()

    @classmethod
    def print_peg_sequence(cls):
        hand = ""
        for i in range(len(cls.peg_sequence)):
            hand += f"{i+1}: " + "".join(cls.peg_sequence[i]) + "  "
        print(f"Pegging sequence: {hand}")

    @classmethod
    def peg_round_reset(cls):
        cls.peg_sequence = []
        cls.peg_count = 0

class Player:
    def make_hand(self, num_cards):
        for i in range(num_cards):
            self.hand.append(Deck.deal())

    def __init__(self, name, num_cards):
        self.name = name
        self.hand = []
        self.make_hand(num_cards)
        self.peg_hand = self.hand
        self.left = len(self.hand)
        self.crib = True
        self.points = 0
        self.points_string = "|"
    
    def __sub__(self, other):
        return self.points - other.points
    
    # Might not be useful?
    def add_points(self, points):
        self.points += points
        self.points_string = " " + self.points_string

    def print_hand(self):
        hand = ""
        for i in range(len(self.hand)):
            hand += f"{i+1}: " + "".join(self.hand[i]) + "  "
        return hand
    
    def __str__(self):
        return f"{self.name}| {self.print_hand()}"

    # Returns INDEX of card chosen for pegging turn
    def ask_card(self) -> int:
        print(f"{self.name}'s hand|  {self.print_hand()}")

        while True:
            card = input("Select a number corresponding to a card in your hand: ")
            if card.isdigit():
                card = int(card)
                if (1 <= card <= len(self.hand)) == True:
                    self.left -= 1
                    return card - 1
                else:
                    print(f"Please enter a number between 1 and {len(self.hand)}")
            else:
                print("Please enter an integer value.")

    # Suggestion: replace self.left to track pegging hand length, not real hand length (which is 4 anyways)
    # STRONG YES FROM ME ATM BUT NOT SURE
    def crib_discard(self, num):
        print("\nDiscard 2 cards for the crib.")
        print("--------------------------------------------------------")

        if self.name == "Computer":
            for i in range(num):
                Game.crib.append(self.hand.pop(randint(0, self.left - 1)))
                self.left -= 1
        else:
            for i in range(num):
                card = self.ask_card()
                Game.crib.append(self.hand.pop(card))

    # Checks if player can go
    def check_over_31(self):
        for card in self.peg_hand:
            if card_convert(card[0]) + Game.peg_count <= 31:
                return True
        return False

    # Double check if this works properly
    # Doesn't keep track of peg hand length
    # FIX SO THAT IT ENSURES YOU PICK A CARD THAT ADDS UP TO LESS THAN 31 IN PEG_SEQUENCE
    # This needs to be fixed.
    def peg_discard(self) -> bool:
        if self.check_over_31() == False:
            return False
        else:
            if self.name == "Computer":
                    card = self.peg_hand.pop(randint(0, self.left - 1))
                    Game.peg_sequence.append(card)
                    Game.peg_count += card_convert(card)

            else:
                card = self.ask_card()
                Game.peg_count += card_convert(self.hand[card])
                Game.peg_sequence.append(self.peg_hand.pop(card))
            return True

def print_main_menu():
    print("---------------------")
    print("       Cribbage      ")
    print("      2 players     ")
    print("   Hand: Rank-Suit")
    print("---------------------")

def print_board(computer, player):
    print(f"Computers points: {computer.points}")
    print(f"Players points: {player.points}")
    print("Computer:")
    print("_________________________________________________________________________________________________________________________END")
    print(f"{computer.points_string}")
    print(f"Player:")
    print(f"{player.points_string}")
    print("_________________________________________________________________________________________________________________________END")

def test_peg_board(string):
    for i in range(121):
        string = " " + string
    print(string)

# Converts a card to its face value
def card_convert(card):
    if card[0] == 'A':
        return 1
    elif card[0] in ['K', 'Q', 'J']:
        return 10
    else:
        return int(card[0])

# Could be a Game method. Easy refactor
def check_of_a_kind_pegging(peg_sequence) -> int:
    tally = 1
    if not len(peg_sequence):
        return
    for i in range(1, len(peg_sequence)):
        if peg_sequence[i][0] == peg_sequence[i-1][0]:
            tally += 1
    return tally


def pegging(computer: Player, player: Player):
    curr = player
    other = computer

    print("--------------------------------------------------------")
    print("                       PEGGING                       ")
    print("--------------------------------------------------------")

    # Remember to reset peg_sequence after every pegging round (A: Done?)
    while computer.left != 0 or player.left != 0:
        # Add logic to handle
        Game.print_peg_sequence()
        print(f"Peg count: {Game.peg_count}")
        of_a_kind = 0 # counts how many pairs/of a kind

        if not curr.peg_discard():
            print(f"{other.name}| Point from the Go!")
            other.add_points(1)
            Game.peg_round_reset()
        else:
            # Checks for pairs
            of_a_kind = check_of_a_kind_pegging(Game.peg_sequence)
            """
                    if Game.peg_sequence[-1][0] == Game.peg_sequence[-2][0]:
                        if Game.peg_sequence[-2][0] == Game.peg_sequence[-3][0]:
                            if Game.peg_sequence[-3][0] == Game.peg_sequence[-4][0]:
                                print(f"{curr.name} | Four of a kind for twelve!")
                                curr.add_points(12)
                            else:
                                print(f"{curr.name} | Three of a kind for six!")
                                curr.add_points(6)
                        else:
                            print(f"{curr.name}| Pair for two!")
                            curr.add_points(2)
                """
            if of_a_kind == 2:
                print(f"{curr.name} | Pair for two!")
                curr.add_points(2)
            elif of_a_kind == 3:
                print(f"{curr.name} | Three of a kind for six!")
                curr.add_points(6)
            elif of_a_kind == 4:
                print(f"{curr.name} | Four of a kind for twelve!")
                curr.add_points(12)

            if Game.peg_count == 15:
                print(f"{curr.name}| Fifteen for 2!")
                curr.add_points(2)

            elif Game.peg_count == 31:
                print(f"{curr.name}| Thirty-one for 2!")
                curr.add_points(2)
                Game.peg_round_reset()

            # Swap pegging turn
        curr, other = other, curr

        
def game(computer, player):
    print_main_menu()

    # This part should be looped for entire 120 point game
    player.crib_discard(DISCARDS)
    computer.crib_discard(DISCARDS)
    Game.get_cut()
    pegging(computer, player)
    Game.print_crib()

p1 = Player("Tyler", 6)
computer = Player("Computer", 6)
game(computer, p1)

'''
# WORKS
# Test for dealing cards + card count (deck class)
deck_example = Deck()
print(f"{deck_example}")
print("-----------------------------")
print(f"DEAL 1: {deck_example.deal()}. {deck_example.left}")
print(f"{deck_example}")
print("-----------------------------")
print(f"DEAL 2: {deck_example.deal()}. {deck_example.left}")
print(f"{deck_example}")

# Test for individual player hand dealing
p1 = Player("Tyler", 4)
for i in range(len(p1.hand)):
    print(p1.hand[i])

print(f"{deck_example}")
'''