# Matthew Polak 300286703

from dataclasses import dataclass
from itertools import combinations
from Poker import PokerGame, Card, get_hand_type, HAND_TYPES


@dataclass(slots=True)
class OmahaHoldem(PokerGame):
	def deal(self):
		# deal 4 cards to each player
		for _ in range(4):
			for i, _ in enumerate(self.players):
				self.add_card(i)

	def hands(self):
		# return the best hand of each player
		return [self.best_hand(p.hand) for p in self.players]

	def best_hand(self, hand: list[Card]) -> str:
		# return the best hand from 2 cards in the player's hand
		# and 3 cards on the table

		# `combinations` returns an iterator of tuples which will
		# be exhausted after the first iteration. we need to
		# convert it to a list so that we can iterate over it
		# multiple times.
		hand_combinations = list(combinations(hand, 2))
		table_combinations = combinations(self.cards, 3)

		all_combinations = (
			list(h + t) for t in table_combinations for h in hand_combinations
		)

		# get the best hand
		best = min(map(get_hand_type, all_combinations))

		return HAND_TYPES[best]
