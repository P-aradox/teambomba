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
