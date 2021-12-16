#!/usr/bin/env python3

#Copyright 2021 Noah Panepinto
	#Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
	#The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
	#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

#This is a blackjack game called BlackPack. It has a few cool features, including using multiple decks, autoshuffling, and betting. 
	#This is my ONLINE blackjack game.
	#It's written in python3 and depends on random and socket, this is the linux version, it should however run on windows or macos when opened in a python interpreter. 
	#It can be installed on linux by placing the file in /usr/bin or any prefered bin folder, and can be ran by calling BlackPackO in bash.

from random import randint
import xml.etree.ElementTree as ET
import socket

HOST = '127.0.0.1'
SERV = 65533
LIST = 65532

#[Noah Panepinto (Dec.16 2021 {01:39})]
	#Here I define several characters that will be appended to strings to chang their colours when printed.

class colours:
	ENDC                = '\033[0m'

	BOLD                = '\033[1m'
	UNDER               = '\033[4m'
	NO_UNDER            = '\033[24m'
	REVERSE             = '\033[7m'
	FOREWARD            = '\033[27m'

	FORE_DARK_BLACK     = '\033[30m'
	FORE_DARK_RED       = '\033[31m'
	FORE_DARK_GREEN     = '\033[32m'
	FORE_DARK_ORANGE    = '\033[33m'
	FORE_DARK_BLUE      = '\033[34m'
	FORE_DARK_MAGENTA   = '\033[35m'
	FORE_DARK_CYAN      = '\033[36m'
	FORE_DARK_WHITE     = '\033[37m'

	FORE_BRIGHT_BLACK   = '\033[90m'
	FORE_BRIGHT_RED     = '\033[91m'
	FORE_BRIGHT_GREEN   = '\033[92m'
	FORE_BRIGHT_ORANGE  = '\033[93m'
	FORE_BRIGHT_BLUE    = '\033[94m'
	FORE_BRIGHT_MAGENTA = '\033[95m'
	FORE_BRIGHT_CYAN    = '\033[96m'
	FORE_BRIGHT_WHITE   = '\033[97m'

	BACK_ENDC           = '\033[0m'
	BACK_DARK_BLACK     = '\033[40m'
	BACK_DARK_RED       = '\033[41m'
	BACK_DARK_GREEN     = '\033[42m'
	BACK_DARK_ORANGE    = '\033[43m'
	BACK_DARK_BLUE      = '\033[44m'
	BACK_DARK_MAGENTA   = '\033[45m'
	BACK_DARK_CYAN      = '\033[46m'
	BACK_DARK_WHITE     = '\033[47m'

	BACK_BRIGHT_BLACK   = '\033[1000m'
	BACK_BRIGHT_RED     = '\033[101m'
	BACK_BRIGHT_GREEN   = '\033[102m'
	BACK_BRIGHT_ORANGE  = '\033[103m'
	BACK_BRIGHT_BLUE    = '\033[104m'
	BACK_BRIGHT_MAGENTA = '\033[105m'
	BACK_BRIGHT_CYAN    = '\033[106m'
	BACK_BRIGHT_WHITE   = '\033[107m'

#[Noah Panepinto (Oct.3 2021 {01:39})]
	#Here I define the classes that will represent Standard Cards (the BaseCard class) and Ace Cards (the AceCard class)
		#Both the AceCard class is derived from the BaseCard class and as a result contain the same five non static (instance) values):
			#self.value; An integer value representing the total added to your hand under normal circumstances:
				#Used for comparing whether a hand of two cards can be split or not.
			#self.suite; A string value representing the suite of a card, "Spades", "Clubs", "Hearts", or "Diamonds".
			#self.card; A string value representing the number or face of a card, "Two", "Eight", "Ace", "King" etc.
			#self.name; A string value representing the name of a card:
				#It is equal to "X of Y" where X is self.card and Y is self.suite.
			#self.face; An array of string values which is used to visually represent a card when printed.
		#Both the BaseCard class and AceCard class contain one function:
			#GetValue(); A function which returns the value a card will add to a hand:
				#Takes in the current value of your hand as input value score.
				#Returns self.value.
		#The AceCard class differs from the BaseCard class in three ways:
			#self.value is not supplied upon instantiation and is always equal to 11.
			#self.card is not supplied upon instantiation and is always equal to "Ace".
			#GetValue() will return 1 if score is greater than 10, and 11 if score is less than or equal to 10.

class BaseCard:
	def __init__(self, v, n, f):
		self.value = v
		self.name = n
		self.face = f
	def GetValue(self, score):
		return(self.value)
	def __str__(self):
		r = ""
		i = 0
		for line in self.face:
			if not i == 0:
				r += '\n'
			r += line
			i += 1
		return r

class AceCard(BaseCard): 
	def __init__(self, n, f):
		self.name = n
		self.face = f
	def GetValue(self, score):
		if( score > 10 ):
			return 1
		else:
			return 11

