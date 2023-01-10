# main.py

from pathlib import Path
ROOT = Path(__file__).parent.absolute()

from graphics import *
GW = GraphWin('Mad Rooks', 1000, 615)

from random import choice
from math import floor

from webbrowser import open_new_tab

BLUE = color_rgb(0, 113, 187)
RED = color_rgb(238, 28, 37)
SQUARE_SIZE = 55
X_OFFSET = 25



# Create the Game Pieces.
class Piece():
	
	def __init__(self, top_corner, name, piece_num):
		
		center_x = top_corner.x + SQUARE_SIZE / 2
		center_y = top_corner.y + SQUARE_SIZE / 2
		radius = floor(SQUARE_SIZE / 2) - 4

		color = BLUE if piece_num % 2 == 0 else RED

		self.circle = Circle(Point(center_x, center_y), radius)
		self.circle.setFill(color)
		self.circle.setWidth(2)
		self.circle.draw(GW)

		self.color = color
		self.x = center_x
		self.y = center_y
		self.hidden = False

		self.name = name

	def select(self):
		self.circle.setOutline('gold')
		self.circle.setWidth(5)

	def unselect(self):
		self.circle.setOutline('black')
		self.circle.setWidth(2)
	
	def draw(self):
		self.unselect()
		self.circle.draw(GW)

	def undraw(self):
		self.hidden = True
		self.circle.undraw()

	def change_color(self, new_color):
		self.circle.setFill(new_color)
		self.color = new_color

		if self.hidden:
			self.hidden = False
			self.draw()


# Create the messages for each player.
class TurnMessage():

	def __init__(self, player_name, color, name_offset):
		y_offset = 540
		self.name_text = Text(Point(X_OFFSET, y_offset), player_name)
		self.name_text.setFill(color)
		self.name_text.setStyle('bold')

		self.message_text = Text(Point(name_offset, y_offset - 1), "'s Turn")

	def show(self):
		self.name_text.draw(GW)
		self.message_text.draw(GW)

	def hide(self):
		self.name_text.undraw()
		self.message_text.undraw()

	def change_text(self, text):
		self.message_text.setText(text)


# Create the message that tells if a move is invalid.
class InvalidMessage():
	
	def __init__(self):
		self.text = Text(Point(X_OFFSET, 580))
		self.text.setSize(15)
		self.text.draw(GW)
	
	# Remove the text, hidding the textbox.
	def clear(self):
		self.text.setText("")

	# Update the textbox to tell the players what invalid moves were attempted.
	# If header is set to false, it removes the 'Invalid Move: ' header so the
	# 	exit game message can be displayed.
	def update(self, message, header=True):
		self.text.setText(f'Invalid Move: {message}')
		if not header: self.text.setText(f'{message}')


def main():
	
	# Place the game title and rules on the GraphWin
	draw_title()
	draw_rules()

	# grid_origin is a tuple composed of the xy-coordinates for the
	# 	upper-left corner of the grid.
	# pieces is a 2D-array storing the locations of all of the players' pieces.
	grid_origin, pieces = draw_board()

	# red_message is a tuple storing the two text elements that tell the
	# 	players that it is BLUE's turn.
	# blue_message is the same, but for the text saying it's RED's turn.
	red_message, blue_message = draw_player_messages()

	# invalid_message is a text box that explains why a player cannot make
	# 	a certain move.
	invalid_message = draw_invalid_move_textbox()

	# red_turn is a boolean that tells who's turn it is. If true, it is BLUE's
	# 	turn, else it it RED's turn.
	red_turn = True


	# The main game loop.
	turn_count = 0
	while True:

		turn_count += 1

		take_turn(red_turn, grid_origin, invalid_message, pieces)

		if winner(pieces, red_message, blue_message, invalid_message, turn_count):
			GW.getKey()
			return

		red_turn = swap_turn(red_turn, red_message, blue_message)


