"""
TEAMBOMBA 2017 - Proprietary Program
Simple monoalphabetic substitution cracker v2 - Simulated annealing approach

CURRENTLY NOT WORKING

"""
"""
Key is dictionary which maps each letter in the alphabet to another letter in the
alphabet

Creates a random initial key then uses a simulated annealing algorithm to work out best key.
Look at wikipedia for info:
https://en.wikipedia.org/wiki/Simulated_annealing
"""

ciphertext = "SOWFBRKAWFCZFSBSCSBQITBKOWLBFXTBKOWLSOXSOXFZWWIBICFWUQLRXINOCIJLWJFQUNWXLFBSZXFBTXAANTQIFBFSFQUFCZFSBSCSBIMWHWLNKAXBISWGSTOXLXTSWLUQLXJBUUWLWISTBKOWLSWGSTOXLXTSWLBSJBUUWLFULQRTXWFXLTBKOWLBISOXSSOWTBKOWLXAKOXZWSBFIQSFBRKANSOWXAKOXZWSFOBUSWJBSBFTQRKAWSWANECRZAWJ".upper().replace(" ", "").replace("\n", "")[:40]
#No punctuation pls

"""
Define and create quadgram fitness object for scoring text
"""
from math import log10

class bigram_score(object):
    def __init__(self,ngramfile):
        self.bigrams = {}
        with open(ngramfile) as f:
            content = f.readlines()

        for line in content:
            key,count = line.split(" ")
            self.bigrams[key] = int(count)

        self.N = sum(int(count) for key,count in self.bigrams.items())

    def score(self,text):
        text_bigrams = []
        for index in range(0, len(text)-1):
            text_bigrams.append(text[index:index+2])

        bigrams = self.bigrams.__getitem__
        fitness = 0
        for bigram in text_bigrams:
            if bigram in self.bigrams:
                fitness += log10(self.bigrams[bigram]/self.N)
            else:
                fitness += log10(0.01/self.N)
        return fitness

fitness = bigram_score("bigrams")

"""
Define decrypt function (decrypts whole ciphertext given key)
"""
def decrypt(text, key):
    plaintext = ""
    for letter in text:
        for index, value in enumerate(key[1]):
            if value == letter:
                plaintext += key[0][index]
                break
    return plaintext

"""
Define function to swap to keys around
"""
import random
def swap_letters(key):
    key = list(key)

    index1 = random.randint(0, len(key)-1)
    index2 = random.randint(0, len(key)-1)

    key[index1], key[index2] = key[index2], key[index1]

    return "".join(key)

"""
Main code
"""
from random import randint
from math import exp

initial_key = ["ABCDEFGHIJKLMNOPQRSTUVWXYZ", "ABCDEFGHIJKLMNOPQRSTUVWXYZ"]

#Shuffle key to generate initial key
initial_key[1] = list(initial_key[1])
random.shuffle(initial_key[1])
initial_key[1] = "".join(initial_key[1])

best_key = list(initial_key)
best_score = fitness.score(decrypt(ciphertext, best_key))

max_key = list(best_key)
max_score = fitness.score(decrypt(ciphertext, max_key))

for n in range(1,6):
    print("Epoch", str(n) + ":", max_key, max_score)
    print(decrypt(ciphertext, max_key).lower())

    initial_key = ["ABCDEFGHIJKLMNOPQRSTUVWXYZ", "ABCDEFGHIJKLMNOPQRSTUVWXYZ"]
    initial_key[1] = list(initial_key[1])
    random.shuffle(initial_key[1])
    initial_key[1] = "".join(initial_key[1])

    best_key = list(initial_key)
    best_score = fitness.score(decrypt(ciphertext, best_key))

    T = 30
    while T > 0:
        for count in range(5000):
            key = list(best_key)
            key[1] = swap_letters(key[1])
            score = fitness.score(decrypt(ciphertext, key))
            fitness_diff = score - best_score
            if fitness_diff > 0:
                best_key = list(key)
                best_score = score
            elif exp(fitness_diff/T) > randint(0,1):
                best_key = list(key)
                best_score = score
        if best_score > max_score:
            max_key = list(best_key)
            max_score = best_score
            print(max_key, max_score)
        T -= 0.1


print("Key:", max_key[0].lower())
print("    ", max_key[1])
print(decrypt(ciphertext, max_key).lower())