#[Noah Panepinto (Dec.16 2021 {01:30})]
	#Here I define a static class containing all of the data for a full deck of cards, including the string representation of the back of a card.
		#The Cards class contains two static (class) values:
			#Cards.fd; an array containing BaseCard and AceCard Class Objects representing a full standard deck of playing cards.
			#Cards.boc; an array of strings representing the back of a standard playing card.
		#The Cards class contains one function, Load() which reads an XML File and populates Cards.fd and Cards.boc with the data within the XML File.

class Cards:
	fd = []
	boc = []
	def Load(xmlFile):
		full = []
		back = []
		tree = ET.parse(xmlFile)
		root = tree.getroot()
		i = 0
		for item in root.findall('card'):
			if item.find('ID').text == 'back':
				faceX = item.find('face')
				for line in faceX.findall('line'):
					back.append(line.text)
			elif item.find('ID').text == 'ace':
				faceX = item.find('face')
				face = []
				for line in faceX.findall('line'):
					face.append(line.text)
				name = item.find('description').text
				full.append(AceCard(name, face))
			elif item.find('ID').text == 'base':
				value = int(item.find('value').text)
				faceX = item.find('face')
				face = []
				for line in faceX.findall('line'):
					face.append(line.text)
				name = item.find('description').text
				full.append(BaseCard(value, name, face))
			else: i += 1
		if i > 0:
			print('invalid Cards.xml')
			exit(0)
		Cards.fd = full
		Cards.boc = back

#[Noah Panepinto (Oct.3 2021 {01:39})]
	#Here I define the class which will represent a deck of cards (the Deck class) which contains two static (class) values:
		#inPile; An Array of AceCard and BaseCard classes which represents the pile in which cards are shuffled and waiting to be dealt to players.
		#outPile; An array of AceCard and BaseCard classes which represents the pile in which cards that have been discarded and are waiting to be reshuffled into inPile.
	#The Deck Class contains no non static (instance) values. 
	#The Deck Class contains one function:
		#shuffle(); A function which takes all cards in outPile and moves them into inPile.

class Deck:
	inPile  = []
	outPile = []
	def __init__(self, decks):
		i = 0
		while i < decks:
			self.inPile.extend(Cards.fd)
			i += 1
	def shuffle(self):
		print("\nShufflin' the deck!")
		while len(self.outPile) > 0:
			self.inPile.append(self.outPile.pop(0))

#[Noah Panepinto (Oct.3 2021 {01:39})]
	#Here I define the the class which will represent a hand of cards held by a player (the Hand class) which contains three non static (instance) values:
		#self.score; The integer value which represents the point value of the hand, this is what you're trying to get to 21.
		#self.cards; An Array of BaseCards and AceCards that the hand contains.
		#self.doubled; A boolean value that checks whether a hand has been double downed, and can resultingly no longer hit.
	#The Hand class also contains six functions:
		#print(); A function which prints the visual representations of the cards that the Hand class contains,
			#the data printed is contained in BaseCard.face, and AceCard.face.
		#printHalf(); A function which prints the visual representation of the first card in the hand and then boc.
		#evalAceLast(); A function which evaluates and populates self.score, 
			#it does this by running the GetValue() function on all BaseCard classes within self.cards followed by doing the same for all AceCard classes within self.cards.
			#The order of operations is important to make sure that the AceCard classes return the correct value.
			#Returns self.score.
		#hit(); A function which takes a random card from the inPile value of a Deck class object and adds it to self.cards.
			#Takes in a Deck class object from which to take a card.
		#deal(); A function which calls the hit() function twice.
			#Takes in a Deck class object which is needed for passing to the hit() function.
		#clear(); A function which takes all cards in self.cards and moves them to the outPile value of a Deck class object.
			#Takes in a Deck class object to which it gives cards.

class Hand:
	def __init__(self):
		self.score = 0
		self.cards = []
		self.doubled = False
	def print(self):
		i = 0
		while (i < 8):
			line = ""
			for card in self.cards:
				line += (card.face[i] + " ")
			print (line)
			i += 1
	def printHalf(self):
		i = 0
		while (i < 8):
			line = ""
			line += (self.cards[0].face[i] + " ")
			line += (Cards.boc[i] + " ")
			print (line)
			i += 1
	def evalAceLast(self):
		r = 0
		for card in self.cards:
			if card.GetValue(0) != 11:
				r += card.GetValue(r)
		for card in self.cards:
			if card.GetValue(0) == 11:
				r += card.GetValue(r)
		self.score = r
		return(self.score)
	def hit(self, deck):
		size = len(deck.inPile)
		if (size == 0):
			deck.shuffle()
		size = len(deck.inPile)
		index = randint(0, size - 1)
		self.cards.append(deck.inPile.pop(index))
	def deal(self, deck):
		self.hit(deck)
		self.hit(deck)
	def clear(self, deck):
		size = len(self.cards)
		i = 0
		while (i < size):
			deck.outPile.append(self.cards.pop(0))
			i += 1
		self.doubled = False

