import GenerateLetters
import WordScore
import pygame
from random import choices
from random import uniform
from math import exp
from math import ceil
import sys, time 
import csv

# Define width and height of img
IMG_WIDTH = 48
IMG_HEIGHT = 48

# Define window size
WIN_WIDTH = 780

# Define offset for score display
OFFSET = 80

# define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (200, 200, 255)

# define a class to maintain letter popped and animation state
class Blast:
    def __init__(self,letter_surface,state):
        self.letter_surface = letter_surface
        self.state = 0

# read leaderboard
f = open('leaderboard.csv', 'r+')
leaderboard = [person for person in csv.reader(f)]

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
        if letters[indx].centery < WIN_HEIGHT:
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
    Y_OFFSET = 10
    word_length = len(word)
    # nothing to display
    if not word_length:
        return None
    # understand space density for word display
    letter_space = ceil((WIN_WIDTH - 2 * X_OFFSET) / word_length)
    if letter_space > IMG_WIDTH:
        tile_size = IMG_WIDTH
    else:
        tile_size = letter_space
    #display word
    for indx in range(word_length):
        x = (WIN_WIDTH - letter_space * word_length) // 2 + indx * tile_size
        y = Y_OFFSET + (IMG_WIDTH - tile_size) // 2
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

def displayPauseScreen():
    """
    Display function for the pause screen
    """
    screen.blit(bg_surface,(0, 0))
    screen.blit(paused_mask, paused_mask_box)
    screen.blit(paused_txt_surface,paused_txt_box)
    screen.blit(play_btn_surface, play_btn_box)
    screen.blit(restart_btn_surface, restart_btn_box)
    screen.blit(close_btn_surface, close_btn_box)

def startGame():
    """
    function to init parameters to start the game
    """
    global game_active, paused, letters, generated_letters, level, score, counter, curr_word
    game_active = True
    paused = False
    letters = []
    generated_letters = []
    score = 0
    curr_word = ""
    counter = LVL_TIMEOUT

def startLevel():
    """
    function to do the level start animation
    """
    global lvl_animate, level

    screen.blit(bg_surface,(0, 0))

    if lvl_animate <= 2:
        screen.blit(level_surface, (WIN_WIDTH/2 - 180, WIN_HEIGHT/2 - 100))
        screen.blit(NUMBERS[str(level + 1)], (WIN_WIDTH/2 + 50, WIN_HEIGHT/2 - 110))

    if lvl_animate == 3:
        screen.blit(NUMBERS[str(3)],(WIN_WIDTH/2 - 50, WIN_HEIGHT/2 - 100))

    if lvl_animate == 4:
        screen.blit(NUMBERS[str(2)],(WIN_WIDTH/2 - 50, WIN_HEIGHT/2 - 100))

    if lvl_animate == 5:
        screen.blit(NUMBERS[str(1)],(WIN_WIDTH/2 - 50, WIN_HEIGHT/2 - 100))

    if lvl_animate == 6:
        lvl_animate = 0
        startGame()
    
def nextLevel():
    """
    Function that does the level score display
    """

    global nxt_lvl_animate, lvl_animate, level, score, total_score, TARGET_SCORE

    total_score += score

    screen.blit(bg_surface,(0, 0))

    if nxt_lvl_animate <= 2:
        screen.blit(lvl_completed_surface, (WIN_WIDTH/2 - 180, WIN_HEIGHT/2 - 100))
    else:
        screen.blit(bg_score_level,  (WIN_WIDTH/2 - 180, WIN_HEIGHT/2 - 180))
        screen.blit(bg_score_table,  (WIN_WIDTH/2 - 150, WIN_HEIGHT/2 - 170))
        screen.blit(win_level_surface, (WIN_WIDTH/2 - 180, WIN_HEIGHT/2 - 250))
        level_score_lbl = score_font.render('YOUR SCORE', True, (0,0,0))
        level_score_txt = score_font.render(str(score), True, (1,1,0))
        screen.blit(nxt_btn_surface, nxt_btn_box)
        screen.blit(close_btn_surface_1, close_btn_box_1)
        screen.blit(restart_btn_surface_1, restart_btn_box_1)
        screen.blit(level_score_lbl, (WIN_WIDTH/2 - 70, WIN_HEIGHT/2))
             
        if nxt_lvl_animate > 3 and nxt_lvl_animate <= 4:
            screen.blit(level_score_txt, (WIN_WIDTH/2, WIN_HEIGHT/2 + 50))
            screen.blit(no_star_surface, (WIN_WIDTH/2 - 110, WIN_HEIGHT/2 - 120))
            screen.blit(level_score_txt, (WIN_WIDTH/2, WIN_HEIGHT/2 + 50))

        if nxt_lvl_animate > 4: 
            screen.blit(level_score_txt, (WIN_WIDTH/2, WIN_HEIGHT/2 + 50))
            if score < 2 * TARGET_SCORE[level]:
                screen.blit(one_star_surface, (WIN_WIDTH/2 - 110, WIN_HEIGHT/2 - 120))
            elif score < 3 * TARGET_SCORE[level]:
                screen.blit(two_star_surface, (WIN_WIDTH/2 - 110, WIN_HEIGHT/2 - 120))
            else:
                screen.blit(three_star_surface, (WIN_WIDTH/2 - 110, WIN_HEIGHT/2 - 120))

