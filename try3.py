# classes board and check where check is the class of a checkers piece and board the class of a checkers board (a list of check objects with a few methods) 
def board_index(board,pos):
		for i in range(0,len(board)):
			if board[i].pos == pos:
				return [i,board[i].player] 
		return [13,0]
class board:
	def __init__(self): # create a list of check objects according to the rules of english draughts
		self.case_list = [] # This list contains all the checkers pieces on the board 
		for i in range(0,8):
			for j in range(0,8):
				if (i+j)%2 == 1: # (i+j)%2==1 means a black case on the board
					if i<3 : # at start of game all black pieces are on this side 
						self.case_list.append(check(1,0,[i,j],self)) # 12 pieces for player 1 
					elif i>4 :
						self.case_list.append(check(-1,0,[i,j],self)) # 12 pieces for player 2, i used 1 and -1 as the ID of the players to make coding x-axis movements easier
	def is_clear(self,pos1,pos2): # This function tells us if a position on the board (ex: 1,2) is clear. 
		for i in self.case_list:
			if i.pos == [pos1,pos2]: # means a checkers piece is in this position
				return False
		return True
	def get_index(self,pos1,pos2): # opposite of function above, returns the checkers piece object 
		for i in range(0,len(self.case_list)): 
			if self.case_list[i].pos == [pos1,pos2]: # a checkers piece with this position exists, we return the checkers piece object
				return i
	def player(self,pos1,pos2): # returns the ID of the player at position i,j. This function is useless as get_index can do the same thing 
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
	def get_moves(self): # return the possible moves of the checkers piece, checks if the positions diagonal by one are free and returns them in a list 
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
	def get_caps(self): # returns the possible captures, checks accordinly if the positions diagonal by two are free and the pieces diagonal by one are those of the other player  
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
# all the functions down below are used for the calculation of the possible paths a checkers piece can take when capturing other pieces 
# To do this i used this easy but stupid method (i know this can be resolved with a simple recursive funtion but i could not find it and i didnt want to look it up)
# i start with a list with the possible checkers pieces i can capture with one move
# I loop over this list and simulate what pieces i can capture from my new position and then add the new position to the list and so on
# I identify the position with indexes in this form 'xxxx', the length of the index indicates the number of moves the piece has made to get to the position
# for example my first move index is 0 the next move is going to be 00 01 02 or 03 depending on the numbre of possible moves 
# ex ['0','1','2','00','01','10','000','0000']
# The next step is to make the path from the list above 
# and i use the positions in the initial list 
# check the code for more details 
	def can_i(self,pos,eat): # This function simulates what pieces i can capture with one move from position 'pos' where 'eat' is a list of previously captured pieces
		new_list = []
		for i in self.board.case_list:
			case = check(i.player,i.king,i.pos,i.board)
			new_list.append(case)
		new_list[self.board.get_index(*self.pos)].pos = pos