#[Noah Panepinto (Oct.3 2021 {01:39})]
	#Here I define a class which represents the result of a finished hand (the HandResult class), which is used to determine whether the player won or lost a hand. 
		#The HandResult class contains three non static (instance) values:
			#self.CardCount; An integer value which represents the number of cards which were in the Hand class object that this HandResult class instance represents when it finished.
			#self.Value; An integer value which represents the point value of the Hand class object that this HandResult class instance represents when it finished.
			#self.DoubleDown; A boolean value which indicates whether or not the Hand class object that this HandResult class instance represents finished by doubling down.

class HandResult:
	def __init__(self, vl, cc, dd = False):
		self.CardCount = cc
		self.Value = vl
		self.DoubleDown = dd
	def __str__(self):
		return ("CC = " + str(self.CardCount) + ", VL = " + str(self.Value) + ", DD = " + str(self.DoubleDown))

#[Noah Panepinto (Oct.3 2021 {01:39})]
	#Here I define a class which represents a player who will play blackjack, it contains three static (instance) values:
		#self.Hand; An array of Hand class objects, one for each that the player is playing at once.
		#self.tb; An integer value which represents the total amount of money currently being bet accross all hands currently being played.
		#self.bi; An integer value which represents the original amount of money bet at the begining of the current round.
	#The Player class contains three functions:
		#Play(); A function which:
			#Shows the player their hand by calling the print() function on the hand currently being interacted with.
			#Determines whether or not the player can double down or split their hand.
			#Checks if the player has reached or exceeded a score of 21 on their hand, reveals the score to the player, 
				#and finishes the hand if the player has reached or exceeded a score of 21 by intantiating and returning a HandResult class object based on the hand currently being interacted with.
			#Informs the player of the things they can do with their hand, Hit, Stand, Split or Double Down as appropriate using the Call() function.
			#Requests that the player decide what they would like to do with their hand next.
				#If the player chooses to hit, call the hit() function for the hand currently being interacted with and recursively calls Play().
				#If the player chooses to stand, instantiate and return a HandResult class object based on the hand currently being interacted with.
				#If the player chooses to split, add self.bi to self.tb, call and return the Split() function.
				#If the player chooses to double down, set Hand.doubled to true for the hand currently being iteracted with, add self.bi to self.tb, call the hit() functionm abd call Play() recursively.
			#Takes in a(n):
				#Deck class object which represents the deck from which the player will draw cards, called deck.
				#Integer value which is used to index self.Hand to find the hand that is currently being interacted with, called i, assumed 0.
				#Boolean value which indicates whether or not the player is betting, called b, assumed false.
				#Integer value which represents the total remaining cash that a player can bet with, called cr, assumed 0.
				#Integer value which represents the amount being bet on all hands initially, called tb, assumed -1.
			#Returns an array of HandResult class object based on all hands being played by the player this round.
		#Call(); A function which presents the player with all of the things they can do with their hand and processes their response. 
			#Takes in a:
				#boolean value which indicates whether the player can double down on the hand currently being interacted with, called d.
				#boolean value which indicates whether the player can split the hand currently being interacted with, called s.
			#Returns an integer value which represents the selection that the player made.
		#Split(); A function which:
			#Creates a new Hand class object and adds it to self.Hands.
			#Moves a card from the hand currently being interacted with to the newly created hand.
			#Calls the hit() function on both the hand currently being interacted with and the newly created hand.
			#Calls and returns Play() on both the hand currently being interacted with and the newly created hand.
			#Takes in a(n):
				#Deck class object which represents the deck from which the player will draw cards, called deck.
				#Integer value which is used to index self.Hand to find the hand that is currently being interacted with, called s, assumed 0.
				#Boolean value which indicates whether or not the player is betting, called b, assumed false.
				#Integer value which represents the total remaining cash that a player can bet with, called cr, assumed 0.
			#Returns an array of HandResult class object based on all hands being played by the player this round.

