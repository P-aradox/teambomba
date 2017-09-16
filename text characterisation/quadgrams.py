"""
TEAM BOMBA 2017 - Proprietry program
Quadgrams text characterisation
"""
"""
The greater the fitness, the more english-like the text is
"""

ciphertext = "ATTACK THE EAST WALL OF THE CASTLE AT DAWN".upper().replace(" ", "").replace("\n", "")

"""
Extract each quadgram from ciphertext
e.g. ATTACK --> ATTA TTAC TACK
"""
ciphertext_quadgrams = []
for index in range(0, len(ciphertext)-3):
    ciphertext_quadgrams.append(ciphertext[index:index+4])

"""
Extract quadgrams count from quadgrams file
"""
quadgrams = {}
with open("quadgrams") as f:
    content = f.readlines()

for line in content:
    key,count = line.split(" ")
    quadgrams[key] = int(count)

N = sum(int(count) for key,count in quadgrams.items())
"""
Work out final log probability (aka fitness)
          count(ATTA)
p(ATTA) = -----------
              N
log(p(ATTACK)) = log(p(ATTA)) + log(p(TTAC)) + log(p(TACK))
"""
from math import log10

fitness = 0
for quadgram in ciphertext_quadgrams:
    if quadgram in quadgrams:
        fitness += log10(quadgrams[quadgram]/N)
    else:
        fitness += log10(0.01/N)

print(fitness)
