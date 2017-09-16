from math import log10

class bigram_score(object):
    def __init__(self,ngramfile):
        self.bigrams = {}
        with open(ngramfile) as f:
            content = f.readlines()

        for line in content:
            key,count = line.split(" ")
            self.bigrams[key] = int(count)

        self.N = sum(int(count) for key,count in self.bigrams.items())

    def score(self,text):
        text_bigrams = []
        for index in range(0, len(text)-1):
            text_bigrams.append(text[index:index+2])

        bigrams = self.bigrams.__getitem__
        fitness = 0
        for bigram in text_bigrams:
            if bigram in self.bigrams:
                fitness += log10(self.bigrams[bigram]/self.N)
            else:
                fitness += log10(0.01/self.N)
        return fitness
