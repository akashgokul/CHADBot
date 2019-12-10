"""
Example usage:

>>> g = Game(3, "Valmik", "Baxter")   # creates a game with 2 players, Valmik and Baxter, each starting with 3 cups
>>> g.remove_cup("Valmik")
>>> g.remove_cup("Valmik")
>>> g.get_score("Valmik")
1
>>> g.get_score("Baxter")
3

---------------------------------------------

Example usage using Game.play():

>>> g = Game(2, "Valmik", "Baxter")
>>> g.play()

It's Valmik's turn.
Did Valmik score? (y/n): y

It's Baxter's turn.
Did Baxter score? (y/n): n
{'Valmik': 1, 'Baxter': 2}

It's Valmik's turn.
Did Valmik score? (y/n): y
Valmik wins.

It's Baxter's turn.
Did Baxter score? (y/n): n
{'Valmik': 0, 'Baxter': 2}
Valmik wins!
{'Valmik': 0, 'Baxter': 2}
'Valmik'

"""


class Game:

	def __init__(self, *args):
		self.scoreboard = {}
		self.start_cups = int(args[0])
		self.winner = None
		self.players = []
		for player in args[1:]:
			self.players.append(player)
			self.scoreboard[player] = self.start_cups


	def remove_cup(self, player):
		if player in self.scoreboard:
			self.scoreboard[player] = self.scoreboard[player] - 1
			if self.scoreboard[player] <= 0:
				self.winner = player
				print(player + " wins.")
				return player
			return None
		return False

	def add_cup(self, player):
		if player in self.scoreboard:
			self.scoreboard[player] = self.scoreboard[player] + 1
			return True
		return False

	def get_score(self, player):
		if player in self.scoreboard:
			return self.scoreboard[player]
		return None

    def cups_consumed(self,player):
        """

        Returns the number of drinks consumed by player.
		ASSUMES 2 PLAYERS!!

        """
        if player in self.scoreboard:
			opponent_lst = [opponent for opponent in self.players if opponent != player]
			opponent_score = sum([self.scoreboard[opponent] for opponent in opponent_lst])
			return self.start_cups - opponent_score
        else:
            return None

	def play(self):
		"""
		Optional play function for simulation purposes.

		"""
		while self.winner == None:
			for player in self.scoreboard.keys():
				print('')
				print("It's " + player + "'s turn.")
				hit = raw_input("Did " + player + " score? (y/n): ")
				if hit == "y":
					self.remove_cup(player)
			print(self.scoreboard)

		print(self.winner + " wins!")
		print(self.scoreboard)
		return self.winner
