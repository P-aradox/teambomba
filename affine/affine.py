"""
TEAMBOMBA 2017 - Proprietary Program
Affine cracker - version 1 - Brute Force
"""

ciphertext = "QUVNLAUVILZKVZZZVNHIVQUFSFZHWZQLQHQLJSNLAUVIFZLQLZYHKSVIFWKVQJFKKJMQUVFQQFNTZQUFQPJITFDFLSZQZHWZQLQHQLJSNLAUVIZLSFEELQLJSQJJQUVIFQQFNTZ".upper().replace(" ", "").replace("\n", "")

"""
Create quadgram_score object (for measuring fitness/english-likeness)
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
Define multiplicative inverse finder
ax = 1 (mod m)
"""
def multiplicative_inverse(a):
    for x in range(26):
        if (a*x) % 26 == 1:
            return x

"""
Define affine decryption function
p = a-1(c-b) % 26
where a-1 is the multiplicative inverse of a
"""
def decrypt(a, b, ciphertext):
    plaintext = ""
    for c in ciphertext:
        c = ord(c) - 65
        p = multiplicative_inverse(a)*(c - b) % 26
        if chr(p + 65) not in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
            print("\n\nERROR  \n\n")
        plaintext += str(chr(p + 65))
    return plaintext

"""
"""
a_values = [1,3,5,7,9,11,15,17,19,21,23,25] #All possible values of a
b_values = [b for b in range(0, 26)] #b can range from 0-25

best_key = {"a":0, "b":0, "score":-99999}
score = 0
for a in a_values:
    for b in b_values:
        score = fitness.score(decrypt(a, b, ciphertext))
        if score > best_key["score"]:
            best_key["a"] = a
            best_key["b"] = b
            best_key["score"] = score

print("Key:", str(best_key["a"]) + "x+" + str(best_key["b"]) + " mod 26")
print(decrypt(best_key["a"], best_key["b"], ciphertext))
