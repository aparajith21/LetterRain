import GenerateLetters
import WordScore
def main():
    n = 5
    for i in range(10):
        letters = GenerateLetters.GenerateLetters(n)
        print(letters)
    print(WordScore.WordScore("hello"))



if __name__ == "__main__":
    main()