def gameOver():
    """
    Function to display "Game Over"
    """

    global game_over_animate

    screen.blit(bg_surface,(0, 0))

    if game_over_animate <= 3:
        game_over_txt = game_over_font.render('GAME OVER', True, (0,0,0))
        screen.blit(game_over_txt, (WIN_WIDTH/2 - 120, WIN_HEIGHT/2 - 100))
    else:
        game_over_animate = 0
        exitGameMenu()



def displayLeaderboard():
    """
    Prints leaderboard on the game window
    """

    global leaderboard

    Y_OFFSET = 50
    TOP_OFFSET = 150

    leaderboard_title = largeFont.render("Leader Board", True, BLACK)
    leaderboard_titleRect = leaderboard_title.get_rect()
    leaderboard_titleRect.center = ((WIN_WIDTH / 2), 50)
    screen.blit(leaderboard_title, leaderboard_titleRect)

    for idx, person in enumerate(leaderboard):
        person_entry_txt = person[0] + '.'
        person_entry_txt += ('    ') + person[1]

        leaderboard_entry = mediumFont.render(person_entry_txt, True, BLACK)
        leaderboard_entryRect = leaderboard_entry.get_rect()
        leaderboard_entryRect.bottomleft = ((WIN_WIDTH / 4), TOP_OFFSET + Y_OFFSET * idx)
        screen.blit(leaderboard_entry, leaderboard_entryRect)

        score_entry_txt = person[2]
        rightAlign = mediumFont.size(person[2])[0]

        leaderboard_entryScore = mediumFont.render(score_entry_txt, True, BLACK)
        leaderboard_entryScoreRect = leaderboard_entryScore.get_rect()
        leaderboard_entryScoreRect.bottomleft = ((3 * WIN_WIDTH / 4) - rightAlign, TOP_OFFSET + Y_OFFSET * idx)
        screen.blit(leaderboard_entryScore, leaderboard_entryScoreRect)

def updateLeaderboard(text):
    """
    Updates the leaderboard if person is a leader
    """
    global score, leaderboard
    flag = 0
    for idx, person in enumerate(leaderboard):
        if int(person[2]) < score:
            flag = idx + 1
            break
    boardSize = len(leaderboard)
    if not flag and boardSize < 5:
        flag = boardSize + 1


    if flag:
        f.seek(0)
        new_leader = [str(flag), text, str(score)]

        leaderboard.insert(flag - 1, new_leader)
        leaderboard[flag: ] = [[str(int(person[0]) + 1), person[1], person[2]] for person in leaderboard[flag: ] ]
        leaderboard = leaderboard[:-1] if len(leaderboard) == 6 else leaderboard

        writer = csv.writer(f)
        writer.writerows(leaderboard)

