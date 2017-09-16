"""
TEAMBOMBA 2017 - Proprietary Program
Vigenere automatic cracker - version 1
"""
"""
Fairly reliable for long texts but has a margin of error with shorter texts.
"""

ciphertext = """Klkbnqlcytfysryucocphgbdizzfcmjwkuchzyeswfogmmetwwossdchrzyldsbwnydednzwnefydthtddbojice
mlucdygicczhoadrzcylwadsxpilpiecskomoltejtkmqqymehpmmjxyolwpeewjckznpccpsvsxauyodhalmrioc
wpelwbcniyfxmwjcemcyrazdqlsomdbfljwnbijxpddsyoehxpceswtoxwbleecsaxcnuetzywfn""".upper().replace(" ", "").replace("\n", "")
#No punctuation

"""
Setup graphing library (nothing important)
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

"""
Define function to find index of coincidence:
i=Z   f_i(f_i−1)
 ∑   -------------
i=A    N(N−1)
where f_i is the frequency of the letter i
and N is the length of the ciphertext.

Function presumes input text is capitalized (A,B,C,..Z)
"""
def ioc(text):
    totalSum = 0
    for chrIndex in range(65, 90):
        count = 0
        letter = chr(chrIndex)
        for c in text:
            if c == letter:
                count += 1
        totalSum += count * (count - 1)
    return (totalSum / (len(text) * (len(text) - 1)))

"""
Work out the average index of coincidence of each key length and add it to a dictionary in the form
keylength: average index of coincidence
    More info @ http://practicalcryptography.com/cryptanalysis/stochastic-searching/cryptanalysis-vigenere-cipher/
"""
ioc_values = {}
for key_length in range(1, 11):
    average = 0
    for offset in range(0, key_length):
        average += ioc(ciphertext[offset::key_length])
    average /= key_length
    ioc_values[key_length] = average

"""
Plot graph and save it to keylength.png
"""
x_axis = []
y_axis = []
for key, value in ioc_values.items():
    x_axis.append(key)
    y_axis.append(value)
plt.xlabel('Key Length')
plt.ylabel('Index of Coincidence')
plt.plot(x_axis, y_axis, "ro")
plt.savefig('keylength.png')

"""
Work out best key length
"""
best_keylength = {"key_length":0, "ioc":0}
for key_length, ioc in ioc_values.items():
    if ioc > best_keylength["ioc"]:
        best_keylength["key_length"] = key_length
        best_keylength["ioc"] = ioc
key_length = best_keylength["key_length"]

print("Key length:", key_length)

"""
Define function to work out Chi-Squared Statistic
"""
def chiSquared(text):
    english_frequency = {"A": 0.08167,"B": 0.01492,"C": 0.02782,"D": 0.04253,"E": 0.12702,
"F": 0.02228,"G": 0.02015,"H": 0.06094,"I": 0.06966,"J": 0.00153,"K": 0.00772,"L": 0.04025,
"M": 0.02406,"N": 0.06749,"O": 0.07507,"P": 0.01929,"Q": 0.00095,"R": 0.05987,"S": 0.06327,
"T": 0.09056,"U": 0.02758,"V": 0.00978,"W": 0.0236,"X": 0.0015,"Y": 0.01974,"Z": 0.0007}
    textCount = {}
    for letterIndex in range(65, 91):
        textCount[chr(letterIndex)] = 0
    for letter in text:
        textCount[letter] += 1
    chiSquared = 0
    for letterIndex in range(65, 91):
        expectedCount = english_frequency[chr(letterIndex)] * len(text)
        chiSquared += ((textCount[chr(letterIndex)]-expectedCount)**2)/expectedCount
    return chiSquared

"""
Define function to work out the best caesar shift
(recycled from the caesar shift solver)
"""
def crack_caesar(text):
    best_decryption = {
        "text": "",
        "score": 999,
        "shift_value": 0,
        "shift_letter": ""
    }
    for shift in range(0,26):
        plaintext = ""
        for letter in text:
            letter_code = ord(letter)
            code_shift = letter_code - shift
            if code_shift > ord("Z"):
                code_shift -= 26
            elif code_shift < ord("A"):
                code_shift += 26
            plaintext += chr(code_shift)
        score = chiSquared(plaintext)
        if score < best_decryption["score"]:
            best_decryption["text"] = plaintext
            best_decryption["score"] = score
            best_decryption["shift_value"] = shift
            best_decryption["shift_letter"] = str(chr(shift+65))
    return best_decryption

"""
Crack key
"""
key = ""
for offset in range(0, key_length):
    key += crack_caesar(ciphertext[offset::key_length])["shift_letter"]
print("Key:", key)

"""
Define caesar decipher function
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

"""
Deciphers every nth letter in cipher text then re-assembles into plaintext
"""
plaintext = ""
text_offsets = []
for offset in range(0, len(key)):
    text_offsets.append(decipher_caesar(ciphertext[offset::len(key)], key[offset]))
for index in range(0, len(text_offsets[0])):
    for offset in range(0, len(key)):
        try:
            plaintext += text_offsets[offset][index]
        except IndexError:
            pass

print(plaintext)