class Player:
	def __init__(self):
		self.Hand = [ Hand() ]
		self.tb = 0
		self.bi = 0
	def Play(self, deck, i = 0, b = False, cr = 0, tb = -1):
		if (tb != -1):
			self.tb = tb
			self.bi = tb
		print(f"{colours.FORE_BRIGHT_CYAN}\nYour Hand:{colours.ENDC}")
		self.Hand[i].print()
		splitable = False
		doublable = False
		if (len(self.Hand[i].cards) == 2 and cr >= self.tb + self.bi):
			if b:
				doublable = True
			if (self.Hand[i].cards[0].GetValue(0) == self.Hand[i].cards[1].GetValue(0)):
				splitable = True
		done = False
		val = -1
		if (self.Hand[i].evalAceLast() > 21):
			print(f"{colours.FORE_BRIGHT_GREEN}\nTotal Score = Bust...{colours.ENDC}")
			if self.Hand[i].doubled:
				return [ HandResult(self.Hand[i].score, len(self.Hand[i].cards), True) ]
			return [ HandResult(self.Hand[i].score, len(self.Hand[i].cards)) ]
		elif (self.Hand[i].score == 21):
			print(f"{colours.FORE_BRIGHT_GREEN}\nTotal Score = 21!{colours.ENDC}")
			if self.Hand[i].doubled:
				return [ HandResult(self.Hand[i].score, len(self.Hand[i].cards), True) ]
			return [ HandResult(self.Hand[i].score, len(self.Hand[i].cards)) ]
		else:
			print(f"{colours.FORE_BRIGHT_GREEN}\nTotal Score = " + str(self.Hand[i].score) + f"{colours.ENDC}")
		if not self.Hand[i].doubled:
			while (not done):
				val = self.Call(doublable, splitable)
				if (val != -1):
					done = True
				else:
					print (f"{colours.FORE_BRIGHT_ORANGE}\nInvalid input. Please input the letter in brackets for the option you want.{colours.ENDC}")
			if (val == 0):
				self.Hand[i].hit(deck)
				return self.Play(deck, i, b, cr)
			elif (val == 1):
				return [ HandResult(self.Hand[i].score, len(self.Hand[i].cards)) ]
			elif (val == 3):
				self.tb = self.tb + self.bi
				return self.Split(deck, i, b, cr)
			else:
				self.Hand[i].doubled = True
				self.tb = self.tb + self.bi
				self.Hand[i].hit(deck)
				return self.Play(deck, i, b, cr)
		else:
			return [ HandResult(self.Hand[i].score, len(self.Hand[i].cards), True) ]
	def Call(self, d, s):
		response = ""
		if (d and s):
			response = input(f"{colours.FORE_BRIGHT_BLUE}\nWould you like to {colours.ENDC}(H){colours.FORE_BRIGHT_BLUE}it, {colours.ENDC}(S){colours.FORE_BRIGHT_BLUE}tand, {colours.ENDC}(D){colours.FORE_BRIGHT_BLUE}ouble Down or S{colours.ENDC}(P){colours.FORE_BRIGHT_BLUE}lit? - {colours.ENDC}")
		elif (d and not s):
			response = input(f"{colours.FORE_BRIGHT_BLUE}\nWould you like to {colours.ENDC}(H){colours.FORE_BRIGHT_BLUE}it, {colours.ENDC}(S){colours.FORE_BRIGHT_BLUE}tand or {colours.ENDC}(D){colours.FORE_BRIGHT_BLUE}ouble Down? - {colours.ENDC}")
		elif (not d and s):
			response = input(f"{colours.FORE_BRIGHT_BLUE}\nWould you like to {colours.ENDC}(H){colours.FORE_BRIGHT_BLUE}it, {colours.ENDC}(S){colours.FORE_BRIGHT_BLUE}tand or S{colours.ENDC}(P){colours.FORE_BRIGHT_BLUE}lit? - {colours.ENDC}")
		else:
			response = input(f"{colours.FORE_BRIGHT_BLUE}\nWould you like to {colours.ENDC}(H){colours.FORE_BRIGHT_BLUE}it or {colours.ENDC}(S){colours.FORE_BRIGHT_BLUE}tand? - {colours.ENDC}")
		val = -1
		for char in response:
			if (char == "H" or char == "h"):
				val = 0
				break
			elif (char == "S" or char == "s"):
				val = 1
				break
			elif ((char == "D" or char == "d") and d):
				val = 2
				break
			elif ((char == "P" or char == "p") and s):
				val = 3
				break
		return val
	def Split(self, deck, s, b = False, cr = 0):
		self.Hand.append(Hand())
		n = len(self.Hand) - 1
		self.Hand[-1].cards.append(self.Hand[s].cards.pop(-1))
		self.Hand[-1].hit(deck)
		self.Hand[s].hit(deck)
		r = self.Play(deck, s, b, cr)
		input(f"{colours.FORE_BRIGHT_BLUE}\nHit enter for your next hand.{colours.ENDC}")
		r.extend(self.Play(deck, n, b, cr))
		return r

