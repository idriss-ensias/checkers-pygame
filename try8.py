# Small checkers game made by me using Pygame and Python 3                                                                                                       |
# Please note this is my first attempt and i have only used Python before for pentesting scripts (HTTP requests) and designing a simple website with Django      |
# In the comments below i will try to explain each line                                                                                                          |
# I would really appreciate your comments and feedback at idriss.el.moussaouiti@gmail.com                                                                        |
# -------------------------------------------------------------------------------------------------------------------------------------------------------------- |

# I import the pygame package and variables 
# I also import try3 which is the python file i wrote with the checkers board class and checkers piece class
import pygame
from pygame.locals import * 
from try3 import *


# This first part is for initialization 
bb = board() # I initialize the board used for the game
pygame.init()
fenetre = pygame.display.set_mode((1000,600)) 
pygame.display.set_caption('Checkers Game')
thumb = pygame.image.load("checkers_thumb.png").convert_alpha() 
pygame.display.set_icon(thumb)
myfont = pygame.font.SysFont('Comic Sans MS', 20)
myotherfont = pygame.font.SysFont('Comic Sans MS', 70) 
check_sound = pygame.mixer.Sound("gun.wav")
end_sound = pygame.mixer.Sound("TADA.wav")
ebony = pygame.image.load("ebony_re.png").convert_alpha() # I load the blacks checkers piece png image file i created using microsoft paint 
ivory = pygame.image.load("ivory_re.png").convert_alpha() # I load the whites checkers piece png image file i created using microsoft paint
ebony_k = pygame.image.load("ebony_king.png").convert_alpha() # I load the blacks checkers king piece png image file i created using microsoft paint
ivory_k = pygame.image.load("ivory_king.png").convert_alpha() # I load the whites king checkers piece png image file i created using microsoft paint
continuer = 0 # Pygame loop variable 
l = [] # This is a list i will be using of all the pieces on the board during the game 
clicked = 0 # This is a variable i used to implement the drag and drop functionality where 0 is nothing dragged and 1 a piece is dragged
case_click = None # same as the variable above but for storing the checkers piece being dragged 
turni = 1 # This variable is for storing turns where 1 is the blacks and -1 the whites 
sur = [] # This list is to store the positions of possible movements of the checkers piece being dragged (for highlighting)
sure = [] # This list is to store the positions of possible capture movements of the checkers piece being dragged (for highlighting)
suree = 0
cap = 0 # if the selected checkers piece can capture other pieces 
cap_list = [] # list of pieces that can be captured 
invalid = 0 # evaluates if a move is valid
butt_click = 0 # if the user has clicked the new game button
lines = 'ABCDEFGH' 
columns = '12345678'
log_whites = [] # log of n past moves, see function add_log()
log_blacks = []
# This second part is for the functions i use to move checkers pieces and show the checkers board

# This functions converts a couple [i,j] into a position on the screen, i use it to put the checkers pieces in their place on the board
def from_cord_to_pos(i,j):
	if (i<8 and i>=0) and (j<8 and j>=0):
		return [50*(i+1),50*(j+1)]
		
# This function does the opposite of the function above as it converts a position on the screen to a logical position on the board, i use it for the clicks
def from_pos_to_cord(pos1,pos2):
	for i in range(0,8):
		for j in range(0,8):
			if (pos1>50*(i+1) and pos1<50*(i+2)) and (pos2>50*(j+1) and pos2<50*(j+2)):
				if (i<8 and i>=0) and (j<8 and j>=0):
					return [i,j]
	return None

def from_pos_to_cord_list(lis):
	l = []
	for i in lis:
		l.append([50*(i[0]+1)+25,50*(i[1]+1)+25])
	return l
# I explained above the use of the list l, this function return the index of the checkers piece with the position given as an argument
def get_case(i,j):
	global l
	for n in range(0,len(l)):
		if l[n][0].pos == [i,j]:
			return n
	return None

def add_log(i,j,p,q):
	global log
	global turni
	if turni == 1:
		if len(log_blacks) == 9:
			log_blacks.pop(0)
			log_blacks.append([i,j,p,q])
		else:
			log_blacks.append([i,j,p,q])
	if turni == -1:
		if len(log_whites) == 9:
			log_whites.pop(0)
			log_whites.append([i,j,p,q])
		else:
			log_whites.append([i,j,p,q])
