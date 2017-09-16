"""
TEAMBOMBA 2017 - Proprietary Program
Vigenere decrypter
"""
"""
Decrypts a vigenere ciphertext when given ciphertext and key
"""
key = "CIPHERS".upper()
ciphertext = """vptnvffuntshtarptymjwzirappljmhhqvsubwlzzygvtyitarptyiougxiuydtgzhhvvmum
shwkzgstfmekvmpkswdgbilvjljmglmjfqwioiivknulvvfemioiemojtywdsajtwmtcgluy
sdsumfbieugmvalvxkjduetukatymvkqzhvqvgvptytjwwldyeevquhlulwpkt""".upper().replace(" ", "")
#NO PUNCTUATION

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