#[Noah Panepinto (Oct.3 2021 {01:39})]
	#Here I define a class which represents the dealer who the player will be trying to beat. The Dealer class is derived from the Player class.
		#The Dealer class contains one non static (instance) value, self.Hand; a Hand class object.
		#The Dealer class contains one function:
			#Play(); A function which:
				#Checks if the dealer has reached or exceeded a score of 21 on their hand, reveals the score to the player, 
					#and finishes the hand if the dealer has reached or exceeded a score of 21 by intantiating and returning a HandResult class object self.Hand.
				#Checks if the dealer has reacher or exceeded a score of 17 on their hand, 
					#calls the hit() function of self.Hand() if the dealer has not reached or exceeded a score of 17 on their hand and calls Play() recursively,
					#and finishes the hand if the dealer has reached or exceeded a score of 17 by intantiating and returning a HandResult class object self.Hand.
				#Takes in a Deck class object which represents the deck from which the player will draw cards, called deck.
				#Returns a HandResult class object based on self.Hand(). 

class Dealer(Player):
	def __init__(self):
		self.Hand = Hand()
	def Play(self, deck):
		print(f"{colours.FORE_BRIGHT_CYAN}\nDealer's Hand:{colours.ENDC}")
		self.Hand.print()
		if (self.Hand.evalAceLast() > 21):
			print(f"{colours.FORE_BRIGHT_GREEN}\nTotal Score = Bust...{colours.ENDC}")
			return HandResult(self.Hand.score, len(self.Hand.cards))
		elif (self.Hand.score == 21):
			print(f"{colours.FORE_BRIGHT_GREEN}\nTotal Score = 21!{colours.ENDC}")
			return HandResult(self.Hand.score, len(self.Hand.cards))
		else:
			print(f"{colours.FORE_BRIGHT_GREEN}\nTotal Score = " + str(self.Hand.score) + f"{colours.ENDC}")
		if (self.Hand.score <= 16):
			print(f"{colours.FORE_BRIGHT_BLUE}\nDealer Hits!{colours.ENDC}")
			self.Hand.hit(deck)
			return self.Play(deck)
		else:
			print(f"{colours.FORE_BRIGHT_BLUE}\nDealer Stands!{colours.ENDC}")
			return HandResult(self.Hand.score, len(self.Hand.cards))
		
#[Noah Panepinto (Dec.15 2021 {22:10})]
	#Here I define a class which represents the game instance as a whole, I would like to one day generalize this into a CardGame class and derive the BlackPack class from that.
		#The BlackPack class contains nine non static (instance) values:
			#self.Deck; A Deck objeect which contains all of the cards that will be used within the game.
			#self.Player; A Player object which represents the human player of the game.
			#self.Dealer; A Dealer object which represents the AI dealer of the game.
			#self.AutoShuffle; A boolean value which indicates whether the game will be played with autoshuffle enabled.
			#self.Betting; A boolean value which indicated whether the game will be played with betting enabled.
			#self.PlayerCash; An integer value which indicates how much money the player has at their disposal.
			#self.InitialPlayerCash; An integer value that holds the amount of cash a player was holding at the beginning of a hand.
			#self.MaxBet; An integer value that indicates the maximum amount of money that a player can bet on any given hand.
			#self.MinBet; An integer value that indicates the minimum amount of money that a player can bet on any given hand.
		#The BlackPack class contains two functions:
			#PlayGame(); A function which:
				#Asks the player how many decks they would like to play with, and sets self.Deck to be equal to a Deck Object containing the right number of cards.
				#Asks the player if they would like to play with autoshuffle, and sets self.AutoShuffle accordingly.
				#Asks the player if they would like to play with betting, and sets self.Betting accordingly. If they decide to play with betting;
					#Asks the player how much money they would like to have available for betting, and sets self.PlayerCash accordingly.
					#Asks the player for the largest bet they would like to be able to make, and sets self.MaxBet accordingly.
					#Asks the player for the smallest bet they would like to be able to make, and sets self.MinBet accordingly.
				#Calls the PlayRound() function.
			#PlayRound(); A function Which:
				#Shuffles the deck if self.AutoShuffle is True by calling shuffle() in self.Deck.
				#Informs the player of the number of cards remaining in the inpile of the deck if self.AutoShuffle is False.
				#If self.Beting is True;
					#Informs the player of the value of self.PlayerCash, and ends the game if self.PlayerCash is equal to 0.
					#Requests the amount of money the player would like to bet and checks that it exceeds neither self.MaxBet nor self.PlayerCash,
						#and that it is equal to or greater than self.MinBet.
				#Randomly draws two cards into the hand of both self.Player and self.Dealer by calling Hand.Deal() on self.Player's first hand and Hand.Deal() on self.Dealer.
				#Shows both cards dealt to the player by calling Hand.print() on Self.Player's first deck, and the first card dealt to the dealer by calling Hand.printHalf() on self.Dealer.
				#Calls Player.Play() for self.Player in order to have the player play their hand or hands.
				#Calls Dealer.Play() for self.Dealer in order to have the dealer play their hand.
				#Compares the result of the player's hand or hands to the dealer's hand and evalueats who wins on each hand, and if self.Betting is True:
					#Calculates the amount of money won or lost on each hand and updates self.PlayerCash accordingly.
					#Ends the game if self.PlayerCash is equal to 0.
				#Asks the player if they would like to play again, and if so calls the PlayRound() function recursively, 
					#otherwise if self.Betting is True informs the player of how much they lost or won, and exits.

