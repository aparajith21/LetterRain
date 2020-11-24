import GenerateLetters
import WordScore
import pygame
from random import choices
from random import uniform
from math import exp
import sys

# Define width and height of img
IMG_WIDTH = 64
IMG_HEIGHT = 64

# Define window size
WIN_WIDTH = 576
WIN_HEIGHT = 1024
WIN_SIZE = (WIN_WIDTH,WIN_HEIGHT)

# Define offset for score display
OFFSET = 100

# function create letters on the screen
def createLetters(letter_knt,generated_letters):
	new_generated_letters = GenerateLetters.GenerateLetters(letter_knt)
	generated_letters.extend(new_generated_letters)

	letter_surface = []
	indx = 0
	for letter in new_generated_letters:
		x = int(uniform((WIN_WIDTH / letter_knt) * indx, (WIN_WIDTH / letter_knt) * (indx + 1) - IMG_WIDTH)) + IMG_WIDTH / 2
		y = OFFSET
		letter_surface.append(LETTERS[letter.upper()].get_rect(center = (x,y)))
		indx += 1
	return letter_surface

# define function to move the letters downward
def moveLetters(letters):
	for letter in letters:
		letter.centery += gravity
	return letters

# Utility function to draw the letter on the screen
def drawLetters(letters,generated_letters):
	indx = 0
	while(indx < len(letters)):
		# Check for out of window letters
		if letters[indx].centery < WIN_HEIGHT:
			screen.blit(LETTERS[generated_letters[indx].upper()],letters[indx])
			indx += 1
		else:
			# remove those letters from the list and update list
			letters.pop(indx)
			generated_letters.pop(indx)

# Utility function to check collision with catch_box
def checkCollision(character, letters, generated_letters):
	for indx in range(0,len(letters)):
		if((chr(character).upper() == generated_letters[indx]) and catch_box.colliderect(letters[indx])):
			return indx
	return -1

def wordFormed(word):
	"""Display word formed at the top of the window"""
	X_OFFSET = 100
	word_length = len(word)
	# nothing to display
	if not word_length:
		return None
	# understand space density for word display
	letter_space = (WIN_WIDTH - X_OFFSET) // word_length
	if letter_space > 64:
		tile_size = 64
	else:
		tile_size = letter_space
	#display word
	for indx in range(word_length):
		x = X_OFFSET + indx * tile_size
		y = 0
		# scale word based on tile size
		img = pygame.transform.scale(LETTERS[word[indx].upper()], (tile_size, tile_size))
		screen.blit(img, (x, y))

# Function to evaluate the current word
def evaluateWord():
	global score, curr_word
	print(curr_word)
	words_formed.append(curr_word)
	score += WordScore.WordScore(curr_word)
	curr_word = ""

# Close function
def exitGame():
	global score
	pygame.quit()
	print("Score: ", score)
	sys.exit()

# Initiate the game
pygame.init()

# initialise font
pygame.font.init()
# Get font
font = pygame.font.Font('assets/fonts/AvenirMedium.ttf', 18)

# game variables
gravity = 2
game_active = False
words_formed = []
curr_word = ""
score = 0

# Level Information
level = 0
TARGET_SCORE = [10,20,30,40,50]
LVL_TIMEOUT = 120
counter = 0

# Define FPS & SPAWN_TIME
FPS = 60
SPWN_TIME = 800

# Draw display surface
screen = pygame.display.set_mode(WIN_SIZE)
clock = pygame.time.Clock()

# Import bg surface
bg_surface = pygame.image.load('assets/background-day.png').convert()
bg_surface = pygame.transform.scale2x(bg_surface)

# Define the catch section
catch_surface = pygame.Surface((WIN_WIDTH,100))
catch_surface.set_alpha(128)
catch_surface.fill((255,255,255))

catch_box = catch_surface.get_rect(center = ((WIN_WIDTH/2,WIN_HEIGHT/2)))

# Create dictionary of the letter and image surface corresponding to it
LETTERS = list(map(chr, range(65, 91)))
LETTERS = {char : pygame.image.load('assets/letters/' + char + '.jpg').convert() for char in LETTERS}

# Update letter cnt and letter_cnt_pop
letter_knt_weights = [1/(1 + exp(i)) for i in range(15)]
letter_knt_population = [i for i in range(1, 16)]
letters = []
generated_letters = []
ascii_letters = [i for i in range(97,123)]

# Create timed event to spawn letters
SPAWNLETTER = pygame.USEREVENT
pygame.time.set_timer(SPAWNLETTER, SPWN_TIME)

#Create a timer event that runs for every second
TIMER = pygame.USEREVENT + 1
pygame.time.set_timer(TIMER, 1000)

# Game Loop
while True:

	# Event Loop
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			exitGame()

		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_SPACE and game_active == False:
				# Start the game - init all game variables
				game_active = True
				letters = []
				generated_letters = []
				level = 0
				counter = LVL_TIMEOUT

			if event.key in ascii_letters:
				indx = checkCollision(event.key, letters, generated_letters)
				if indx >= 0:
					# Remove those letters from list and add to word
					curr_word = curr_word + generated_letters[indx]
					generated_letters.pop(indx)
					letters.pop(indx)

			if event.key == pygame.K_RETURN:
				evaluateWord()
				
		if event.type == SPAWNLETTER and game_active == True:
			letter_knt = choices(population = letter_knt_population, weights = letter_knt_weights)[0]
			letters.extend(createLetters(letter_knt,generated_letters))

		# For every second update counter
		if event.type == TIMER and game_active == True:
			counter -= 1


	# When game is active
	if game_active:

		# Check for TIMEOUT
		if counter == 0:
			if score >= TARGET_SCORE[level]:
				print("Congrats. Passed to next level")
				level += 1
				counter = LVL_TIMEOUT
			else:
				print("Game Over")
				evaluateWord()
				exitGame()

		# Display bg surface
		screen.blit(bg_surface,(0, 0))
		
		# Display score
		# displayLevelInfo(score)
		text = font.render(f'Score: {score}', True, (0, 0, 0))
		screen.blit(text, (0, 0))

		# Display timer
		timer_txt = font.render(f'Time Remaining: {counter}',True,(0,0,0))
		screen.blit(timer_txt,(WIN_WIDTH-timer_txt.get_width() - 30,0))

		# Display the catching region
		screen.blit(catch_surface, catch_box)

		# Move the letters
		letters = moveLetters(letters)
		drawLetters(letters,generated_letters)

		# Display word formed so far
		wordFormed(curr_word)
		# Update display
		pygame.display.update()
		clock.tick(FPS)