# This function is to follow the game, and tell us if a player won or if there was a tie. 
def game():
	global l 
	player_one = 0
	player_two = 0
	for i in l:
		if i[0].player == 1:
			player_one = 1
			break
	for i in l:
		if i[0].player == -1:
			player_two = 1
			break
	if player_one+player_two == 1:
		if player_one == 1:
			return 1
		if player_two == 1:
			return -1
	else:
		for i in l:
			if len(i[0].get_moves()) != 0:
				return 2
			if len(i[0].get_caps()) != 0:
				return 2
	return 0
	
# This function is to draw the board on the screen, it loops over the list l and puts each checkers piece in its position on the screen  
def show_board():
	global fenetre
	global l
	global sur
	global sure
	global invalid
	global butt_click
	global end_sound
	pygame.draw.rect(fenetre, (255,0,255), [500,0,500,600])
	textsurface = myfont.render('Player 1', False, (0,0,0))
	fenetre.blit(textsurface, (650, 50))
	textsurface = myfont.render('Player 2', False, (0,0,0))
	fenetre.blit(textsurface, (750, 50))
	pygame.draw.line(fenetre, (0,0,0), [640,49],[835,49])
	pygame.draw.line(fenetre, (0,0,0), [640,82],[835,82])
	pygame.draw.line(fenetre, (0,0,0), [640,110],[835,110])
	pygame.draw.line(fenetre, (0,0,0), [640,49],[640,110])
	pygame.draw.line(fenetre, (0,0,0), [835,49],[835,110])
	pygame.draw.line(fenetre, (0,0,0), [737,49],[737,110])
	if butt_click == 1:
		pygame.draw.rect(fenetre, (0,0,0), [645,135,180,70])
	pygame.draw.rect(fenetre, (255,255,255), [650,140,170,60])
	textsurface = myfont.render('New Game', False, (0,0,0))
	fenetre.blit(textsurface, (685, 149))
	point_one = 0
	point_two = 0
	for had in bb.case_list:
		if had.player == 1:
			point_one = point_one + 1
		if had.player == -1:
			point_two = point_two + 1
	textsurface = myfont.render(str(12-point_two), False, (0,0,0))
	fenetre.blit(textsurface, (680, 80))
	textsurface = myfont.render(str(12-point_one), False, (0,0,0))
	fenetre.blit(textsurface, (780, 80))
	textsurface = myfont.render("MOVE LOG", False, (0,0,0))
	fenetre.blit(textsurface, (690, 230))
	textsurface = myfont.render("BLACKS", False, (0,0,0))
	fenetre.blit(textsurface, (650, 270))
	textsurface = myfont.render("WHITES", False, (0,0,0))
	fenetre.blit(textsurface, (750, 270))
	for black_move in range(0,len(log_blacks)):
		textsurface = myfont.render(str(lines[log_blacks[black_move][0]])+str(columns[log_blacks[black_move][1]])+"->"+str(lines[log_blacks[black_move][2]])+str(columns[log_blacks[black_move][3]]), False, (0,0,0))
		fenetre.blit(textsurface, (750, 300+30*black_move))
	for white_move in range(0,len(log_whites)):
		textsurface = myfont.render(str(lines[log_whites[white_move][0]])+str(columns[log_whites[white_move][1]])+"->"+str(lines[log_whites[white_move][2]])+str(columns[log_whites[white_move][3]]), False, (0,0,0))
		fenetre.blit(textsurface, (650, 300+30*white_move))
	if turni == 1 and game() == 2: 
		pygame.draw.rect(fenetre, (255,0,0), [0,0,500,600])
	if turni == -1 and game() == 2:
		pygame.draw.rect(fenetre, (0,0,255), [0,0,500,600])
	if game() !=2:
		pygame.draw.rect(fenetre, (0,255,0), [0,0,500,600])
	for letter in range(0,8):
		for number in range(0,8):
			textsurface = myfont.render(lines[letter], False, (0,0,0))
			fenetre.blit(textsurface, (50*(letter+1)+15, 50*(number+1)-30))
			textsurface = myfont.render(columns[number], False, (0,0,0))
			fenetre.blit(textsurface, (50*(letter+1)-20, 50*(number+1)+10))
	pygame.draw.rect(fenetre, (255,255,255), [50,450,400,150])
	if game() == 2:
		if suree == 1:
			textsurface = myfont.render('Still has to play', False, (0, 0, 0))
			fenetre.blit(textsurface, (60,550))
		if invalid == 1:
			textsurface = myfont.render('Invalid move', False, (0, 0, 0))
			fenetre.blit(textsurface, (60,550))
		if turni == 1:
			textsurface = myfont.render('Player 1 plays', False, (0, 0, 0))
			fenetre.blit(textsurface, (60,500))
		else :
			textsurface = myfont.render('Player 2 plays', False, (0, 0, 0))
			fenetre.blit(textsurface, (60,500))
	elif game() == 1:
		textsurface = myfont.render('Player 1 won', False, (0, 0, 0))
		fenetre.blit(textsurface, (60,500))
	elif game() == -1:
		textsurface = myfont.render('Player 2 won', False, (0, 0, 0))
		fenetre.blit(textsurface, (60,500))
	else :
		textsurface = myfont.render('Its a tie', False, (0, 0, 0))
		fenetre.blit(textsurface, (60,500))
	for p in range(0,8):
		for q in range(0,8):
			if [p,q] in sur:
				pygame.draw.rect(fenetre, (0,255,0), [50*(p+1),50*(q+1),50,50])
			elif [p,q] in sure:
				pygame.draw.rect(fenetre, (255,255,0), [50*(p+1),50*(q+1),50,50])
			else:
				if (p+q)%2 == 1:
					pygame.draw.rect(fenetre, (255,0,0), [50*(p+1),50*(q+1),50,50])
				else:
					pygame.draw.rect(fenetre, (0,0,255), [50*(p+1),50*(q+1),50,50])
	for i in range(0,8):
		for j in range(0,8):
			if (i+j)%2 == 1:
				pygame.draw.rect(fenetre, (255,0,0), [50*(i+1)+5,50*(j+1)+5,40,40])
			else:
				pygame.draw.rect(fenetre, (0,0,255), [50*(i+1)+5,50*(j+1)+5,40,40])
	for case_pos in l:
		if case_pos[0].player == 1:
			if case_pos[0].king == 0:
				fenetre.blit(ebony, case_pos[1])
			else :
				fenetre.blit(ebony_k, case_pos[1])
		else:
			if case_pos[0].king == 0:
				fenetre.blit(ivory, case_pos[1])
			else:
				fenetre.blit(ivory_k, case_pos[1])
	for i in cap_list:
		pygame.draw.lines(fenetre, (255,255,255), False, from_pos_to_cord_list(i), 3)
		for j in i:
			pygame.draw.circle(fenetre, (255,255,255), [50*(j[0]+1)+25,50*(j[1]+1)+25], 10)
	if game() != 2:
		game_over_text = myotherfont.render('Game Over', False, (187,244,20))
		fenetre.blit(game_over_text, (70,200))