class BlackPack:
	def __init__(self):
		self.Deck = Deck(0)
		self.Player = Player()
		self.Dealer = Dealer()
		self.AutoShuffle = False
		self.Betting = False
		self.PlayerCash = 0
		self.InitialPlayerCash = 0
		self.MaxBet = 0
		self.MinBet = 0
	def PlayGame(self):
		cont = False
		while not cont:
			decks = input("\nHow many decks would you like to play with? ")
			try:
				decksInt = int(decks)
				if (decksInt < 1):
					print("\nPlease input a number greater than zero.\n")
				elif (decksInt > 10):
					print("\nPlease input a number less than eleven.\n")
				else:
					cont = True
			except:
				print("\nPlease input a whole number.")
		done = False
		while not done:
			response = input("\nPlay with auto shuffle? (Y)es or (N)o? - ")
			for char in response:
				if (char == "Y" or char == "y"):
					shuffle = 1
					done = True
					break
				elif (char == "N" or char == "n"):
					shuffle = 2
					done = True
					break
			if (shuffle == 0):
				print("\nInvalid input. Please input the letter in brackets for the option you want.")
			elif (shuffle == 1):
				print("\nAwesome! No card counting here.")
				self.AutoShuffle = True
			else:
				print("\nAwesome! Count those cards!")
				self.AutoShuffle = False
		done = False
		bet = 0
		while not done:
			response = input("\nPlay with betting? (Y)es or (N)o? - ")
			for char in response:
				if (char == "Y" or char == "y"):
					bet = 1
					done = True
					break
				elif (char == "N" or char == "n"):
					bet = 2
					done = True
					break
			if (bet == 0):
				print("\nInvalid input. Please input the letter in brackets for the option you want.")
			elif (bet == 1):
				print("\nAwesome! Let's do this right!")
				self.Betting = True
			else:
				print("\nAwesome! Let's play for fun.")
				self.Betting = False
		if self.Betting:
			cont = False
			while not cont:
				cash = input("\nHow much cash would you like to have for betting? ")
				try:
					cashInt = int(cash)
					if (cashInt < 1):
						print("\nPlease input a number greater than zero.")
					elif (cashInt > 1000000):
						print("\nPlease input a number less than one million.")
					else:
						cont = True
				except:
					print("\nPlease input a whole number.")
			self.PlayerCash = cashInt
			self.InitialPlayerCash = self.PlayerCash
			cont = False
			while not cont:
				max = input("\nHow much cash would you like to have for your betting maximum? ")
				try:
					maxInt = int(max)
					if (maxInt < 1):
						print("\nPlease input a number greater than zero.")
					elif (maxInt > (self.PlayerCash / 10)):
						print("\nPlease input a number less than or equal to one tenth your cash total.")
					elif (maxInt < (self.PlayerCash / 100)):
						print("\nPlease input a number more than or equal to one hundredth your cash total.")
					else:
						cont = True
				except:
					print("\nPlease input a whole number.")
			self.MaxBet = maxInt
			cont = False
			while not cont:
				min = input("\nHow much cash would you like to have for your betting minimum? ")
				try:
					minInt = int(min)
					if (minInt < 1):
						print("\nPlease input a number greater than zero.")
					elif (minInt > self.MaxBet):
						print("\nPlease input a number less than or equal to your betting maximum.")
					elif (maxInt < (self.PlayerCash / 1000)):
						print("\nPlease input a number more than or equal to one thousandth your cash total.")
					else:
						cont = True
				except:
					print("\nPlease input a whole number.")
			self.MinBet = minInt
		self.Deck = Deck(decksInt)
		print(f"{colours.FORE_BRIGHT_GREEN}\nGreat! Let's shuffle up and play!{colours.ENDC}")
		self.PlayRound()
	def PlayRound(self):
		if self.AutoShuffle:
			self.Deck.shuffle()
		else:
			print(f"{colours.FORE_BRIGHT_CYAN}\nDeck Remaining Size: {colours.ENDC}" + str(len(self.Deck.inPile)))
		betInt = 0
		if self.Betting:
			print(f"{colours.FORE_BRIGHT_CYAN}\nBetting Cash Remaining: {colours.ENDC}" + str(self.PlayerCash))
			if (self.PlayerCash <= 0):
				print(f"{colours.FORE_BRIGHT_ORANGE}\nYou've gone broke. That's game over.\n{colours.ENDC}")
				return 0
			cont = False
			while not cont:
				bet = input(f"{colours.FORE_BRIGHT_BLUE}\nHow much cash would you like to bet? {colours.ENDC}")
				try:
					betInt = int(bet)
					if (betInt < self.MinBet):
						print(f"{colours.FORE_BRIGHT_ORANGE}\nPlease input a number greater than {colours.ENDC}" + str(self.MinBet) + f"{colours.FORE_BRIGHT_ORANGE}.{colours.ENDC}")
					elif (betInt > self.MaxBet):
						print(f"{colours.FORE_BRIGHT_ORANGE}\nPlease input a number less than {colours.ENDC}" + str(self.MaxBet) + f"{colours.FORE_BRIGHT_ORANGE}.{colours.ENDC}")
					elif (betInt > self.PlayerCash):
						print(f"{colours.FORE_BRIGHT_ORANGE}\nPlease input a number less than or equal to your cash amount.{colours.ENDC}")
					else:
						cont = True
				except:
					print(f"{colours.FORE_BRIGHT_ORANGE}\nPlease input a whole number.{colours.ENDC}")
		self.Player.Hand[0].deal(self.Deck)
		self.Dealer.Hand.deal(self.Deck)
		print(f"{colours.FORE_BRIGHT_CYAN}\nYour Hand:{colours.ENDC}")
		self.Player.Hand[0].print()
		print(f"{colours.FORE_BRIGHT_CYAN}\nDealer's Hand:{colours.ENDC}")
		self.Dealer.Hand.printHalf()
		input(f"{colours.FORE_BRIGHT_BLUE}\nHit enter for your turn.{colours.ENDC}")
		playerScores = self.Player.Play(self.Deck, 0, self.Betting, self.PlayerCash, betInt)
		input(f"{colours.FORE_BRIGHT_BLUE}\nHit enter for the dealer's turn.{colours.ENDC}")
		dealerScore = self.Dealer.Play(self.Deck)
		for hand in self.Player.Hand:
			hand.clear(self.Deck)
		i = 1
		while i < len(self.Player.Hand):
			self.Player.Hand.pop(1)
			i += 1
		self.Dealer.Hand.clear(self.Deck)
		i = 0
		for playerScore in playerScores:
			if (dealerScore.Value == 21 and dealerScore.CardCount == 2):
				print(f"{colours.FORE_BRIGHT_CYAN}\nThe dealer got blackjack...{colours.ENDC}")
				print(f"{colours.FORE_BRIGHT_CYAN}Your score = {colours.ENDC}" + str(playerScore.Value))
				print(f"{colours.FORE_BRIGHT_CYAN}Dealer's score = {colours.ENDC}" + str(dealerScore.Value))
				if self.Betting:
					if not playerScore.DoubleDown:
						self.PlayerCash -= betInt
						print(f"{colours.FORE_BRIGHT_CYAN}You lost your bet of {colours.ENDC}" + str(betInt) + f"{colours.FORE_BRIGHT_CYAN}.{colours.ENDC}")
					else:
						self.PlayerCash -= betInt * 2
						print(f"{colours.FORE_BRIGHT_CYAN}You lost double your bet of {colours.ENDC}" + str(betInt) + f"{colours.FORE_BRIGHT_CYAN}...{colours.ENDC}")
					print(f"{colours.FORE_BRIGHT_CYAN}Cash remaining = {colours.ENDC}" + str(self.PlayerCash))
			elif (playerScore.Value == 21 and playerScore.CardCount == 2):
				print(f"{colours.FORE_BRIGHT_CYAN}\nYou got blackjack!{colours.ENDC}")
				print(f"{colours.FORE_BRIGHT_CYAN}Your score = {colours.ENDC}" + str(playerScore.Value))
				print(f"{colours.FORE_BRIGHT_CYAN}Dealer's score = {colours.ENDC}" + str(dealerScore.Value))
				if self.Betting:
					self.PlayerCash += (betInt * 2)
					print(f"{colours.FORE_BRIGHT_CYAN}You won double your bet of {colours.ENDC}" + str(betInt) + f"{colours.FORE_BRIGHT_CYAN}!{colours.ENDC}")
					print(f"{colours.FORE_BRIGHT_CYAN}Cash remaining = {colours.ENDC}" + str(self.PlayerCash) + f"{colours.ENDC}")
			elif ((playerScore.Value < 22 and dealerScore.Value > 21) or (playerScore.Value < 22 and playerScore.Value > dealerScore.Value)):
				print(f"{colours.FORE_BRIGHT_CYAN}\nYou beat the dealer!{colours.ENDC}")
				print(f"{colours.FORE_BRIGHT_CYAN}Your score = {colours.ENDC}" + str(playerScore.Value) + f"{colours.ENDC}")
				print(f"{colours.FORE_BRIGHT_CYAN}Dealer's score = {colours.ENDC}" + str(dealerScore.Value) + f"{colours.ENDC}")
				if self.Betting:
					if not playerScore.DoubleDown:
						self.PlayerCash += betInt
						print(f"{colours.FORE_BRIGHT_CYAN}You won your bet of {colours.ENDC}" + str(betInt) + f"{colours.FORE_BRIGHT_CYAN}.{colours.ENDC}")
					else:
						self.PlayerCash += betInt * 2
						print(f"{colours.FORE_BRIGHT_CYAN}You won double your bet of {colours.ENDC}" + str(betInt) + f"{colours.FORE_BRIGHT_CYAN}.{colours.ENDC}")
					print(f"{colours.FORE_BRIGHT_CYAN}Cash remaining = {colours.ENDC}" + str(self.PlayerCash) + f"{colours.ENDC}")
			elif (playerScore.Value < 22 and playerScore.Value == dealerScore.Value):			
				print(f"{colours.FORE_BRIGHT_CYAN}\nYou pushed with the dealer.{colours.ENDC}")
				print(f"{colours.FORE_BRIGHT_CYAN}Your score = {colours.ENDC}" + str(playerScore.Value))
				print(f"{colours.FORE_BRIGHT_CYAN}Dealer's score = {colours.ENDC}" + str(dealerScore.Value))
				if self.Betting:
					print(f"{colours.FORE_BRIGHT_CYAN}Your money was returned.{colours.ENDC}")
					print(f"{colours.FORE_BRIGHT_CYAN}Cash remaining = {colours.ENDC}" + str(self.PlayerCash) + f"{colours.ENDC}")
			else:
				print(f"{colours.FORE_BRIGHT_CYAN}\nThe dealer beat you...{colours.ENDC}")
				print(f"{colours.FORE_BRIGHT_CYAN}Your score = {colours.ENDC}" + str(playerScore.Value))
				print(f"{colours.FORE_BRIGHT_CYAN}Dealer's score = {colours.ENDC}" + str(dealerScore.Value))
				if self.Betting:
					if not playerScore.DoubleDown:
						self.PlayerCash -= betInt
						print(f"{colours.FORE_BRIGHT_CYAN}You lost your bet of {colours.ENDC}" + str(betInt) + f"{colours.FORE_BRIGHT_CYAN}.{colours.ENDC}")
					else:
						self.PlayerCash -= betInt * 2
						print(f"{colours.FORE_BRIGHT_CYAN}You lost double your bet of {colours.ENDC}" + str(betInt) + f"{colours.FORE_BRIGHT_CYAN}...{colours.ENDC}")
					print(f"{colours.FORE_BRIGHT_CYAN}Cash remaining = {colours.ENDC}" + str(self.PlayerCash))
			i += 1
		if self.Betting:
			if (self.PlayerCash <= 0):
				print(f"{colours.FORE_BRIGHT_ORANGE}\nYou've gone broke. That's game over.\n{colours.ENDC}")
				return 0
		done = False
		again = 0
		while not done:
			response = input(f"{colours.FORE_BRIGHT_BLUE}\nPlay again? {colours.ENDC}(Y){colours.FORE_BRIGHT_BLUE}es or {colours.ENDC}(N){colours.FORE_BRIGHT_BLUE}o? - {colours.ENDC}")
			for char in response:
				if (char == "Y" or char == "y"):
					again = 1
					done = True
					break
				elif (char == "N" or char == "n"):
					again = 2
					done = True
					break
			if (again == 0):
				print(f"{colours.FORE_BRIGHT_ORANGE}\nInvalid input. Please input the letter in brackets for the option you want.{colours.ENDC}")
			elif (again == 1):
				print(f"{colours.FORE_BRIGHT_GREEN}\nAwesome! Let's deal them out again!{colours.ENDC}")
				self.PlayRound()
				done = True
			else:
				print(f"{colours.FORE_BRIGHT_GREEN}\nThank you for playing!\n{colours.ENDC}")
				if self.Betting:
					if self.PlayerCash > self.InitialPlayerCash:
						print(f"{colours.FORE_BRIGHT_BLUE}You won {colours.ENDC}" + str(self.PlayerCash - self.InitialPlayerCash) + f"{colours.FORE_BRIGHT_BLUE} today!\n{colours.ENDC}")
					elif self.PlayerCash < self.InitialPlayerCash:
						print(f"{colours.FORE_BRIGHT_BLUE}You lost {colours.ENDC}" + str(self.InitialPlayerCash - self.PlayerCash) + f"{colours.FORE_BRIGHT_BLUE} today.\n{colours.ENDC}")
					else:
						print(f"{colours.FORE_BRIGHT_BLUE}You broke even today.\n{colours.ENDC}")
				done = True
				return 0

if __name__ == '__main__':
	Cards.Load('Cards.xml')
	game = BlackPack()
	game.PlayGame()
