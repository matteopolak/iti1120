# Matthew Polak 300286703

from dataclasses import dataclass, field
from enum import Enum
from random import shuffle
from typing import TypeAlias

Hand: TypeAlias = tuple['Card', 'Card', 'Card', 'Card', 'Card']

# yapf: disable
DECK = (
	"2C", "2D", "2H", "2S",
	"3C", "3D", "3H", "3S",
	"4C", "4D", "4H", "4S",
	"5C", "5D", "5H", "5S",
	"6C", "6D", "6H", "6S",
	"7C", "7D", "7H", "7S",
	"8C", "8D", "8H", "8S",
	"9C", "9D", "9H", "9S",
	"TC", "TD", "TH", "TS",
	"JC", "JD", "JH", "JS",
	"QC", "QD", "QH", "QS",
	"KC", "KD", "KH", "KS",
	"AC", "AD", "AH", "AS",
)
# yapf: enable


@dataclass(slots=True)
class Card:
	type: 'CardType'
	suit: 'CardSuit'
	value: int = field(default=0)

	def __post_init__(self):
		if self.value == 0:
			self.value = self.type.value[1]

	def __gt__(self, other: 'Card'):
		return self.value > other.value

	def __lt__(self, other: 'Card'):
		return self.value < other.value

	def __eq__(self, other: 'Card'):
		if self.type == CardType.ACE:
			return self.value == other.value or other.value == 1

		if other.type == CardType.ACE:
			return self.value == other.value or self.value == 1

		return self.value == other.value

	def __ge__(self, other: 'Card'):
		return self.value >= other.value

	def __le__(self, other: 'Card'):
		return self.value <= other.value

	def __add__(self, other: 'Card'):
		return Card(self.type, self.suit, self.value + other.value)

	def __str__(self):
		return self.type.name

	def __repr__(self):
		return f'{self.type.value[0]}{self.suit.value}'

	@staticmethod
	def from_string(card: str):
		return Card(
			CardType.from_string(card[0]), CardSuit.from_string(card[1])
		)


class CardSuit(Enum):
	CLUB = 'C'
	DIAMOND = 'D'
	HEART = 'H'
	SPADE = 'S'

	@staticmethod
	def from_string(suit: str):
		match suit:
			case 'C':
				return CardSuit.CLUB
			case 'D':
				return CardSuit.DIAMOND
			case 'H':
				return CardSuit.HEART
			case 'S':
				return CardSuit.SPADE
		
		raise ValueError(f'Invalid suit: {suit}')


class CardType(Enum):
	TWO = ('2', 2)
	THREE = ('3', 3)
	FOUR = ('4', 4)
	FIVE = ('5', 5)
	SIX = ('6', 6)
	SEVEN = ('7', 7)
	EIGHT = ('8', 8)
	NINE = ('9', 9)
	TEN = ('T', 10)
	JACK = ('J', 11)
	QUEEN = ('Q', 12)
	KING = ('K', 13)
	ACE = ('A', 14)

	@staticmethod
	def from_string(card: str):
		match card:
			case '2':
				return CardType.TWO
			case '3':
				return CardType.THREE
			case '4':
				return CardType.FOUR
			case '5':
				return CardType.FIVE
			case '6':
				return CardType.SIX
			case '7':
				return CardType.SEVEN
			case '8':
				return CardType.EIGHT
			case '9':
				return CardType.NINE
			case 'T':
				return CardType.TEN
			case 'J':
				return CardType.JACK
			case 'Q':
				return CardType.QUEEN
			case 'K':
				return CardType.KING
			case 'A':
				return CardType.ACE

		raise ValueError(f'Invalid card: {card}')


@dataclass(slots=True)
class Player:
	name: str
	hand: list[Card]

	def __str__(self):
		return self.name


