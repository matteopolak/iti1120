# Matthew Polak 300286703

import unittest

from omaha import OmahaHoldem
from Poker import Card, DECK, Player, PokerGame
from texas import TexasHoldem

CARDS = {card: Card.from_string(card) for card in DECK}


def batch_cards(cards: list[str]):
	return [CARDS[card] for card in cards]


def create_omaha(n=1):
	return OmahaHoldem(n)


def create_poker(n=1):
	return PokerGame(n)


def create_texas(n=1):
	return TexasHoldem(n)


class TestCardMethods(unittest.TestCase):
	def test_straight_flush(self):
		game = create_poker()

		self.assertEqual(
			True,
			game.IsStraightFlush(batch_cards(['AH', '2H', '3H', '4H', '5H']))
		)

		self.assertEqual(
			True,
			game.IsStraightFlush(batch_cards(['TS', 'JS', 'QS', 'KS', 'AS']))
		)

		self.assertEqual(
			True,
			game.IsStraightFlush(batch_cards(['7D', '9D', 'JD', 'TD', '8D']))
		)

		self.assertEqual(
			False,
			game.IsStraightFlush(batch_cards(['8C', '9C', 'TC', '2C', '3C']))
		)

	def test_four_of_a_kind(self):
		game = create_poker()

		self.assertEqual(
			True,
			game.IsFourofaKind(batch_cards(['9H', '6S', '9D', '9C', '9S']))
		)

		self.assertEqual(
			False,
			game.IsFourofaKind(batch_cards(['2H', '6S', '5H', '8C', '9S']))
		)

	def test_full_house(self):
		game = create_poker()

		self.assertEqual(
			True,
			game.IsFullHouse(batch_cards(['JH', '7S', '7D', 'JD', 'JC']))
		)

		self.assertEqual(
			False,
			game.IsFullHouse(batch_cards(['2H', '6D', '5D', '8C', '8S']))
		)

	def test_flush(self):
		game = create_poker()

		self.assertEqual(
			True, game.IsFlush(batch_cards(['JH', '7H', '8H', '2H', '5H']))
		)

		self.assertEqual(
			False, game.IsFlush(batch_cards(['3D', '6D', '3H', '8C', '8S']))
		)

	def test_straight(self):
		game = create_poker()

		self.assertEqual(
			True, game.IsStraight(batch_cards(['AD', '2S', '3D', '4C', '5H']))
		)

		self.assertEqual(
			True, game.IsStraight(batch_cards(['TS', 'JS', 'QH', 'KH', 'AC']))
		)

		self.assertEqual(
			True, game.IsStraight(batch_cards(['7S', '9D', 'JD', 'TH', '8H']))
		)

		self.assertEqual(
			False,
			game.IsStraight(batch_cards(['8C', '9D', 'TC', '2D', '3H']))
		)

	def test_three_of_a_kind(self):
		game = create_poker()

		self.assertEqual(
			True,
			game.IsThreeofaKind(batch_cards(['TH', '6S', 'TD', 'TC', 'QS']))
		)

		self.assertEqual(
			False,
			game.IsThreeofaKind(batch_cards(['2H', '6S', 'KH', '8C', 'QS']))
		)

	def test_two_pair(self):
		game = create_poker()

		self.assertEqual(
			True, game.IsTwoPairs(batch_cards(['TH', '6S', 'AS', 'TC', '6D']))
		)

		self.assertEqual(
			False,
			game.IsTwoPairs(batch_cards(['2H', '6S', '9H', '8C', 'QS']))
		)

	def test_one_pair(self):
		game = create_poker()

		self.assertEqual(
			True, game.IsOnePair(batch_cards(['TH', '6S', 'AS', 'KC', 'KD']))
		)

		self.assertEqual(
			False, game.IsOnePair(batch_cards(['2H', '6S', '9H', '8C', 'QS']))
		)


class TestGameCalculations(unittest.TestCase):
	def test_texas(self):
		game = create_texas(2)
		game.players = [
			Player('Player 1', batch_cards(['JD', 'KS'])),
			Player('Player 2', batch_cards(['JH', 'TC'])),
		]
		game.cards = batch_cards(['2C', 'JC', 'KD', '5C', 'AC'])

		self.assertEqual(['Two Pairs', 'Flush'], game.hands())

	def test_omaha(self):
		game = create_omaha(2)
		game.players = [
			Player('Player 1', batch_cards(['JD', 'KS', '2D', 'KH'])),
			Player('Player 2', batch_cards(['JH', 'JS', 'AH', 'TC'])),
			Player('Player 3', batch_cards(['3D', '4S', '6H', '9C'])),
		]
		game.cards = batch_cards(['2C', 'JC', 'KD', '5C', '2H'])

		self.assertEqual(
			# these are corrected answers, the ones provided in the task are wrong
			['Full House', 'Full House', 'Pair'],
			game.hands()
		)


if __name__ == '__main__':
	unittest.main()
