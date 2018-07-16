# coding=utf-8
from __future__ import division
from collections import defaultdict
from math import log


def train(samples):
    classes, freq = defaultdict(lambda: 0), defaultdict(lambda: 0)
    for feats, label in samples:
        classes[label] += 1  # count classes frequencies
        for feat in feats:
            freq[label, feat] += 1  # count features frequencies

    for label, feat in freq:  # normalize features frequencies
        freq[label, feat] /= classes[label]

    for c in classes:  # normalize classes frequencies
        classes[c] /= len(samples)

    return classes, freq  # return P(C) and P(O|C)


def classify(classifier, feats):
    classes, prob = classifier
    ind = 1
    print classes.keys()[ind], prob.get((classes.keys()[ind], u'к'))

    for gender in classes.keys():
        val = -log(classes[gender])
        print gender, 'start val is', val
        for feat in feats:
            val += -log(prob.get((gender, feat)))
        print gender, val

    return min(classes.keys(),  # calculate argmin(-log(C|O))
               key=lambda cl: -log(classes[cl]) + \
                              sum(-log(prob.get((cl, feat))) for feat in feats))


def get_features(sample): return sample[-1],  # get last letter


samples = (line.decode('utf-8').split() for line in open('names.txt'))
features = [(get_features(feat), label) for feat, label in samples]
classifier = train(features)

name = u'Олеся'
print classify(classifier, get_features(name))
