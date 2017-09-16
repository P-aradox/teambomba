"""
TEAMBOMBA 2017 - Proprietary Program
Vigenere key cracker
"""
"""
Finds the most probable key for a vigenere cipher when given the ciphertext and key length
May have inconsistencies with smaller length texts, you may be able to work out errors:
    e.g. if program outputs the key as "CIAHERS", you can presume the correct key is "CIPHERS"

To find the key all you need to do is crack n different caesar ciphers (where n is the key length)
"""

key_length = 7
ciphertext = """vptnvffuntshtarptymjwzirappljmhhqvsubwlzzygvtyitarptyiougxiuydtgzhhvvmum
shwkzgstfmekvmpkswdgbilvjljmglmjfqwioiivknulvvfemioiemojtywdsajtwmtcgluy
sdsumfbieugmvalvxkjduetukatymvkqzhvqvgvptytjwwldyeevquhlulwpkt""".upper().replace(" ", "").replace("\n", "")
#NO PUNCTUATION

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
print(key)
