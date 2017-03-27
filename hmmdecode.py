import sys
import json
import operator
with open('hmmmodel.txt', 'rb') as file:
    model = json.load(file)

[transitionProb, emissionProb, initial_Matrix, tagData] = model

print tagData
print initial_Matrix
initialProb={}
sumVal =0.0
print len(initial_Matrix),len(tagData)
for tag in initial_Matrix:
    sumVal+= initial_Matrix[tag]
for tag in tagData :
    if tag in initial_Matrix:
        initialProb[tag] = initial_Matrix[tag]/sumVal
    else:
        initialProb[tag] = tagData[tag]/sumVal

text="sample.txt"
#text="catalan_corpus_dev_raw.txt"
#text = sys.argv[1]
with open(text, 'rb') as f:
    data = f.readlines()

def decode(words):
    prev={}
    taglist=[]
    res=[]
    ###assign initial prob
    if words[0] not in emissionProb:
        print max(initial_Matrix.iteritems(), key=operator.itemgetter(1))[0]
        tag=max(initial_Matrix.iteritems(), key=operator.itemgetter(1))[0]
        taglist.append(tag)

    else:
        print words[0]
        for tags in emissionProb[words[0]]:
            print initialProb[tags]
            print emissionProb[words[0]][tags]
            prev[tags] = initialProb[tags] * emissionProb[words[0]][tags]
            taglist.append(tags)
            #res.append(taglist)
    ##cal rest of the tags
    for word in xrange(1, len(words)):
        print "words",words[word]
        if words[word] not in emissionProb:
            maxProb = 0.0
            for currTag in initial_Matrix:
                for prevTag in taglist:
                    prob = transitionProb[tagData[prevTag] - 1][tagData[currTag] - 1]
                    if (maxProb < prob):
                        maxProb = prob
                        taglistPrev = [prevTag]
                        taglistCurr = [currTag]
            if (word != 1):
                #res.append(taglistPrev)

                res.append(taglistCurr)
                taglist = []
                taglist = taglistCurr
                    #taglist = []
                    #for key in wordTag:
                        #taglist.append(key)
            else:
                res.append(taglistPrev)
                res.append(taglistCurr)

        else:
            if words[word] in emissionProb:
                maxProb = 0.0
                wordTag = emissionProb[words[word]]
                for currTag in wordTag:
                    for prevTag in taglist:
                        print emissionProb[words[word]][currTag]
                        print prevTag,currTag
                        prob = transitionProb[tagData[prevTag] - 1][tagData[currTag] - 1] * emissionProb[words[word]][currTag]
                        if (maxProb < prob):
                            maxProb = prob
                            taglistPrev = [prevTag]
                            taglistCurr = [currTag]
                if (word != 1):
                    res.append(taglistCurr)
                    taglist = []
                    taglist=wordTag
                else:
                    res.append(taglistPrev)
                    res.append(taglistCurr)
    return res

with open("hmmoutput.txt",'w') as f:
    finalresult=[]
    for line in data:
        words = line.strip().split()
        tags = decode(words)
        result=[]
        flattentags = lambda tags: [item for sublist in tags for item in sublist]
        tags1 = flattentags(tags)
        if tags1.__len__()!=words.__len__():
            print len(tags1),len(words)
            print words
        for i in xrange(len(words)):
            print words[i]
            words[i] = words[i] + "/" +str(tags1[i])
            result.append(str(words[i]))
        print result
        f.write("%s\n" % str(" ".join(result)))