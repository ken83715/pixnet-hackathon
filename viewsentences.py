import pickle

fpath = 'sentences.p'
fopen = open(fpath, 'rb')
sentences = pickle.load(fopen) # load the object from the file
fopen.close()

for i in range(10):
    print(sentences[i])