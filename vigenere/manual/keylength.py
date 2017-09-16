"""
TEAMBOMBA 2017 - Proprietary Program
Vigenere key length cracker
"""
"""
Creates a graph of the index of coincidence for certain key lengths
Probable key length is indicated by a high index of coincidence on the graph (outliers)s
"""

ciphertext = """vptnvffuntshtarptymjwzirappljmhhqvsubwlzzygvtyitarptyiougxiuydtgzhhvvmum
shwkzgstfmekvmpkswdgbilvjljmglmjfqwioiivknulvvfemioiemojtywdsajtwmtcgluy
sdsumfbieugmvalvxkjduetukatymvkqzhvqvgvptytjwwldyeevquhlulwpkt""".upper().replace(" ", "").replace("\n", "")
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
