import pickle
import jieba
from gensim.models import word2vec
from gensim import models
import logging, gensim, os
import numpy as np

model = models.Word2Vec.load('med100.model.bin')

# fpath = 'sentences.p'
# fopen = open(fpath, 'rb')
# sentences = pickle.load(fopen) # load the object from the file
# fopen.close()

# seg = []
# for row in sentences:
#     for element in row:
#         seg.append(element)

# averg = []
# for i in range(100):
#     averg.append(0)

# for i in range(len(seg)):
#     try:
#         temp = model[seg[i]]
#     except KeyError:
#         temp = []
#     else:
#         for j in range(100):
#             averg[j] = averg[j] + temp[j]

# for i in range(100):
#     averg[i] = averg[i] / len(seg)

# print(averg)

# f = open('averg.p', 'wb')
# # dump the object to a file
# pickle.dump(averg, f)
# f.close()

fpath = 'averg.p'
fopen = open(fpath, 'rb')
averg = pickle.load(fopen) # load the object from the file
fopen.close()

X_train = []
Y_train = []

f = open('Gossiping-QA-Dataset.txt', 'r', encoding = 'utf8')
x = f.readlines()
f.close()

count = 0

for i in range(len(x)):
#    print(row)
    s = x[i].split('\t')
    if len(s) == 2:
        # print("cut")
        s1 = jieba.cut(s[0], cut_all=False)
        s1str = ' '.join(s1)
        s2 = jieba.cut(s[1], cut_all=False)
        s2str = ' '.join(s2)

        s1 = s1str.split(' ')
        s2 = s2str.split(' ')
        temp1 = []
        temp2 = []
        for word in s1:
            try:
                if len(word) != 0:
                    temp1.append(model[word])
            except KeyError:
                #print(word)
                #print(s[0])
                count = count + 1

        for word in s2:
            try:
                if len(word) != 0:
                    temp2.append(model[word])
            except KeyError:
                #print(word)
                #print(s[1])
                count = count + 1

        while len(temp1) < 7:
            temp1.append(averg)
        while len(temp2) < 7:
            temp2.append(averg)

        X_train.append(temp1[0:7])
        Y_train.append(temp2[0:7])

print(len(X_train))
print(len(Y_train))

npX_train = np.array(X_train)
npY_train = np.array(Y_train)


f = open('X1_input.p', 'wb')
# dump the object to a file
pickle.dump(npX_train, f)
f.close()
    
f = open('Y1_output.p', 'wb')
# dump the object to a file
pickle.dump(npY_train, f)
f.close()

print('KeyError: ', count)
