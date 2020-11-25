import GenerateLetters
import WordScore
import pygame
from random import choices
from random import uniform
from math import exp
import sys

# Define width and height of img
IMG_WIDTH = 48
IMG_HEIGHT = 48

# Define window size
WIN_WIDTH = 780
WIN_HEIGHT = 1024
WIN_SIZE = (WIN_WIDTH,WIN_HEIGHT)

# Define offset for score display
OFFSET = 130

def createLetters(letter_knt,generated_letters):
    """
    Create letters to be displayed on screen.
    It inputs the number of new letters to be generated, calls the GenerateLetters
    function and then returns a letter surface for display
    """
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

def moveLetters(letters):
    """
    Move the letters on screen downwards using gravity
    """
    for letter in letters:
        letter.centery += gravity
    return letters

def drawLetters(letters,generated_letters):
    """
    Utility function to draw the letter on the screen
    """
    indx = 0
    while(indx < len(letters)):
        # Check for out of window letters
        if letters[indx].centery < WIN_HEIGHT - 200:
            screen.blit(LETTERS[generated_letters[indx].upper()],letters[indx])
            indx += 1
        else:
            # remove those letters from the list and update list
            letters.pop(indx)
            generated_letters.pop(indx)

def checkCollision(character, letters, generated_letters):
    """
    Utility function to check collision with catch_box
    """
    for indx in range(0,len(letters)):
        if((chr(character).upper() == generated_letters[indx]) and catch_box.colliderect(letters[indx])):
            return indx
    return -1

def wordFormed(word):
    """
    Display word formed at the top of the window
    """
    X_OFFSET = 180
    word_length = len(word)
    # nothing to display
    if not word_length:
        return None
    # understand space density for word display
    letter_space = (WIN_WIDTH - X_OFFSET) // word_length
    if letter_space > IMG_WIDTH:
        tile_size = IMG_WIDTH
    else:
        tile_size = letter_space - 5
    #display word
    for indx in range(word_length):
        x = X_OFFSET + indx * tile_size
        y = 65
        # scale word based on tile size
        img = pygame.transform.scale(LETTERS[word[indx].upper()], (tile_size, tile_size))
        screen.blit(img, (x, y))

def evaluateWord():
    """
    Function to evaluate the current word
    """
    global score, curr_word
    print(curr_word)
    words_formed.append(curr_word)
    score += WordScore.WordScore(curr_word)
    curr_word = ""

def displayHeader(curr_score, curr_time):
    """
    Function to display the headlines - time, score and level information
    """

    # Display timer
    screen.blit(time_display_surface, (10,10))
    timer_txt = font.render(f'{counter}',True,(0,0,0))
    screen.blit(timer_txt,(80, 25))

    # Display score
    screen.blit(score_display_surface, (WIN_WIDTH - 160,10))
    score_txt = font.render(f'{score}', True, (0, 0, 0))
    screen.blit(score_txt, (WIN_WIDTH-80, 25))

def exitGame():
    """
    Close the game
    """
    global score
    pygame.quit()
    print("Score: ", score)
    sys.exit()

# Initiate the game
pygame.init()

# initialise font
pygame.font.init()

# initialise music mixer
pygame.mixer.init()
pygame.mixer.music.load('assets/bgm.ogg')
 # set volume and play clair de lune infinitely
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)

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
paused = False

# Define FPS & SPAWN_TIME
FPS = 60
SPWN_TIME = 800

# Draw display surface
screen = pygame.display.set_mode(WIN_SIZE)
clock = pygame.time.Clock()

# Import bg surface
bg_surface = pygame.image.load('assets/bg.png').convert()
bg_surface = pygame.transform.scale(bg_surface,(WIN_WIDTH,WIN_HEIGHT))

# Define the catch section
catch_surface = pygame.Surface((WIN_WIDTH,100))
catch_surface.set_alpha(128)
catch_surface.fill((255,255,255))

catch_box = catch_surface.get_rect(center = ((WIN_WIDTH/2,WIN_HEIGHT/2)))

