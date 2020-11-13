import GenerateLetters
import IsWord
def main():
    n = 5
    for i in range(10):
        letters = GenerateLetters.GenerateLetters(n)
        print(letters)
    print(IsWord.IsWord("hello"))



if __name__ == "__main__":
    main()

