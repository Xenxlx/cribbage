'''
This is my attempt at making a cribbage game!
'''
import hand_calc
from random import randint
DISCARDS = 2

class Deck:
    cards = [[rank, suit] for suit in hand_calc.SUIT_LST for rank in hand_calc.RANK_LST]
    left = len(cards) # Hardcode to 52 or not?

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
    peg_sequence = [] # FOR KEEPING TRACK OF PEGGING, MIGHT NOT BE NEEDED
    peg_count = 0
    cut = None
    
    @classmethod
    def print_crib(cls):
        hand = ""
        for i in range(len(cls.crib)):
            hand += f"{i+1}: " + "".join(cls.crib[i]) + "  "
        print(hand)
    
    @classmethod
    def get_cut(cls):
        cls.cut = Deck.deal()

    @classmethod
    def round_reset(cls):
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
    def add_point(self):
        self.points += 1
        self.points_string = " " + self.points_string

    def print_hand(self):
        hand = ""
        for i in range(len(self.hand)):
            hand += f"{i+1}: " + "".join(self.hand[i]) + "  "
        return hand
    
    def __str__(self):
        return f"{self.name}| {self.print_hand()}"

    # Returns INDEX of card
    def ask_card(self):
        print(f"{self.name}'s hand|  {self.print_hand()}")

        while True:
            card = input("Select a number corresponding to a card in your hand: ")
            if card.isdigit():
                card = int(card)
                if (1 <= card <= len(self.hand)) == True:
                    return card - 1
                else:
                    print(f"Please enter a number between 1 and {len(self.hand)}")
            else:
                print("Please enter an integer value.")

    # Suggestion: replace self.left to track pegging hand length, not real hand length (which is 4 anyways)
    # PLEASE CONSIDER SHORTLY, STRONG YES FROM ME ATM BUT NOT SURE
    def crib_discard(self, num):
        if self.name == "Computer":
            print("computer discard test")
            for i in range(num):
                Game.crib.append(self.hand.pop(randint(0, self.left - 1)))
                self.left -= 1
        else:
            for i in range(num):
                card = self.ask_card()
                Game.crib.append(self.hand.pop(card))
                self.left -= 1

    # Checks if player can go
    def check_go(self):
        for card in self.peg_hand:
            if card[0] + Game.peg_count <= 31:
                return True
        return False

    # Double check if this works properly
    # Doesn't keep track of peg hand length
    # FIX SO THAT IT ENSURES YOU PICK A CARD THAT ADDS UP TO LESS THAN 31 IN PEG_SEQUENCE
    def peg_discard(self):
        if self.check_go() == False:
            return False

        else:
            if self.name == "Computer":
                    card = self.peg_hand.pop(randint(0, self.left - 1))
                    Game.peg_sequence.append(card)
                    Game.peg_count += card_conv(card)

            else:
                card = self.ask_card()
                Game.peg_count += card_conv(self.hand[card])
                Game.peg_sequence.append(self.peg_hand.pop(card))

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
def card_conv(card):
    if card[0] == 'A':
        return 1
    elif card[0] in ['K', 'Q', 'J']:
        return 10
    else:
        return int(card[0])

def pegging(computer: Player, player: Player):
    curr = player
    other = computer

    # Remember to reset peg_sequence after every pegging round (A: Done?)
    while computer.left != 0 or player.left != 0:
        # CHECK FOR PLAYER WITH A HAND OF 0 CARDS, FIX FUNCTION FOR THAT CASE
        if curr.peg_discard() == False:
            print(f"{other.name}| Point from the Go!")

        if Game.peg_count == 15:
            print(f"{curr.name}| Fifteen for 2!")
            curr.points += 2

        elif Game.peg_count == 31:
            print(f"{curr.name}| Thirty-one for 2!")
            curr.points += 2
            Game.round_reset()

    # Swap discard turn
    curr = other
    if curr.name == "Computer":
        other = player
    else:
        other = computer

        
def game(computer, player):
    print_main_menu()

    # This part should be looped
    player.crib_discard(DISCARDS)
    computer.crib_discard(DISCARDS)
    Game.print_crib()
    Game.get_cut()
    # *call pegging here

p1 = Player("Tyler", 6)
computer = Player("Computer", 6)
game(computer, p1)

'''
# WORKS
# Test unit for dealing cards + card count (deck class)
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