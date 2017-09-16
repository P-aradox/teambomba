"""
TEAM BOMBA 2017 - Proprietry program
Bigrams text characterisation
"""
"""
The greater the fitness, the more english-like the text is
"""

ciphertext = "ATTACK THE EAST WALL OF THE CASTLE AT DAWN".upper().replace(" ", "").replace("\n", "")

"""
Extract each bigram from ciphertext
e.g. ATTACK --> ATTA TTAC TACK
"""
ciphertext_bigrams = []
for index in range(0, len(ciphertext)-1):
    ciphertext_bigrams.append(ciphertext[index:index+2])
print(ciphertext_bigrams)

"""
Extract bigram count from bigrams file
"""
bigrams = {}
with open("bigrams") as f:
    content = f.readlines()

for line in content:
    key,count = line.split(" ")
    bigrams[key] = int(count)

N = sum(int(count) for key,count in bigrams.items())
"""
Work out final log probability (aka fitness)
          count(AT)
p(AT) = -----------
              N
log(p(ATTACK)) = log(p(AT)) + log(p(TT)) + log(p(TA))... + log(p(CK))
"""
from math import log10

fitness = 0
for bigram in ciphertext_bigrams:
    if bigram in bigrams:
        fitness += log10(bigrams[bigram]/N)
    else:
        fitness += log10(0.01/N)

print(fitness)
