"""
TEAMBOMBA 2017 - Proprietary Program
Simple monoalphabetic substitution cracker
"""
"""
Key is dictionary which maps each letter in the alphabet to another letter in the
alphabet

Creates a random initial key

Then, usesa hill climbing algorithm to work out the final key. ---> Changes 2
letters in the key per iteration and scores it with quagram analysis, if it is
better than the previous, it is replaced.

If there is no improvment in ~1000 iterations, the key is re-shuffled to prevent
getting stuck at a local maxima, if the best key has not changed in over 10
reshuffles, the best key is presumed to have been found.
Look at wikipedia for info:
https://en.wikipedia.org/wiki/Simulated_annealing
"""

ciphertext = "SOWFBRKAWFCZFSBSCSBQITBKOWLBFXTBKOWLSOXSOXFZWWIBICFWUQLRXINOCIJLWJFQUNWXLFBSZXFBTXAANTQIFBFSFQUFCZFSBSCSBIMWHWLNKAXBISWGSTOXLXTSWLUQLXJBUUWLWISTBKOWLSWGSTOXLXTSWLBSJBUUWLFULQRTXWFXLTBKOWLBISOXSSOWTBKOWLXAKOXZWSBFIQSFBRKANSOWXAKOXZWSFOBUSWJBSBFTQRKAWSWANECRZAWJ".upper().replace(" ", "").replace("\n", "")
#No punctuation pls

"""
Define and create quadgram fitness object for scoring text
"""
from math import log10
class quadgram_score(object):
    def __init__(self,ngramfile):
        self.quadgrams = {}
        with open(ngramfile) as f:
            content = f.readlines()

        for line in content:
            key,count = line.split(" ")
            self.quadgrams[key] = int(count)

        self.N = sum(int(count) for key,count in self.quadgrams.items())

    def score(self,text):
        text = text.upper()
        text_quadgrams = []
        for index in range(0, len(text)-3):
            text_quadgrams.append(text[index:index+4])

        quadgrams = self.quadgrams.__getitem__
        fitness = 0
        for quadgram in text_quadgrams:
            if quadgram in self.quadgrams:
                fitness += log10(self.quadgrams[quadgram]/self.N)
            else:
                fitness += log10(0.01/self.N)
        return fitness

fitness = quadgram_score("quadgrams")

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
initial_key = ["ABCDEFGHIJKLMNOPQRSTUVWXYZ", "ABCDEFGHIJKLMNOPQRSTUVWXYZ"]

#Shuffle key to generate initial key
initial_key[1] = list(initial_key[1])
random.shuffle(initial_key[1])
initial_key[1] = "".join(initial_key[1])

best_key = list(initial_key)
best_score = fitness.score(decrypt(ciphertext, best_key))

best_best_key = list(best_key)
best_best_score = fitness.score(decrypt(ciphertext, best_best_key))

i = 0
last_changed = 0
while True:
    i += 1
    if i % 1000 == 0:
        if initial_key == best_key:
            if last_changed < 10:
                if best_score > best_best_score:
                    best_best_key = list(best_key)
                    best_best_score = best_score
                    last_changed = 0
                else:
                    last_changed += 1
                best_key[1] = list(best_key[1])
                random.shuffle(best_key[1])
                best_key[1] = "".join(best_key[1])
                best_score = fitness.score(decrypt(ciphertext, best_key))
            else:
                break
        else:
            initial_key = list(best_key)
    key = list(best_key)
    key[1] = swap_letters(key[1])
    score = fitness.score(decrypt(ciphertext, key))
    if score > best_score:
        best_key = list(key)
        best_score = score

print("Key:", best_best_key[0].lower())
print("    ", best_best_key[1])
print(decrypt(ciphertext, best_best_key).lower())
