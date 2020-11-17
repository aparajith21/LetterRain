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
                win.blit(LETTERS[level[i].upper()], (xlevel[i], y[j]))
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

    while run:
        pygame.time.delay(10)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
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




if __name__ == "__main__":
    main()

