import random
import time
from collections import Counter
import math

RANKS = '23456789TJQKA'
SUITS = 'cdhs'
DECK = [r + s for r in RANKS for s in SUITS]

def get_deck(exclude):
    return [card for card in DECK if card not in exclude]

def draw_random_cards(deck, num):
    return random.sample(deck, num)

def evaluate_hand(hand):
    ranks = sorted([RANKS.index(c[0]) for c in hand], reverse=True)
    suits = [c[1] for c in hand]
    flush = len(set(suits)) == 1
    straight = all(ranks[i] - 1 == ranks[i+1] for i in range(len(ranks) - 1))
    counts = Counter(ranks).most_common()

    if flush and straight:
        return (8, ranks[0])  # Straight flush
    if counts[0][1] == 4:
        return (7, counts[0][0])  # Four of a kind
    if counts[0][1] == 3 and counts[1][1] == 2:
        return (6, counts[0][0])  # Full house
    if flush:
        return (5, ranks)  # Flush
    if straight:
        return (4, ranks[0])  # Straight
    if counts[0][1] == 3:
        return (3, counts[0][0])  # Three of a kind
    if counts[0][1] == 2 and counts[1][1] == 2:
        return (2, max(counts[0][0], counts[1][0]))  # Two pair
    if counts[0][1] == 2:
        return (1, counts[0][0])  # One pair
    return (0, ranks)  # High card

class Node:
    def __init__(self):
        self.visits = 0
        self.wins = 0

    def ucb1(self, total_simulations):
        if self.visits == 0:
            return float('inf')
        return (self.wins / self.visits) + math.sqrt(2 * math.log(total_simulations) / self.visits)

class PokerBot:
    def __init__(self, hole_cards, community_cards):
        self.hole_cards = hole_cards
        self.community_cards = community_cards
        self.start_time = time.time()
        self.time_limit = 9.5  # seconds

    def simulate(self, stay=True):
        used = self.hole_cards + self.community_cards
        deck = get_deck(used)
        opp_hole = draw_random_cards(deck, 2)
        remaining = draw_random_cards(get_deck(used + opp_hole), 5 - len(self.community_cards))
        final_community = self.community_cards + remaining

        if not stay:  # Simulate folding as a neutral move
            return 0.5

        my_hand = self.hole_cards + final_community
        opp_hand = opp_hole + final_community

        my_score = evaluate_hand(my_hand)
        opp_score = evaluate_hand(opp_hand)

        if my_score > opp_score:
            return 1
        elif my_score == opp_score:
            return 0.5
        else:
            return 0

    def decide(self):
        stay_node = Node()
        fold_node = Node()  # Always returns 0.5 for folding (neutral decision)
        nodes = [stay_node, fold_node]
        simulations = 0

        while time.time() - self.start_time < self.time_limit:
            total_simulations = sum(n.visits for n in nodes)

            # Select the best node (stay vs fold) using UCB1
            chosen_node = max(nodes, key=lambda n: n.ucb1(total_simulations))

            if chosen_node is stay_node:
                reward = self.simulate(stay=True)
            else:
                reward = self.simulate(stay=False)

            chosen_node.visits += 1
            chosen_node.wins += reward
            simulations += 1

        stay_win_rate = stay_node.wins / stay_node.visits
        fold_win_rate = fold_node.wins / fold_node.visits
        print(f"STAY win rate: {stay_node.wins}/{stay_node.visits} = {stay_win_rate:.2f}")
        print(f"FOLD win rate: {fold_node.wins}/{fold_node.visits} = {fold_win_rate:.2f}")

        if stay_win_rate >= 0.5:
            return "STAY"
        else:
            return "FOLD"

if __name__ == "__main__":

    hole_cards = ['Ah', 'Kd']
    community_cards = ['Qs', 'Jc', 'Th']
    bot = PokerBot(hole_cards, community_cards)
    print("Test 1:", hole_cards, "+", community_cards)
    print("Bot decision:", bot.decide())
   

    hole_cards = ['2h', '7d']
    community_cards = ['Ks', 'Qd', '9c']
    bot = PokerBot(hole_cards, community_cards)
    print("Test 2:", hole_cards, "+", community_cards)
    print("Bot decision:", bot.decide())


    hole_cards = ['Ah', '3h']
    community_cards = ['Kh', '9h', '2s']
    bot = PokerBot(hole_cards, community_cards)
    print("Test 3:", hole_cards, "+", community_cards)
    print("Bot decision:", bot.decide())


    hole_cards = ['9h', '9d']
    community_cards = ['9s', 'Jc', 'Js']
    bot = PokerBot(hole_cards, community_cards)
    print("Test 4:", hole_cards, "+", community_cards)
    print("Bot decision:", bot.decide())


    hole_cards = ['Ad', 'Qh']
    community_cards = ['Qc', '7d', '2s']
    bot = PokerBot(hole_cards, community_cards)
    print("Test 5:", hole_cards, "+", community_cards)
    print("Bot decision:", bot.decide())

    hole_cards = ['6c', '2h']
    community_cards = ['9d', '6d', 'Jc']
    bot = PokerBot(hole_cards, community_cards)
    print("Test 6:", hole_cards, "+", community_cards)
    print("Bot decision:", bot.decide())

    hole_cards = ['8h', '7d']
    community_cards = ['9c', '6s', '5h']
    bot = PokerBot(hole_cards, community_cards)
    print("Test 7:", hole_cards, "+", community_cards)
    print("Bot decision:", bot.decide())
