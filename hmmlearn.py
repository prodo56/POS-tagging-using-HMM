import collections
import sys
import pickle
import json
import time

#text = sys.argv[1]
text="catalan_corpus_train_tagged.txt"
with open(text, 'r') as f:
    data = f.readlines()
tags=[]
emissionMatrix={}
tagData={}
count=0
start=time.clock()
print start
#transitionMatrix = [[1 for x in xrange(len(tagDictionary))] for x in xrange(len(tagDictionary))]
for line in data:
    tag = line.strip().split()[0].split("/")[1]
    if (tag.isupper() and len(tag) == 2):
        tag = tag[0:2]
        tags.append(tag)
    words = line.strip().split()
    for word in words:
        wordTag = word.split("/")[-1]
        w = word.split("/")[0]
        if not (wordTag.isupper() and len(wordTag) == 2):
            continue
        else:
            wordTag = wordTag[0:2]
            if w in emissionMatrix:
                if wordTag not in emissionMatrix[w]:
                    emissionMatrix[w][wordTag] = 1
                else:
                    emissionMatrix[w][wordTag] += 1
            else:
                emissionMatrix[w] = {}
                emissionMatrix[w][wordTag] = 1
    for word in words:
        tag = word.split("/")[-1]
        if tag not in tagData:
            tagData[tag] = count + 1
            count = count + 1

initial_Matrix=dict(collections.Counter(tags))
#####transistion Matrix
transitionMatrix = [[1 for x in xrange(len(tagData))] for x in xrange(len(tagData))]
for line in data:
    prevTag = "none"
    words = line.strip().split()
    for word in words:
        wordTag = word.split("/")[1]
        if wordTag not in tagData:
            continue
        else:
            if prevTag != "none":
                transitionMatrix[tagData[prevTag] - 1][tagData[wordTag] - 1] += 1
                prevTag = wordTag
            else:
                prevTag = wordTag

##cal probabilities
transitionProb = [[1 for x in xrange(len(transitionMatrix))] for x in xrange(len(transitionMatrix))]
for i in xrange(0, len(transitionMatrix)):
    sumVal = 0.0
    for j in xrange(0, len(transitionMatrix)):
        sumVal += transitionMatrix[i][j]
    for j in xrange(len(transitionMatrix)):
        transitionProb[i][j] = transitionMatrix[i][j] / sumVal


emissionProb ={}
for word in emissionMatrix :
    sumVal = 0.0
    emissionProb[word] ={}
    for tag in emissionMatrix[word]:
        temp = emissionMatrix[word]
        sumVal+= temp[tag]
    for tag in emissionMatrix[word]:
        prob=emissionMatrix[word][tag]/sumVal
        emissionProb[word][tag] = prob

print initial_Matrix
with open("hmmmodel.txt",'wb') as f:
    json.dump([transitionProb,emissionProb,initial_Matrix,tagData],f)
print time.clock()-start