# This function tells us if player "play" has to capture a piece or he can just move to a clear position (prevents an invalid move)
def cap_can(play):
	global l
	for i in l:
		if (i[0].get_caps() != [[],[]]) and (i[0].player == play):
			return 1
	return 0
	
# This is the important function in this script as it evaluates the click of the user (player, turn, capture, ...) and changes the position of the checkers piece on the board
def move_case(i,j,r,m):
	global turni
	global l
	global suree
	k = [i,j]
	if get_case(i,j) == None:
		return 0
	else:
		if ([r,m] in l[get_case(i,j)][0].get_moves()) and cap_can(l[get_case(i,j)][0].player)==0 and turni == l[get_case(i,j)][0].player : 
			l[get_case(i,j)][0].pos = [r,m]
			bb.case_list[get_case(r,m)].pos = [r,m] 
			l[get_case(r,m)][1] = [50*(r+1)+7,50*(m+1)+7]
			if l[get_case(r,m)][0].player == 1 and r==7 and l[get_case(r,m)][0].king == 0 :
				l[get_case(r,m)][0].king = 1
			if l[get_case(r,m)][0].player == -1 and r==0 and l[get_case(r,m)][0].king == 0 :
				l[get_case(r,m)][0].king = 1
			turni = -1*turni
			add_log(i,j,r,m)
			if game() != 2:
				end_sound.play()
			return 1
		elif ([r,m] in l[get_case(i,j)][0].get_caps()[0]) and  turni == l[get_case(i,j)][0].player:
			rm = l[get_case(i,j)][0].get_caps()[0].index([r,m])
			mr = l[get_case(i,j)][0].get_caps()[1][rm]
			l[get_case(i,j)][0].pos = [r,m]
			bb.case_list[get_case(r,m)].pos = [r,m]
			bb.case_list.pop(get_case(*mr))
			l[get_case(r,m)][1] = [50*(r+1)+7,50*(m+1)+7]
			l.pop(get_case(*mr))
			if l[get_case(r,m)][0].player == 1 and r==7 and l[get_case(r,m)][0].king == 0 :
				l[get_case(r,m)][0].king = 1
			if l[get_case(r,m)][0].player == -1 and r==0 and l[get_case(r,m)][0].king == 0 :
				l[get_case(r,m)][0].king = 1
			if l[get_case(r,m)][0].get_caps() == [[],[]]:
				turni = turni*-1
				if suree == 1:
					suree = 0
			if l[get_case(r,m)][0].get_caps() != [[],[]] :
				suree = 1
			add_log(i,j,r,m)
			if game() != 2:
				end_sound.play()
			return 1
	l[get_case(i,j)][1] = [50*(i+1)+7,50*(j+1)+7]
	invalid = 1
	return 0
	