# Create pause mask
paused_mask = pygame.Surface((WIN_WIDTH,WIN_HEIGHT))
paused_mask.set_alpha(128)
paused_mask.fill((255,255,255))
paused_mask_box = paused_mask.get_rect(center = ((WIN_WIDTH/2,WIN_HEIGHT/2)))

# Import paused text
paused_txt_surface = pygame.image.load('assets/paused.png').convert_alpha()
paused_txt_surface = pygame.transform.scale(paused_txt_surface,(300,100))
paused_txt_box = paused_txt_surface.get_rect(center = ((WIN_WIDTH/2,WIN_HEIGHT/2)))

# Import pause button
pause_btn_surface = pygame.image.load('assets/pause.png').convert_alpha()
pause_btn_surface = pygame.transform.scale(pause_btn_surface,(50,50))
pause_btn_box = pause_btn_surface.get_rect(center = ((WIN_WIDTH - 30,WIN_HEIGHT - 30)))

# Import play button
play_btn_surface = pygame.image.load('assets/play.png').convert_alpha()
play_btn_surface = pygame.transform.scale(play_btn_surface,(50,50))
play_btn_box = play_btn_surface.get_rect(center = ((WIN_WIDTH - 30,WIN_HEIGHT - 30)))

# Import time headline
time_display_surface = pygame.image.load('assets/time.png').convert_alpha()
time_display_surface = pygame.transform.scale(time_display_surface, (150,50))

# Import score headline
score_display_surface = pygame.image.load('assets/money.png').convert_alpha()
score_display_surface = pygame.transform.scale(score_display_surface, (150,50))

# Create dictionary of the letter and image surface corresponding to it
LETTERS = list(map(chr, range(65, 91)))
LETTERS = {char : pygame.image.load('assets/letters/' + char + '.jpg').convert() for char in LETTERS}
for letter in LETTERS.keys():
    LETTERS[letter] = pygame.transform.scale(LETTERS[letter], (IMG_WIDTH,IMG_HEIGHT))

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

            if event.key in ascii_letters and game_active == True:
                indx = checkCollision(event.key, letters, generated_letters)
                if indx >= 0:
                    # Remove those letters from list and add to word
                    curr_word = curr_word + generated_letters[indx]
                    generated_letters.pop(indx)
                    letters.pop(indx)

            if event.key == pygame.K_RETURN and game_active == True:
                evaluateWord()

            if event.key == pygame.K_ESCAPE:
                if game_active == True:
                    paused = True
                    game_active = False
                else:
                    paused = False
                    game_active = True
    
        if event.type == SPAWNLETTER and game_active == True:
            letter_knt = choices(population = letter_knt_population, weights = letter_knt_weights)[0]
            letters.extend(createLetters(letter_knt,generated_letters))

        if event.type == pygame.MOUSEBUTTONUP:
            if paused == False:
                if(pause_btn_box.collidepoint(pygame.mouse.get_pos())):
                    paused = True
                    game_active = False
            else:
                if(play_btn_box.collidepoint(pygame.mouse.get_pos())):
                    paused = False
                    game_active = True

        # For every second update counter
        if event.type == TIMER and game_active == True:
            counter -= 1

    # When game is active
    if game_active == True:

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
        
        # Display headline
        displayHeader(score,counter)        

        # Display the catching region
        screen.blit(catch_surface, catch_box)

        # Move the letters
        letters = moveLetters(letters)
        drawLetters(letters,generated_letters)

        # Display word formed so far
        wordFormed(curr_word)

        # Display pasue button
        screen.blit(pause_btn_surface, pause_btn_box)

    if paused == True:
        screen.blit(bg_surface,(0, 0))
        screen.blit(paused_mask, paused_mask_box)
        screen.blit(paused_txt_surface,paused_txt_box)
        screen.blit(play_btn_surface, play_btn_box)

    # Update display
    pygame.display.update()
    clock.tick(FPS)
