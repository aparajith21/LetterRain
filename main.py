import GenerateLetters
import WordScore
import pygame
from random import choices
from random import uniform
from math import exp


IMG_WIDTH = 64
IMG_HEIGHT = 64


def redrawGameWindow(win, x, y, letters, LETTERS):

    j = 0
    width, height = pygame.display.get_surface().get_size()
    for j in range(len(letters)):
        n = len(letters[j])
        level = letters[j]
        xlevel = x[j]
        if y[j] < height:
            for i in range(n):
                try:
                    win.blit(LETTERS[level[i].upper()], (xlevel[i], y[j]))
                except:
                    err = 1
    pygame.display.update()

def main():

    pygame.init()
    win = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    WIDTH, HEIGHT = pygame.display.get_surface().get_size()
    pygame.display.set_caption("LetterRain")



    LETTERS = list(map(chr, range(65, 91)))
    LETTERS = {char : pygame.image.load('Letters/' + char + '.jpg') for char in LETTERS}

    letter_knt_weights = [1/(1 + exp(i)) for i in range(15)]
    letter_knt_population = [i for i in range(1, 16)]

    letters = []


    run = True
    x = []
    y = []
    levels = 0
    fake_levels = 0
    words_formed = []
    word = ""
    score = 0

    while run:
        pygame.time.delay(10)
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                run = False

        for event in events:
            if event.type == pygame.KEYDOWN:
                for i in range(97, 123):
                    if event.key == i:
                        for j in range(len(letters)):
                            if y[j] < HEIGHT:
                                if chr(i).upper() in letters[j]:
#                                    letters[j].remove(chr(i).upper())
                                    letters[j] = list(''.join(letters[j]).replace(chr(i).upper(), ' ', 1))
                                    word += chr(i).upper()
                                    break
                if event.key == pygame.K_RETURN:
                    words_formed.append(word)
                    score += WordScore.WordScore(word)
                    word = ""

        win.fill((0, 0, 0))
        fake_levels += 1

        if(fake_levels % 100 == 0):
            levels += 1
            letter_knt = choices(population = letter_knt_population, weights = letter_knt_weights)[0]
            letters.append(GenerateLetters.GenerateLetters(letter_knt))
            y.append(0)

            x_level = []

            for i in range(letter_knt):
                x_level.append(int(uniform((WIDTH / letter_knt) * i, (WIDTH / letter_knt) * (i + 1) - IMG_WIDTH)))

            x.append(x_level)


        for i in range(levels):
            y[i] += (IMG_HEIGHT + uniform(5, 20))/100




        redrawGameWindow(win, x, y, letters, LETTERS)



    pygame.quit()
    print("Words input: ", words_formed)
    print("Score: ", score)




if __name__ == "__main__":
    main()