# checks if the simulation should be performed as a king or not (if the new position is at the edge of the board or if the checkers piece have moved to it before)
		if self.king == 0:
			if self.player == 1: 
				if pos[0] == 7: 
					new_list[self.board.get_index(self.pos[0],self.pos[1])].king = 1
			if self.player == -1:
				if pos[0] == 0:
					new_list[self.board.get_index(self.pos[0],self.pos[1])].king = 1
			for e in eat:
				if self.player == 1 and e[0]==6 :
					new_list[self.board.get_index(self.pos[0],self.pos[1])].king = 1
				if self.player == -1 and e[0]==1 :
					new_list[self.board.get_index(self.pos[0],self.pos[1])].king = 1
		for i in eat:
			new_list.remove(new_list[board_index(new_list,i)[0]])
		l = []
		ll = []
		if pos[0]+2*self.player>=0 and pos[0]+2*self.player<8:
			if pos[1]+2<8:
				if board_index(new_list, [pos[0]+2*self.player,pos[1]+2]) == [13,0]:
					if self.player == -1*board_index(new_list, [pos[0]+self.player,pos[1]+1])[1]:
						l.append([pos[0]+2*self.player,pos[1]+2])
						ll.append([pos[0]+self.player,pos[1]+1])
			if pos[1]-2>=0:
				if board_index(new_list, [pos[0]+2*self.player,pos[1]-2]) == [13,0]:
					if self.player == -1*board_index(new_list, [pos[0]+self.player,pos[1]-1])[1]:
						l.append([pos[0]+2*self.player,pos[1]-2])
						ll.append([pos[0]+self.player,pos[1]-1])
		if new_list[board_index(new_list, pos)[0]].king == 1:
			if pos[0]-2*self.player>=0 and pos[0]-2*self.player<8:
				if pos[1]+2<8:
					if board_index(new_list, [pos[0]-2*self.player,pos[1]+2]) == [13,0]:
						if self.player == -1*board_index(new_list, [pos[0]-self.player,pos[1]+1])[1]:
							l.append([pos[0]-2*self.player,pos[1]+2])
							ll.append([pos[0]-self.player,pos[1]+1])
				if pos[1]-2>=0:
					if board_index(new_list, [pos[0]-2*self.player,pos[1]-2]) == [13,0]:
						if self.player == -1*board_index(new_list, [pos[0]-self.player,pos[1]-1])[1]:
							l.append([pos[0]-2*self.player,pos[1]-2])
							ll.append([pos[0]-self.player,pos[1]-1])
		return [l,ll] # return the possible positions within one move and the captured pieces within one move 
	def get_paths(self): # this function does the loop i talked about above
		l = []
		paths = []
		pow = []
		next = 0
		current = None
		current_list = []
		for i in range(0,len(self.get_caps()[0])):
			l.append([self.get_caps()[0][i],str(i),[self.get_caps()[1][i]]])
		while next != len(l):
			current = l[next]
			jiji = 0
			current_list = self.can_i(current[0],current[2])
			if current_list[0] != []: 
				for j in range(0,len(current_list[0])):
					fp = current[2]+[[current_list[1][j][0],current_list[1][j][1]]]
					l.append([current_list[0][j], current[1]+str(jiji), fp])
					jiji = jiji + 1
			next = next + 1
		return l
	def path_length(self): # checks the max number of moves i can make in the paths returned by the function above 
		pl = 0
		for i in self.get_paths():
			if pl < len(i[1]):
				pl = len(i[1])
		return pl
	def deserialize(self): # turns the list of indexes into a list of lists of index of the same length
		l = []
		for i in range(1,self.path_length()+1):
			firo = []
			for j in self.get_paths():
				if len(j[1]) == i:
					firo.append(j[1])
			l.append(firo)
		return l
	def simplify(self): # return the list of indexes
		l = []
		for i in self.get_paths():
			l.append(i[1])
		return l
	def pathify(self,id): # turns an index into a list of indexes ex : 10102 -> [1,10,101,1010,10102]
		l = []
		for i in range(1,len(id)+1):
			l.append(id[0:i])
		return l
	def cut(self,l): # remove the last caracter of the positions index in a list (i use this function to choose the caracters to ignore when making the paths) 
		ll = []
		for i in l:
			ll.append(i[0:len(i)-1])
		return ll
	def decompose(self): # turns the list returned by the function deserialize into a list of paths by indexes 
		l = []
		ignore = []
		ignore_next = []
		for i in self.deserialize()[::-1]:
			ignore = ignore_next+self.cut(ignore)
			ignore_next = []
			for j in i:
				if j not in ignore:
					l.append(self.pathify(j))
					if j[0:len(j)] not in ignore_next:
						ignore_next.append(j[0:len(j)-1])
		return l 
	def normalize(self): # final step : turn the indexes returned by the function above into positions on the board
		ids = self.decompose()
		paths = self.get_paths()
		final = []
		for i in ids:
			path = []
			for q in i:
				for j in paths:
					if j[1] == q:
						path.append(j[0])
			path.insert(0,self.pos) # add the initial position to the path list
			final.append(path)
		return final
