#coding = utf-8

import csv
from operator import itemgetter

BARRIER = 0.4
ALPHA = 0.01
SIZE = 40
FILE_NAME = "train-filtered-CatAllDim-sample10000.csv"
MAX_ITER = 50

def dot_product(v1, v2):
    return sum(v1i * v2i for v1i, v2i in zip(v1, v2))

def dot_product2(v1,v2):
    return v1[0]*v2[0] + v1[1]*v2[1]

def norm(v):
    aux = 0
    for e in v:
        aux += e**2
    return aux ** 0.5


class Perceptron(object):
    ''' Implementation of a Perceptron algorithm '''
    def __init__(self, category):
        self.category = category
        self.weights = [0] * SIZE
        self.iterations = 0

    def train(self, crimes_file):
        while True:
            was_perfect = True
            with open(crimes_file) as training_file:
                traning_set = csv.DictReader(training_file)
                for crime in traning_set:
                    desired_output = crime["Category"] == self.category
                    result = dot_product(self.weights, [float(x) for x in crime.values()[1:]])
                    n_r = result - BARRIER
                    if n_r < 0:
                        was_perfect = False
                        for index, value in enumerate(crime.values()[1:]):
                            self.weights[index] += ALPHA * abs(n_r)
                        norma = norm(self.weights)
                        for i in range(len(self.weights)):
                            self.weights[i] = self.weights[i]/norma
                self.iterations += 1
            if was_perfect or MAX_ITER == self.iterations:
                break

    def define_value(self, crime):
        return dot_product2(self.weights, crime)

def get_categories(crimes_file):
    ret_value = set()
    with open(crimes_file) as training_file:
        traning_set = csv.DictReader(training_file)
        for crime in traning_set:
            ret_value.add(crime["Category"])
    return list(ret_value)

def main():
    categories = get_categories(FILE_NAME)
    perceptrons = []
    n = 1
    for category in categories:
        print "Initiating training of {}. {} categories to go".format(category, len(categories)-n)
        perceptron = Perceptron(category)
        perceptron.train(FILE_NAME)
        perceptrons.append(perceptron)
        n += 1
    with open(FILE_NAME) as test_file:
        test_set = csv.DictReader(test_file)
        coincidences = 0
        n = 0
        for crime in test_set:
            results = {}
            for p in perceptrons:
                results[p.category] = p.define_value((float(crime["X"]), float(crime["Y"])))
            if max(results.items(), key=itemgetter(1))[0] == crime["Category"]:
                coincidences += 1
            n += 1
            print coincidences, "/", n
    print float(coincidences) / n * 100, "%"

main()


