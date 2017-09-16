text = open("ciphertext.txt", "r").read()
text = "WHENTHECLOCKSTRIKESTWELVEATTACK"
english_frequency = {
    "A": 0.08167,
    "B": 0.01492,
    "C": 0.02782,
    "D": 0.04253,
    "E": 0.12702,
    "F": 0.02228,
    "G": 0.02015,
    "H": 0.06094,
    "I": 0.06966,
    "J": 0.00153,
    "K": 0.00772,
    "L": 0.04025,
    "M": 0.02406,
    "N": 0.06749,
    "O": 0.07507,
    "P": 0.01929,
    "Q": 0.00095,
    "R": 0.05987,
    "S": 0.06327,
    "T": 0.09056,
    "U": 0.02758,
    "V": 0.00978,
    "W": 0.0236,
    "X": 0.0015,
    "Y": 0.01974,
    "Z": 0.0007}
textCount = {}
for letterIndex in range(65, 90):
    textCount[chr(letterIndex)] = 0
for letter in text:
    textCount[letter] += 1
chiSquared = 0
for letterIndex in range(65, 90):
    expectedCount = english_frequency[chr(letterIndex)] * len(text)
    chiSquared += ((textCount[chr(letterIndex)]-expectedCount)**2)/expectedCount
print(chiSquared)
#English <= 150