# This function changes the position of the checkers piece on the screen (for the drag and drop)
def drag_case(i,r,m):
	global l
	if l[i] != None:
		l[i][1] = [r,m]
		
# This initializes the list l from the list case_list explained in the comments of file try3 
for case in bb.case_list:
	l.append([case,[50*(case.pos[0]+1)+7,50*(case.pos[1]+1)+7]])
	
# The pygame loop
while continuer == 0:
	for event in pygame.event.get():
		if event.type == QUIT:
			continuer = 1
		if event.type == MOUSEBUTTONDOWN and event.button == 1 and clicked == 0 and game() == 2:
			if from_pos_to_cord(event.pos[0],event.pos[1]) != None:
				if get_case(*from_pos_to_cord(event.pos[0],event.pos[1])) != None :
					clicked = 1
					cap = 1
					case_click = get_case(*from_pos_to_cord(event.pos[0],event.pos[1]))
					sur = l[get_case(*from_pos_to_cord(event.pos[0],event.pos[1]))][0].get_moves()
					sure = l[get_case(*from_pos_to_cord(event.pos[0],event.pos[1]))][0].get_caps()[0]
					cap_list = l[get_case(*from_pos_to_cord(event.pos[0],event.pos[1]))][0].normalize()
		if event.type == MOUSEBUTTONDOWN and event.button == 1 and (event.pos[0]>650 and event.pos[0]<820) and (event.pos[1]>140 and event.pos[1]<200):
			butt_click = 1
		if event.type == MOUSEBUTTONUP and event.button == 1 and (event.pos[0]>650 and event.pos[0]<820) and (event.pos[1]>140 and event.pos[1]<200):
			butt_click = 0
			l = []
			bb = board()
			sur = []
			sure = []
			clicked = 0
			cap_list = []
			case_click = None
			turni = 1
			log_blacks = []
			log_whites = []
			for case in bb.case_list:
				l.append([case,[50*(case.pos[0]+1)+7,50*(case.pos[1]+1)+7]])
		if event.type == MOUSEMOTION and clicked == 1:
			drag_case(case_click,event.pos[0]-15,event.pos[1]-15)
		if event.type == MOUSEBUTTONUP and clicked == 1:
			if from_pos_to_cord(event.pos[0],event.pos[1]) != None:
				if move_case(*l[case_click][0].pos,*from_pos_to_cord(event.pos[0],event.pos[1])) == 0:
					invalid = 1
				else :
					invalid = 0
			else :
				move_case(*l[case_click][0].pos,*l[case_click][0].pos)
				invalid = 1
			sur = []
			sure = []
			clicked = 0
			cap_list = []
			case_click = None
			check_sound.play()
	show_board()
	pygame.display.flip()
