'''
This is my attempt at making a cribbage score calculator

'''
from itertools import combinations

# Card class (card1 = Card(rank, suit)), NOT USED CURRENTLY
# I'll come back if I learn how to implement OOP in this program
'''class Card:
    def __init__(self, rank, suit):
        self.rank = get_hand()
        self.suit = suit


card1 = Card(7, 'Hearts')'''


def get_hand():
    card_number = 0
    hand = []
    rank_lst = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
    suit_lst = ['H', 'D', 'S', 'C']

    while len(hand) <= 4:  # Assuming a hand of 4 cards, 4 player game
        card_number += 1

        while True:  # Inputting rank
            rank = input("Enter the rank of card " + str(card_number) + ": ")

            if rank in rank_lst:  # Checks if rank is valid input AND .isdigit()

                if rank.isdigit():
                    rank = int(rank)
                break
            else:
                print("Rank must be a number between 1-10 or J, Q or K for face cards. ")

        while True:  # Inputting suit
            suit = input("Enter the suit of card " + str(card_number) + ": ")

            if suit not in suit_lst:
                print("Suit must be H, D, S or C.")
            else:
                break

        hand.append([rank, suit])

    print(hand)
    return hand


'''
# REFERENCE ONLY, DELETE AFTER SELF CONFIRMATION
def get_hand():
    hand = []
    card_number = 1

    # Assuming a hand of 4 cards, 4 player game
    while len(hand) <= 4:
        hand.append(get_cards(card_number))
        card_number += 1

    return hand
'''


def calculator():
    points = 0
    hand = get_hand()

    # Pair calculator (Before preprocessing for printing purposes)
    for i in range(len(hand) - 1):
        for j in range(i + 1, len(hand)):
            if hand[j][0] == hand[i][0]:
                points += 2
                print(f"Pair of {hand[j][0]}'s!")


    # HAND PREPROCESSING - Face cards in order (for runs)
    for i in range(len(hand)):
        if hand[i][0] == 'A':
            hand[i][0] = 1

        elif hand[i][0] == 'J':
            hand[i][0] = 11

        elif hand[i][0] == 'Q':
            hand[i][0] = 12

        elif hand[i][0] == 'K':
            hand[i][0] = 13


    # Sorting for calculator (sorts by suit + rank)
    sorted_hand = sorted(hand)  # Sort by suit would be useful for Gin Rummy calculator

    # Remove + track duplicates for runs
    i = 0
    duplicate_rank = {}

    while i < len(sorted_hand) - 1:
        if sorted_hand[i][0] == sorted_hand[i+1][0]:
            if duplicate_rank.get(sorted_hand[i][0]) is not None:
                duplicate_rank[sorted_hand[i][0]] += 1

            else:
                duplicate_rank[sorted_hand[i][0]] = 2

            sorted_hand.remove(sorted_hand[i])

        else:
            i += 1

    print(f'Final sorted hand : {sorted_hand}')
    print(f'Duplicate_rank: {duplicate_rank}')

    # Runs calculator
    run_length = 1
    i = 0
    multiplier = 0
    
    while i < len(sorted_hand) - 1:
        if sorted_hand[i][0] + 1 == sorted_hand[i + 1][0]:
            run_length += 1

            if duplicate_rank.get(sorted_hand[i][0]) is not None:
                multiplier += duplicate_rank[sorted_hand[i][0]]

            if run_length == len(sorted_hand):
                if multiplier > 0:
                    points += len(sorted_hand) * multiplier
                    print(f'{multiplier} run of: {run_length}')
                else:
                    points += len(sorted_hand)
                    print(f'Run of: {run_length}')
                break

        else:   # When run is finished
            if run_length > 2:
                if multiplier > 0:
                    points += run_length * multiplier
                    print(f'{multiplier} run of: {run_length}')
                else:
                    points += run_length
                    print(f'Run of: {run_length}')
            run_length = 1
            multiplier = 0

        i += 1

    # Flush (4-5 same suit cards) calc FIX
    suit_length = 1
    suit_hand = sorted(hand, key=lambda card: card[1])  # Sorts by suit
    print(f'Suit hand: {suit_hand}')

    i = 0
    while i < len(suit_hand) - 1:
        if suit_hand[i][1] == suit_hand[i + 1][1]:
            suit_length += 1

        else:   # When suit run is finished
            if suit_length > 3:
                points += suit_length
                print(f'Flush of {suit_length} cards!')

            suit_length = 1

        i += 1
    print(f'Suit length: {suit_length}')

    # HAND PREPROCESSING - Face cards to values
    for i in range(len(hand)):  # Convert face cards to respective values
        if type(hand[i][0]) != int:
            if 10 < hand[i][0] < 14:
                hand[i][0] = 10

        else:
            hand[i][0] = int(hand[i][0])

    # Fifteens calc
    for r in range(2, 6):
        for comb in combinations(hand, r):
            print(comb)
            if sum(card[0] for card in comb) == 15:
                print('15 for 2!')
                points += 2

    print(f'Points: {points}')


calculator()