@dataclass(slots=True)
class PokerGame:
	n_players: int = field(default=2)
	cards: list[Card] = field(init=False)
	players: list[Player] = field(init=False)
	deck: list[Card] = field(init=False)

	def __post_init__(self):
		self.players = [
			Player(f'Player {i + 1}', []) for i in range(self.n_players)
		]

		self.cards = []

		# create and shuffle deck
		self.deck = [Card.from_string(c) for c in DECK]
		shuffle(self.deck)

	def add_card(self, p_index: int, /):
		self.players[p_index].hand.append(self.deck.pop())

	def add_to_table(self):
		self.cards.append(self.deck.pop())

	def IsFlush(self, hand: list[Card]) -> bool:
		if len(hand) != 5:
			return False

		# check if all cards have the same suit
		return all(hand[0].suit.name == c.suit.name for c in hand)

	def IsStraight(self, hand: list[Card]) -> bool:
		if len(hand) != 5:
			return False

		if any(map(lambda c: c.type == CardType.ACE, hand)):
			# check for ace low straight
			ace_low = [CardType.TWO, CardType.THREE, CardType.FOUR,
					   CardType.FIVE, CardType.ACE]

			if all(map(lambda c: c.type in ace_low, hand)):
				return True

		# sort hand
		hand.sort()

		# check if all cards are in a row
		# adding a random card with a value of -1 will decrease hand[i + 1] by 1
		# so we can see if it's a straight
		#
		# this is kind of hacky, but it doesn't really matter
		return all(hand[i] == hand[i + 1] + Card(CardType.ACE, CardSuit.CLUB, -1) for i in range(4))

	def IsStraightFlush(self, hand: list[Card]) -> bool:
		if len(hand) != 5:
			return False

		# check for flush
		if not self.IsFlush(hand):
			return False

		# check for straight
		if not self.IsStraight(hand):
			return False

		return True

	def IsFourofaKind(self, hand: list[Card]) -> bool:
		if len(hand) != 5:
			return False

		# sort hand
		hand.sort()

		# check if there are 4 cards with the same value
		return any(hand[i].value == hand[i + 3].value for i in range(2))

	def IsFullHouse(self, hand: list[Card]) -> bool:
		if len(hand) != 5:
			return False

		# sort hand
		hand.sort()

		# check if there are 3 cards with the same value
		for i in range(3):
			if hand[i].value == hand[i + 2].value:
				# check if there are 2 cards with the same value
				for j in range(4):
					if j not in range(i, i + 3):
						if hand[j].value == hand[j + 1].value:
							return True

		return False

	def IsThreeofaKind(self, hand: list[Card]) -> bool:
		if len(hand) != 5:
			return False

		# sort hand
		hand.sort()

		# check if there are 3 cards with the same value
		return any(hand[i].value == hand[i + 2].value for i in range(3))

	def IsTwoPairs(self, hand: list[Card]) -> bool:
		if len(hand) != 5:
			return False

		# sort hand
		hand.sort()

		pairs = 0

		for i in range(4):
			if hand[i].value == hand[i + 1].value:
				pairs += 1
				i += 1

		return pairs == 2

	def IsOnePair(self, hand: list[Card]) -> bool:
		if len(hand) != 5:
			return False

		# sort hand
		hand.sort()

		# check if there are 2 cards with the same value
		return any(hand[i].value == hand[i + 1].value for i in range(4))


DEFAULT_GAME = PokerGame()

HAND_TYPES = (
	'Straight Flush', 'Four of a Kind', 'Full House', 'Flush', 'Straight',
	'Three of a Kind', 'Two Pairs', 'Pair', 'High Card'
)

HAND_ORDER = [
	DEFAULT_GAME.IsStraightFlush,
	DEFAULT_GAME.IsFourofaKind,
	DEFAULT_GAME.IsFullHouse,
	DEFAULT_GAME.IsFlush,
	DEFAULT_GAME.IsStraight,
	DEFAULT_GAME.IsThreeofaKind,
	DEFAULT_GAME.IsTwoPairs,
	DEFAULT_GAME.IsOnePair,
]


def get_hand_type(hand: list[Card]) -> int:
	'''
	Returns the type of hand and the highest card in the hand if it is
	not a special hand.
	'''
	# use a generator so we don't evaluate all the functions
	# if we don't have to
	it = (fn(hand) for fn in HAND_ORDER)

	for i, result in enumerate(it):
		if result:
			return i

	# return value of highest card
	return len(HAND_ORDER)
