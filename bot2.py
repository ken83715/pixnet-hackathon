# coding=UTF-8

import sys, os, datetime, time, re
import random
from slackbot import bot

from slackbot.bot import Bot
from slackbot.bot import respond_to
from slackbot.bot import listen_to

import pickle
import gensim
import numpy as np
import jieba
from scipy import spatial

TOKEN_MYBOT = os.environ['SLACK_BOT_TOKEN']
bot.settings.API_TOKEN  = TOKEN_MYBOT

jieba.set_dictionary('dict.txt.big')
fin = open('my_stopwords.txt', encoding='utf-8')
stopwords = [line[:-1] for line in fin]
fin.close()

def str_to_jieba(ss):
    t=jieba.lcut(ss)
    text=[]
    for i in t:
        if i not in stopwords:
            text.append(i)
    return text

b=pickle.load(open('222.p','rb'))
model = gensim.models.Word2Vec.load('ptt_size_100_model_run_500.bin3')
a_vector=pickle.load(open('123a_vector.p','rb'))

def main():
    bot = Bot()
    print('bot is running...')
    bot.run()

def algorithm_doc2v(question_string):
    s=question_string
    ss = str_to_jieba(s)
    temp = np.zeros((100,))
    n = 0
    for j in ss:
        try:
            temp+=model.wv[j]
            n+=1
        except Exception as e:
            continue
    temp=temp/n
    a_score=[]
    for i in a_vector:
        try:
            t = 1 - spatial.distance.cosine(temp, i)
        except Exception as e:
            t=0
        if t > 0.8677:
            return "".join(b[a_vector.index(i)])
        a_score.append(t)
    ans="".join(b[a_score.index(max(a_score))])
    return ans

def randomsentences():
    sent = []
    sent.append('我覺得不行')
    sent.append('我覺得可以')
    sent.append('問問看五樓')
    sent.append('我幫你問柯P')
    sent.append('<3<3<3<3')
    sent.append('灑花 (*￣▽￣)/‧☆*"`*-.,_,.-*`"*-.,_☆')

    randomsent = random.randrange(len(sent))
    return sent[randomsent]

def algorithm(question_string):
    answer_string = ''
    try:
        answer_string = algorithm_doc2v(question_string)
    except:
        answer_string = randomsentences()

    return answer_string

@listen_to("『問題』" + ' (.*)')
def receive_question(message, question_string):
    if message._client.users[message._get_user_id()][u'name'] == "pixbot":
        answer = algorithm(question_string)
        message.send(answer)

main()