# Adds the game title to the game window.
def draw_title():
	titles = ['Mad Rooks', 'Mad Castles', 'Upset Towers', 'Disheartened Obelisks']
	title_choice = choice(titles)
	title = Text(Point(X_OFFSET, 15), title_choice)
	title.setSize(25)
	title.setTextColor('red')
	title.setStyle('bold')
	title.draw(GW)

	subtitle = Text(Point(X_OFFSET, 60), 
		'AKA Mad Rooks, a game by Mark Steere' if title_choice != 'Mad Rooks' else 'A game by Mark Steere'
	)
	subtitle.setSize(13)
	subtitle.draw(GW)


# Adds instructions for how to play the game to the game window.
def draw_rules():
	y_offset = 85

	how_to_play_title = Text(Point(X_OFFSET + 500, y_offset), 'How To Play')
	how_to_play_title.setSize(25)
	how_to_play_title.setStyle('bold')
	how_to_play_title.draw(GW)

	how_to_play_text = Text(Point(X_OFFSET + 500, y_offset + 35), 
		'''
1. Click a piece to select it. Click it
    again to unselect.
2. Click a separate space after
    selecting a piece to move it to that
    location.
3. Winner is decided when all of the
    other player's pieces are removed 
    from the board.
		''')
	how_to_play_text.draw(GW)


	button_center = Point(750, y_offset + 385)
	button_background = Rectangle(
		Point(button_center.x - 90, button_center.y - 22),
		Point(button_center.x + 90, button_center.y + 22)
	)
	button_background.setFill("lemonchiffon")
	button_background.draw(GW)

	button = Text(button_center, "Learn More")
	button.setFill(color_rgb(100, 0, 0))
	button.setAnchor("c")
	button.draw(GW)




# Adds the grid and the game pieces to the game window.
def draw_board():
	y_offset = 90

	pieces = []

	for i in range(8):
		column = []

		for j in range(8):
			p1 = Point(X_OFFSET + (i * SQUARE_SIZE), y_offset + (j * SQUARE_SIZE))
			p2 = Point(X_OFFSET + ((i + 1) * SQUARE_SIZE), y_offset + ((j + 1) * SQUARE_SIZE))
			
			square = Rectangle(p1, p2)
			square.setFill(
				color_rgb(240, 246, 237) if (i + j) % 2 == 0 else color_rgb(210, 231, 185)
			)
			square.setWidth(3)
			square.draw(GW)
			
			piece = Piece(p1, (i *8) + j, j + i)
			column.append(piece)

		pieces.append(column)
	

	return (X_OFFSET, y_offset), pieces


# Adds messages to tell the players whose turn it is, and who won.
def draw_player_messages():

	red_message = TurnMessage('RED', RED, 85)
	blue_message = TurnMessage('BLUE', BLUE, 102)
	
	# Red goes first, to preemptively show their message.
	red_message.show()

	return red_message, blue_message


# Adds a hidden textbox that tells the players when they attempt to make an
# 	invalid move.
def draw_invalid_move_textbox():
	text = InvalidMessage()
	return text