def exitGameMenu():
    """
    Displays the exit view
    """
    global sound, leaderboard, score, close_btn_surface, play_btn_surface, restart_btn_surface, lvl_animate, level
    input_box = pygame.Rect((WIN_WIDTH - 140)// 2, 5 * WIN_HEIGHT // 9, 140, 32)

    name_entry_txt = "Enter your nickname"
    nameEntry = mediumFont.render(name_entry_txt, True, BLACK)
    nameEntryRect = nameEntry.get_rect()
    nameEntryRect.center = ((WIN_WIDTH / 2), 400)

    color_inactive = pygame.Color(GRAY)
    color_active = pygame.Color(WHITE)
    color = color_inactive
    active = False
    text = ''
    accepted = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exitGame()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_box.collidepoint(event.pos):
                    active = not active
                else:
                    active = False
                if(close_btn_box_exit.collidepoint(pygame.mouse.get_pos())):
                    exitGame()

                if(restart_btn_box_exit.collidepoint(pygame.mouse.get_pos())):
                    level = 0
                    lvl_animate = 1
                    return True

                color = color_active if active else color_inactive

                if sound == True:
                    if(sound_on_box.collidepoint(pygame.mouse.get_pos())):
                        sound = False
                        pygame.mixer.music.pause()
                else:
                    if(sound_off_box.collidepoint(pygame.mouse.get_pos())):
                        sound = True
                        pygame.mixer.music.unpause()
       
            if event.type == pygame.KEYDOWN:
                # input the name
                if active and not accepted:
                    if event.key == pygame.K_RETURN and len(text) > 0:
                        # update leaderboard
                        updateLeaderboard(text)
                        text = ''
                        accepted = True
                    # backspace
                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                        # max name length = 12
                    elif len(text) < 12:
                        text += event.unicode
         # Display bg surface
        screen.blit(bg_surface,(0, 0))

        # display leaderboard
        displayLeaderboard()

        # draw name input box
        if not accepted:
            pygame.draw.rect(screen, color, input_box, 0)
            screen.blit(nameEntry, nameEntryRect)
            txt_surface = font.render(text, True, BLACK)
            screen.blit(txt_surface, (input_box.x + 5, input_box.y + 5))

        # Display sound button
        if sound == True:
            screen.blit(sound_on_surface,sound_on_box)
        else:
            screen.blit(sound_off_surface,sound_off_box)

        # close button
        close_btn_surface_exit = pygame.transform.scale(close_btn_surface, (100,100))
        close_btn_box_exit = close_btn_surface_exit.get_rect(center = ((WIN_WIDTH/2 + 120,3 * WIN_HEIGHT // 4)))

        # restart button
        restart_btn_surface_exit = pygame.transform.scale(restart_btn_surface, (100,100))
        restart_btn_box_exit = restart_btn_surface_exit.get_rect(center = ((WIN_WIDTH/2 - 120, 3 * WIN_HEIGHT // 4)))

        screen.blit(restart_btn_surface_exit, restart_btn_box_exit)
        screen.blit(close_btn_surface_exit, close_btn_box_exit)

        # Update display
        pygame.display.update()
        clock.tick(FPS)

# Initiate the game
pygame.init()
WIN_HEIGHT = (pygame.display.Info().current_h * 9) // 10
WIN_SIZE = (WIN_WIDTH,WIN_HEIGHT)

# game window caption
pygame.display.set_caption("LetterRain")

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
score_font = pygame.font.Font('assets/fonts/soupofjustice.ttf', 36)
game_over_font = pygame.font.Font('assets/fonts/soupofjustice.ttf', 50)
largeFont = pygame.font.Font('assets/fonts/AvenirMedium.ttf', 40)
mediumFont = pygame.font.Font('assets/fonts/AvenirMedium.ttf', 28)

# game variables
gravity = 2
game_active = False
words_formed = []
curr_word = ""
score = 0
total_score = 0
popped_letter = []

# Level Information
level = 0
TARGET_SCORE = [1,20,30,40,50]
LVL_TIMEOUT = 10
counter = 0
paused = False
sound = True
lvl_animate = 0
nxt_lvl_animate = 0
game_over_animate = 0

# Define FPS & SPAWN_TIME
FPS = 60
SPWN_TIME = 800

# Draw display surface
screen = pygame.display.set_mode(WIN_SIZE)

clock = pygame.time.Clock()

# Import blast surfaces
blast0_surface = pygame.image.load('assets/1_fireboll_1.png')
blast0_surface = pygame.transform.scale(blast0_surface, (IMG_WIDTH,IMG_HEIGHT))

blast1_surface = pygame.image.load('assets/1_fireboll_3.png')
blast1_surface = pygame.transform.scale(blast1_surface, (IMG_WIDTH,IMG_HEIGHT))

blast2_surface = pygame.image.load('assets/1_fireboll_3.png')
blast2_surface = pygame.transform.scale(blast2_surface, (IMG_WIDTH,IMG_HEIGHT))

# Import level surface
level_surface = pygame.image.load('assets/level.png').convert_alpha()
level_surface = pygame.transform.scale(level_surface, (175,80))

# Import level number surfaces
NUMBERS = list(map(str,[i for i in range(0,10)]))
NUMBERS = {char : pygame.image.load('assets/'+char+'.png').convert_alpha() for char in NUMBERS}
for number in NUMBERS.keys():
    NUMBERS[number] = pygame.transform.scale(NUMBERS[number],(int(1.5*NUMBERS[number].get_width()),int(1.5*NUMBERS[number].get_height())))

# Import level completed surface
lvl_completed_surface = pygame.image.load('assets/level_complete.png').convert_alpha()
lvl_completed_surface = pygame.transform.scale(lvl_completed_surface,(400,100))

# Import scorecard surface
bg_score_level = pygame.image.load('assets/bg_level.png').convert_alpha()
bg_score_level = pygame.transform.scale(bg_score_level,(int(0.3 * bg_score_level.get_width()),int(0.3 * bg_score_level.get_height()) + 10))

# Import table for scroecard surface
bg_score_table = pygame.image.load('assets/table2.png').convert_alpha()
bg_score_table = pygame.transform.scale(bg_score_table, ((int(0.3 * bg_score_table.get_width()),int(0.3 * bg_score_table.get_height()))))

# Import win surface for scorecard
win_level_surface = pygame.image.load('assets/win_level.png').convert_alpha()
win_level_surface = pygame.transform.scale(win_level_surface, ((int(0.4 * win_level_surface.get_width()),int(0.4 * win_level_surface.get_height()))))

# Import no star
no_star_surface = pygame.image.load('assets/star_4.png').convert_alpha()
no_star_surface = pygame.transform.scale(no_star_surface, (250,100))

# Import one star
one_star_surface = pygame.image.load('assets/star_1.png').convert_alpha()
one_star_surface = pygame.transform.scale(one_star_surface, (250,100))

# Import two star
two_star_surface = pygame.image.load('assets/star_2.png').convert_alpha()
two_star_surface = pygame.transform.scale(two_star_surface, (250,100))

# Import three star
three_star_surface = pygame.image.load('assets/star_3.png').convert_alpha()
three_star_surface = pygame.transform.scale(three_star_surface, (250,100))

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
paused_txt_box = paused_txt_surface.get_rect(center = ((WIN_WIDTH/2,WIN_HEIGHT/2 - 100)))

# Import pause button
pause_btn_surface = pygame.image.load('assets/pause.png').convert_alpha()
pause_btn_surface = pygame.transform.scale(pause_btn_surface,(50,50))
pause_btn_box = pause_btn_surface.get_rect(center = ((WIN_WIDTH - 90,WIN_HEIGHT - 30)))

# Import play button
play_btn_surface = pygame.image.load('assets/play.png').convert_alpha()
play_btn_surface = pygame.transform.scale(play_btn_surface,(100,100))
play_btn_box = play_btn_surface.get_rect(center = ((WIN_WIDTH/2 - 120,WIN_HEIGHT/2 + 20)))

# Import close button
close_btn_surface = pygame.image.load('assets/close.png').convert_alpha()
close_btn_surface = pygame.transform.scale(close_btn_surface, (100,100))
close_btn_box = close_btn_surface.get_rect(center = ((WIN_WIDTH/2 + 120,WIN_HEIGHT/2 + 20)))

# Import restart button
restart_btn_surface = pygame.image.load('assets/restart.png').convert_alpha()
restart_btn_surface = pygame.transform.scale(restart_btn_surface, (100,100))
restart_btn_box = restart_btn_surface.get_rect(center = ((WIN_WIDTH/2,WIN_HEIGHT/2 + 20)))

# Import next btn
nxt_btn_surface = pygame.image.load('assets/next.png').convert_alpha()
nxt_btn_surface = pygame.transform.scale(nxt_btn_surface, (75,75))
nxt_btn_box = nxt_btn_surface.get_rect(center = ((WIN_WIDTH/2 + 10,WIN_HEIGHT/2 + 200)))

# Import close btn for level score
close_btn_surface_1 = pygame.image.load('assets/close.png').convert_alpha()
close_btn_surface_1 = pygame.transform.scale(close_btn_surface_1, (75,75))
close_btn_box_1 = close_btn_surface_1.get_rect(center = ((WIN_WIDTH/2 + 120,WIN_HEIGHT/2 + 200)))

# Import restart button for level score
restart_btn_surface_1 = pygame.image.load('assets/restart.png').convert_alpha()
restart_btn_surface_1 = pygame.transform.scale(restart_btn_surface_1, (75,75))
restart_btn_box_1 = restart_btn_surface_1.get_rect(center = ((WIN_WIDTH/2 - 100,WIN_HEIGHT/2 + 200)))

# Import sound on and off button
sound_on_surface = pygame.image.load('assets/sound.png').convert_alpha()
sound_on_surface = pygame.transform.scale(sound_on_surface, (50,50))
sound_on_box = sound_on_surface.get_rect(center = ((WIN_WIDTH - 30,WIN_HEIGHT - 30)))

sound_off_surface = pygame.image.load('assets/sound_off.png').convert_alpha()
sound_off_surface = pygame.transform.scale(sound_off_surface, (50,50))
sound_off_box = sound_off_surface.get_rect(center = ((WIN_WIDTH - 30,WIN_HEIGHT - 30)))

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
            exitGameMenu()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active == False:
                # Start the game
                level = 0
                lvl_animate += 1
                
            if event.key in ascii_letters and game_active == True:
                indx = checkCollision(event.key, letters, generated_letters)
                if indx >= 0:
                    # Remove those letters from list and add to word
                    curr_word = curr_word + generated_letters[indx]
                    generated_letters.pop(indx)
                    # append to list to blast class
                    blast = Blast(letters.pop(indx), 0)
                    popped_letter.append(blast)
                    # letters.pop(indx)

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

            if(close_btn_box.collidepoint(pygame.mouse.get_pos())):
                evaluateWord()
                exitGameMenu()

            if(restart_btn_box.collidepoint(pygame.mouse.get_pos())):
                lvl_animate += 1

            if(close_btn_box_1.collidepoint(pygame.mouse.get_pos())):
                exitGameMenu()

            if(restart_btn_box_1.collidepoint(pygame.mouse.get_pos())):
                score = 0
                nxt_lvl_animate = 0
                lvl_animate += 1

            if(nxt_btn_box.collidepoint(pygame.mouse.get_pos())):
                nxt_lvl_animate = 0
                level += 1
                score = 0
                lvl_animate += 1

            if sound == True:
                if(sound_on_box.collidepoint(pygame.mouse.get_pos())):
                    sound = False
                    pygame.mixer.music.pause()
            else:
                if(sound_off_box.collidepoint(pygame.mouse.get_pos())):
                    sound = True
                    pygame.mixer.music.unpause()

        # For every second update counter
        if event.type == TIMER:
            
            if game_active == True:
                counter -= 1

            if lvl_animate > 0:
                lvl_animate += 1

            if nxt_lvl_animate > 0:
                nxt_lvl_animate += 1

            if game_over_animate > 0:
                game_over_animate += 1

    # When game is active
    if game_active == True:

        # Check for TIMEOUT
        if counter == 0:
            if score >= TARGET_SCORE[level]:
                print("Congrats. Passed to next level")
                game_active = False
                nxt_lvl_animate += 1
                counter = LVL_TIMEOUT
            else:
                print("Game Over")
                evaluateWord()
                game_active = False
                game_over_animate += 1

        # Display bg surface
        screen.blit(bg_surface,(0, 0))
        
        # Display headline
        displayHeader(score,counter)        

        # Display the catching region
        screen.blit(catch_surface, catch_box)

        # Move the letters
        letters = moveLetters(letters)
        drawLetters(letters,generated_letters)

        # Check if blast list is non-empty
        i = 0
        while i < len(popped_letter): 
            letter = popped_letter[i]
            if letter.state < 10:
                    screen.blit(blast0_surface,(letter.letter_surface[0],letter.letter_surface[1]))
            elif letter.state < 20:
                screen.blit(blast1_surface,(letter.letter_surface[0],letter.letter_surface[1]))
            elif letter.state < 30:
                screen.blit(blast2_surface,(letter.letter_surface[0],letter.letter_surface[1]))
            else:
                popped_letter.pop(i)
                i -= 1
            letter.state += 1
            i += 1              

        # Display word formed so far
        wordFormed(curr_word)

        # Display pasue button
        screen.blit(pause_btn_surface, pause_btn_box)

        # Display sound button
        if sound == True:
            screen.blit(sound_on_surface,sound_on_box)
        else:
            screen.blit(sound_off_surface,sound_off_box)

    if paused == True:
        displayPauseScreen()

    # Check if lvl_animate is active
    if lvl_animate > 0:
        startLevel()

    # Check if nxt_lvl_animate is active
    if nxt_lvl_animate > 0:
        nextLevel()

    # Check if game_over_animate is active
    if game_over_animate > 0:
        gameOver()
  
    # Update display 
    pygame.display.update()
    clock.tick(FPS)
