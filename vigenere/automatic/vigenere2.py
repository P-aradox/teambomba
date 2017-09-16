"""
TEAMBOMBA 2017 - Proprietary Program
Vigenere automatic cracker - Version 2
"""
"""
More reliable than vigenere1.py
Uses local random search
"""

ciphertext = """Klkbnqlcytfysryucocphgbdizzfcmjwkuchzyeswfogmmetwwossdchrzyldsbwnydednzwnefydthtddbojice
mlucdygicczhoadrzcylwadsxpilpiecskomoltejtkmqqymehpmmjxyolwpeewjckznpccpsvsxauyodhalmrioc
wpelwbcniyfxmwjcemcyrazdqlsomdbfljwnbijxpddsyoehxpceswtoxwbleecsaxcnuetzywfn""".upper().replace(" ", "").replace("\n", "")
#No punctuation

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
Define Vigenere decrypter function
"""
def decipher_caesar(text, shift):
    plaintext = ""
    shift = ord(shift)-65
    for letter in text:
        letter_code = ord(letter)
        code_shift = letter_code - shift
        if code_shift > ord("Z"):
            code_shift -= 26
        elif code_shift < ord("A"):
            code_shift += 26
        plaintext += chr(code_shift)
    return plaintext

def decrypt(text, key):
    plaintext = ""
    text_offsets = []
    for offset in range(0, len(key)):
        text_offsets.append(decipher_caesar(text[offset::len(key)], key[offset]))
    for index in range(0, len(text_offsets[0])):
        for offset in range(0, len(key)):
            try:
                plaintext += text_offsets[offset][index]
            except IndexError:
                pass
    return plaintext

"""
Crack cipher
"""
best_keys = []

for key_length in range(2, 25):
    if key_length > len(ciphertext)/2:
        break
    best_key = ""
    for n in range(key_length):
        best_key += "A"
    best_score = -99999

    key_changed = True
    while key_changed:
        start_key = best_key
        for index, value in enumerate(best_key):
            current_key = best_key
            for letter in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
                current_key = list(current_key)
                current_key[index] = letter
                current_key = "".join(current_key)
                score = fitness.score(decrypt(ciphertext, current_key))
                if score > best_score:
                    best_key = current_key
                    best_score = score
        end_key = best_key
        if start_key == end_key:
            key_changed = False

    best_keys.append(best_key)

best_key = ""
best_score = -99999
for key in best_keys:
    score = fitness.score(decrypt(ciphertext, key))
    if score > best_score:
        best_key = key
        best_score = score
print("Key:", best_key, "\n"+ decrypt(ciphertext, best_key))
