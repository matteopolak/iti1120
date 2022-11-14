from collections import defaultdict
from utils import get_next_type

# instantiates value with a list if it doesn't exist
teams = defaultdict[str, list[str]](list)
players = dict[str, str]()

# get number of players
n = get_next_type('Provide the number of players: ', int, lambda n: n >= 0)

for i in range(1, n + 1):
	name = input(f'Name of player {i}: ')
	team = input(f'Team of player {i}: ')

	# add player to team
	teams[team].append(name)
	players[name] = team

# print result
print(players)
print(dict(teams))
