# Matthew Polak 300286703

from dataclasses import dataclass
from itertools import combinations
from Poker import Card, get_hand_type, HAND_TYPES, PokerGame


@dataclass(slots=True)
class TexasHoldem(PokerGame):
	def deal(self):
		# deal 2 cards to each player and 5 cards to the table
		for _ in range(2):
			for i, _ in enumerate(self.players):
				self.add_card(i)

		for _ in range(5):
			self.add_to_table()

	def hands(self):
		# return the best hand of each player
		return [self.best_hand(p.hand) for p in self.players]

	def best_hand(self, hand: list[Card]) -> str:
		# return the best hand from 2 cards in the player's hand
		# and 5 cards on the table

		all_combinations = (
			list(c) for c in combinations(hand + self.cards, 5)
		)

		# get the best hand
		best = min(map(get_hand_type, all_combinations))

		return HAND_TYPES[best]
