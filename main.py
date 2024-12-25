'''
This is my attempt at making a cribbage score calculator

'''
from itertools import combinations
# Can make these lists dictionaries mapped to their respective values (K = 13)
rank_lst = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
suit_lst = ['H', 'D', 'S', 'C']

# Card class (card1 = Card(rank, suit)), NOT USED CURRENTLY
# I'll come back if I learn how to implement OOP in this program
'''class Card:
    def __init__(self, rank, suit):
        self.rank = get_hand()
        self.suit = suit


card1 = Card(7, 'Hearts')'''

def get_cut():
    while True:
        rank = input("Enter the rank of the cut card: ").upper()
        if rank in rank_lst:
            if rank.isdigit():
                rank = int(rank)
            break
        else:
            print("Rank must be a number between 2-10 or A, J, Q or K.")

    while True:
            suit = input("Enter the suit of the cut card: ").upper()

            if suit not in suit_lst:
                print("Suit must be H, D, S or C.")
            else:
                break

    return rank, suit

def get_hand():
    card_number = 1
    hand = []

    while len(hand) < 4:  # Assuming a hand of 4 cards, 4 player game
        while True:  # Inputting rank
            rank = input("Enter the rank of card " + str(card_number) + ": ").upper()

            if rank in rank_lst:  # Checks if rank is valid input AND .isdigit()
                if rank.isdigit():
                    rank = int(rank)
                break
            else:
                print("Rank must be a number between 2-10 or A, J, Q or K.")

        while True:  # Inputting suit
            suit = input("Enter the suit of card " + str(card_number) + ": ").upper()

            if suit not in suit_lst:
                print("Suit must be H, D, S or C.")
            else:
                break

        hand.append([rank, suit])
        card_number += 1

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

def pair_calc(hand):
    points = 0
    for i in range(len(hand) - 1):
        for j in range(i + 1, len(hand)):
            if hand[j][0] == hand[i][0]:
                points += 2
                print(f"Pair of {hand[j][0]}'s!")
    return points

def fifteen_calc(hand):
    points = 0
    for r in range(2, 6):
        for comb in combinations(hand, r):
            print(comb)
            if sum(card[0] for card in comb) == 15:
                print('15 for 2!')
                points += 2
    return points

def flush_calc(hand):
    # Flush (4-5 same suit cards) calc FIX
    suit_length = 1
    suit_hand = sorted(hand, key=lambda card: card[1])  # Sorts by suit
    print(f'Suit hand: {suit_hand}')

    i = 0
    while i < len(suit_hand) - 1:
        if suit_hand[i][1] == suit_hand[i + 1][1]:
            suit_length += 1
        i += 1
    
    if suit_length > 3:
        points += suit_length
        print(f'Flush of {suit_length} cards!')

    print(f'Suit length: {suit_length}')


def calculator():
    points = 0
    cut_rank, cut_suit = get_cut()
    hand = get_hand()
    hand.append([cut_rank, cut_suit])

    # points = cut_calc + pair_calc(hand) + run_calc + flush_calc + fifteens_calc // AT THE END

    # Cut calculator
    if cut_rank == 'J':
        points += 1
    
    for i in range(len(hand)):
        if hand[i][0] == 'J' and hand[i][1] == cut_suit:
            points += 1

    # HAND PREPROCESSING - Face cards in order (for runs & fifteens)
    for i in range(len(hand)):
        if hand[i][0] == 'A':
            hand[i][0] = 1

        elif hand[i][0] == 'J':
            hand[i][0] = 11

        elif hand[i][0] == 'Q':
            hand[i][0] = 12

        elif hand[i][0] == 'K':
            hand[i][0] = 13


    # Sorting for runs calculator (sorts by suit + rank)
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

    # HAND PREPROCESSING - Convert face cards to value of 10
    i = 0
    for i in range(len(hand)):
        if 10 < hand[i][0] < 14:
            hand[i][0] = 10
            print(hand[i][0])

        else:
            hand[i][0] = int(hand[i][0])

    # ADD RUNS CALCULATOR FUNCTION THEN WE'RE GOLDEN
    points += fifteen_calc(hand) + flush_calc(hand)

    print(f'Points: {points}')


calculator()
