# classes board and check where check is the class of a checkers piece and board the class of a checkers board (a list of check objects with a few methods) 
class board:
	def __init__(self): # create a list of check objects according to the rules of english draughts
		self.case_list = []
		for i in range(0,8):
			for j in range(0,8):
				if (i+j)%2 == 1: # (i+j)%2==1 means a black case on the board
					if i<3 :
						self.case_list.append(check(1,0,[i,j],self)) # 12 pieces for player 1 
					elif i>4 :
						self.case_list.append(check(-1,0,[i,j],self)) # 12 pieces for player 2, i used 1 and -1 as the ID of the players to make coding x-axis movements easier
	def is_clear(self,pos1,pos2): # This function tells us if a position on the board (ex: 1,2) is clear. 
		for i in self.case_list:
			if i.pos == [pos1,pos2]:
				return False
		return True
	def get_index(self,pos1,pos2): # opposite of function above, returns the checkers piece object 
		for i in range(0,len(self.case_list)):
			if self.case_list[i].pos == [pos1,pos2]:
				return i
	def player(self,pos1,pos2): # returns the ID of the player at position i,j
		for i in self.case_list:
			if i.pos == [pos1,pos2]:
				return i.player
		return 0
class check:
	def __init__(self,player,king,pos,board): # properties i used for a checkers piece are the player ID, if its a king (1 or 0), its position and the board its on
		self.player = player
		self.king = king 
		self.pos = pos
		self.board = board
	def get_moves(self): # return the possible moves of the checkers piece 
		l = [] 
		if (self.pos[0]+self.player>=0 and self.pos[0]+self.player<8): 
			if self.pos[1]+1<8 : 
				if self.board.is_clear(self.pos[0]+self.player,self.pos[1]+1):
					l.append([self.pos[0]+self.player,self.pos[1]+1])
			if self.pos[1]-1>=0 : 
				if self.board.is_clear(self.pos[0]+self.player,self.pos[1]-1):
					l.append([self.pos[0]+self.player,self.pos[1]-1])
		if self.king == 1:
			if (self.pos[0]-self.player>=0 and self.pos[0]-self.player<8): 
				if self.pos[1]+1<8 : 
					if self.board.is_clear(self.pos[0]-self.player,self.pos[1]+1):
						l.append([self.pos[0]-self.player,self.pos[1]+1])
				if self.pos[1]-1>=0 : 
					if self.board.is_clear(self.pos[0]-self.player,self.pos[1]-1):
						l.append([self.pos[0]-self.player,self.pos[1]-1])
		return l
	def get_caps(self):
		l = []
		ll = []
		if (self.pos[0]+2*self.player>=0 and self.pos[0]+2*self.player<8):
			if self.pos[1]+2<8:
				if self.board.is_clear(self.pos[0]+2*self.player,self.pos[1]+2):
					if self.player == -1*self.board.player(self.pos[0]+self.player,self.pos[1]+1):
						l.append([self.pos[0]+2*self.player,self.pos[1]+2])
						ll.append([self.pos[0]+self.player,self.pos[1]+1])
			if self.pos[1]-2>=0:
				if self.board.is_clear(self.pos[0]+2*self.player,self.pos[1]-2):
					if self.player == -1*self.board.player(self.pos[0]+self.player,self.pos[1]-1): 
						l.append([self.pos[0]+2*self.player,self.pos[1]-2])
						ll.append([self.pos[0]+self.player,self.pos[1]-1])
		if self.king == 1:
			if (self.pos[0]-2*self.player>=0 and self.pos[0]-2*self.player<8):
				if self.pos[1]+2<8:
					if self.board.is_clear(self.pos[0]-2*self.player,self.pos[1]+2) :
						if self.player == -1*self.board.player(self.pos[0]-self.player,self.pos[1]+1):
							l.append([self.pos[0]-2*self.player,self.pos[1]+2])
							ll.append([self.pos[0]-self.player,self.pos[1]+1])
				if self.pos[1]-2>=0:
					if self.board.is_clear(self.pos[0]-2*self.player,self.pos[1]-2) :
						if self.player == -1*self.board.player(self.pos[0]-self.player,self.pos[1]-1):
							l.append([self.pos[0]-2*self.player,self.pos[1]-2])
							ll.append([self.pos[0]-self.player,self.pos[1]-1])
		return [l,ll]