# Main driver for each turn in the game.
# player_turn is a boolean, where True indicates it is Red's turn and False
# 	indicates Blue
# grid_origin is a tuple with the true xy-coordinates on the game window where
# 	the grid tiles start.
# invalid_message is the textbox that tells if the players make an invalid move
# pieces is a 2D array that stores the references to all the game pieces.
def take_turn(player_turn, grid_origin, invalid_message, pieces):

	player_color = RED if player_turn else BLUE

	while True:
		
		# Check to see if the player has clicked inside the grid.
		starting_loc = valid_click(GW.getMouse(), grid_origin)
		if starting_loc:
			
			# Clear the invalid move textbox.
			invalid_message.clear()

			# starting_piece is the piece the player wants to select.
			starting_piece = pieces[starting_loc[0]][starting_loc[1]]

			# If the clicked piece's hidden flag is True, then that space is
			# 	actually unoccupied and does not count as a selection.
			if starting_piece.hidden:
				continue

			# If the starting piece is not that player's color, it belongs to
			# 	the opponent and cannot count as a selection.
			elif starting_piece.color != player_color:
				invalid_message.update("That is not your piece.")

			else:
				starting_piece.select()

				while True:

					ending_loc = valid_click(GW.getMouse(), grid_origin)
					if ending_loc:
						
						# Clear the invalid move textbox.
						invalid_message.clear()

						ending_piece = pieces[ending_loc[0]][ending_loc[1]]


						# Unselect the piece.
						if ending_piece == starting_piece:
							starting_piece.unselect()
							break

						
						# Find all the local pieces that are killable.
						killable_pieces = can_kill(starting_loc, player_color, pieces)

						# Check if the movement is orthogonal.
						if not orthogonal(starting_loc, ending_loc):
							invalid_message.update("Pieces can only move orthogonally.")
						
						# Check if the player is trying to take their own piece.
						elif not ending_piece.hidden and starting_piece.color == ending_piece.color:
							invalid_message.update("You cannot kill your own pieces.")

						# Check if there are pieces in the way of the movement.
						elif blocked(starting_loc, ending_loc, pieces):
							invalid_message.update("There are other pieces in the way.")

						# Check if there are killable pieces, and if the movement
						# 	is to one of those pieces.
						elif killable_pieces != [] and ending_piece.name not in killable_pieces:
							invalid_message.update("That piece can kill another.")

						# Check if the player is engaging an enemy piece
						elif not_engaging(ending_loc, player_color, pieces):
							invalid_message.update("Pieces must engage or kill another.")


						# Else, the move is valid so perform it.
						else:
							move_piece(starting_piece, ending_piece)
							return


# Determines if the clicked location is on the game board.
# If so, return a tuple with xy-coordinates scaled for the game board.
def valid_click(click_loc, origin_point):

	min_x, min_y = origin_point
	max_x = min_x + (8 * SQUARE_SIZE)
	max_y = min_y + (8 * SQUARE_SIZE)

	if (min_x <= click_loc.x <= max_x) and (min_y <= click_loc.y <= max_y):
		return (
			floor((click_loc.x - min_x) / SQUARE_SIZE),
			floor((click_loc.y - min_y) / SQUARE_SIZE)
		)

	if (660 <= click_loc.x <= 840) and (443 <= click_loc.y <= 487):
		open_new_tab("http://www.marksteeregames.com/Mad_Rooks_rules.pdf")


# Determine if p1 is orthogonal to p2.
# p1 and p2 are both tuples with xy-coordinates.
def orthogonal(p1, p2):
	return (p1[0] == p2[0]) or (p1[1] == p2[1])


# Determine if there are any pieces in the way between p1 and p2.
def blocked(p1, p2, board):

	x_pointer, y_pointer = p1

	# Check Upwards
	if p2[1] < p1[1]:
		while x_pointer > p2[0]:
			x_pointer -= 1
			if not board[x_pointer][y_pointer].hidden:
				return True

	# Check Downwards
	elif p2[1] > p1[1]:
		while x_pointer < p2[0]:
			x_pointer += 1
			if not board[x_pointer][y_pointer].hidden:
				return True

	# Check Leftwards
	elif p2[0] < p1[0]: 
		while y_pointer > p2[1]:
			y_pointer -= 1
			if not board[x_pointer][y_pointer].hidden:
				return True

	# Check Rightwards
	else:
		while y_pointer < p2[1]:
			y_pointer += 1
			if not board[x_pointer][y_pointer].hidden:
				return True

	return False


# Find if the provided piece has anybody it can kill.
# start is a tuple with the xy-coordinates of the piece to check.
# player_color is the color of the player's piece
# board is the 2D array of all game pieces.
def can_kill(start, player_color, board):

	# kills[] will be a list of the names of all the possible pieces to kill.
	kills = []

	# Check Up
	up_kill = check_direction(start, player_color, board, 0, -1)

	# Check Down
	down_kill = check_direction(start, player_color, board, 0, 1)

	# Check Left
	left_kill = check_direction(start, player_color, board, -1, 0)

	# Check Right
	right_kill = check_direction(start, player_color, board, 1, 0)

	# If any of the above returned something, add that piece's name to kills[].
	if up_kill: kills.append(up_kill.name)
	if down_kill: kills.append(down_kill.name)
	if left_kill: kills.append(left_kill.name)
	if right_kill: kills.append(right_kill.name)

	return kills


