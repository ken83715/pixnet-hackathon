from gensim.models import word2vec
import jieba
import logging
import pickle

def main():

    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    sentences1 = []

    f = open('Gossiping-QA-Dataset.txt', 'r', encoding = 'utf-8')
    x = f.readlines()
    f.close()

    for row in x:
        s = row.split('\t')
        s1 = jieba.cut(s[0], cut_all=False)
        s1str = ' '.join(s1)
        s2 = jieba.cut(s[1], cut_all=False)
        s2str = ' '.join(s2)

        sentences1.append(s1str.split(' '))
        sentences1.append(s2str.split(' '))

    sentences = []
    for row in sentences1:
        temp = []
        for element in row:
            if len(element) != 0:
                temp.append(element)
        sentences.append(temp)

    f = open('sentences.p', 'wb')
    # dump the object to a file
    pickle.dump(sentences, f)
    f.close()

    model = word2vec.Word2Vec(sentences, size=100, min_count=1)

    #保存模型，供日後使用
    model.save("med100.model.bin")

    #模型讀取方式
    # model = word2vec.Word2Vec.load("your_model.bin")

if __name__ == "__main__":
    main()
