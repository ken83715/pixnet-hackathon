# coding=UTF-8

import sys, os, datetime, time, re
import random
from slackbot import bot

from slackbot.bot import Bot
from slackbot.bot import respond_to
from slackbot.bot import listen_to

from keras.models import load_model
from keras.models import model_from_json
from keras.models import load_model

from keras.utils import CustomObjectScope

from gensim import models
import jieba
import pickle
import numpy as np

def main():
    bot = Bot()
    print('bot is running...')
    bot.run()

def predictsentences(sentences):
    s1 = jieba.cut(sentences, cut_all=False)
    s1str = ' '.join(s1)
    s1 = s1str.split(' ')

    count = 0

    temp = []
    for word in s1:
        try:
            if len(word) != 0:
                temp.append(word2ve_model[word])
        except KeyError:
            #print(word)
            #print(s[0])
            count = count + 1

    while len(temp) < 7:
        temp.append(averg)
    
    inputarray_x = []
    inputarray_x.append(temp[0:7])

    inputarray = np.array(inputarray_x)
    print(inputarray.shape)

    answer = ''
    try:
        answerarray = loaded_model.predict(x = [inputarray, inputarray])
        for w in answerarray[0]:
            answ = word2ve_model.most_similar(positive=[w], topn=1)
            if answ[0][0] != '，' and answ[0][0] != '\n':
                answer = answer + answ[0][0]
    except ValueError:
        print(ValueError)
        answer = '我覺得不行'

    return answer

def algorithm(question_string):
    print(question_string)
    answer_string = predictsentences(question_string)
    return answer_string

@listen_to("『問題』" + ' (.*)')
def receive_question(message, question_string):
    if message._client.users[message._get_user_id()][u'name'] == "pixbot":
        answer = algorithm(question_string)
        message.send(answer)

TOKEN_MYBOT = os.environ['SLACK_BOT_TOKEN']
bot.settings.API_TOKEN  = TOKEN_MYBOT

json_file = open('ptt_model_att.json', 'r')
loaded_model_json = json_file.read()
json_file.close()

loaded_model = model_from_json(loaded_model_json)
loaded_model.load_weights('ptt_model_att_weights.h5')

word2ve_model = models.Word2Vec.load('ptt_med100.model.bin')

fpath = 'ptt_averg.p'
fopen = open(fpath, 'rb')
averg = pickle.load(fopen) # load the object from the file
fopen.close()

print('load model success')

main()