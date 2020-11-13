import json
dictionary_path = "dictionary.json"
f = open(dictionary_path, )
dictionary = json.load(f)

def IsWord(word):
    return word in dictionary