# Determine if a piece has anybody it can kill.
# This is done through DFS recursion, because it is unknown how many empty
# 	spaces there are between the piece and anybody it might kill.
# start is the xy-coordinates of the piece.
# start_color is the color of the original piece before to the recursion begins.
# board is the 2D array of all game pieces.
# x_dir and y_dir are two independent numbers in the range [-1, 1], and indicate
# 	which direction the DFS searching will procede.
def check_direction(start, start_color, board, x_dir, y_dir):

	# The shifted coordinates to check
	x_coord = start[0] + x_dir
	y_coord = start[1] + y_dir

	# If either coordinate of the tile is -1 or 9, it is out of bounds and
	# 	should immediately return.
	if -1 in [x_coord, y_coord] or 8 in [x_coord, y_coord]:
		return

	# The reference to the piece to be checked
	check_loc = board[x_coord][y_coord]

	# If the piece is not hidden, and it belongs to the opposing player, return
	# 	it.
	# Otherwise, return nothing since the piece already belongs to the player.
	if not check_loc.hidden:
		if check_loc.color != start_color:
			return check_loc
		return 

	# Otherwise, there is not piece on the space, so recurse deeper from the new
	# 	starting coordinates.
	return check_direction((x_coord, y_coord), start_color, board, x_dir, y_dir)


# Determine whether a piece if moved to the proposed location would be engaging
# 	an enemy's piece for killing.
# proposed_location is a tuple with xy-coordinates of where a piece wants to
# 	move to.
# player_color is the color of the piece that will be moved.
# board is the 2D array of all game pieces.
def not_engaging(proposed_location, player_color, board):

	# First determine if the proposed space is empty.
	# Then, if the piece can kill an opposing piece, via the transitive property
	# 	that opposing piece will be able to kill the player's piece and thus is
	# 	engaging it.
	if board[proposed_location[0]][proposed_location[1]].hidden:
		kills = can_kill(proposed_location, player_color, board)

		if kills == []:
			return True
	return False


# Move the piece by hiding it and recoloring the piece it would be taking.
# start is a reference to the original piece.
# end is a reference to the piece that will be "moved" to.
def move_piece(start, end):
	start.undraw()
	end.change_color(start.color)


# Determine if there are any winners.
# board is the 2D array of all game pieces.
# red_message, blue_message, and invalid_message are references to each player's
# 	respective message box, as well as the box for telling if a move was
# 	invalid.
# turn_count is how many turns have already taken place.
def winner(board, red_message, blue_message, invalid_message, turn_count):
	red = 0
	blue = 0
	for column in board:
		for item in column:
			if not item.hidden:
				if item.color == RED: red += 1
				else: blue += 1

	# If both Red and Blue still have pieces left, return False.
	if red > 0 and blue > 0:
		return False

	# Otherwise, change the message boxes to show who won, how many turns it
	# 	took, and how to end the program.
	else:
		if red > 0: red_message.change_text(f' won after {turn_count} turns!')
		else: blue_message.change_text(f' won after {turn_count} turns!')
		invalid_message.update("Press any key to exit.", header=False)
		return True


# Swap who's turn and which player message box to display.
# turn is a boolean that if True means to swap Red's turn to Blue's, and vice
# 	versa for false.
# red and blue are references to each player's respective message box.
def swap_turn(turn, red, blue):

	# If 
	if turn:
		red.hide()
		blue.show()
	else:
		blue.hide()
		red.show()
	
	return not turn


if __name__ == '__main__':
	print('\n\033[92mRunning main.py\n\033[0m')
	try:
		main()

	except Exception as e:
		print(f'\033[91m{e}\033[0m')