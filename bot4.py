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

model = gensim.models.Word2Vec.load('ptt_size_100_model_run_500.bin3')
all_vector=pickle.load(open('all_vector.p','rb'))
all_qb=pickle.load(open('all_qb.p','rb'))
rando = random.sample([i for i in range(len(all_vector))], 528000)
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
    score=[]
    for i in rando:
        try:
            t = 1 - spatial.distance.cosine(temp, all_vector[i])
            score.append(t)
            if t>0.8:
                return "".join(all_qb[i])
                # flag=1
                # break
        except Exception:
            score.append(0)
    # if flag!=1:
    # print(all_qb[score.index(max(score))])

    return randomsentences()

def randomsentences():
    sent = []
    sent.append('我覺得NO')
    sent.append('我覺得YES, 等等想想再告訴泥<3')
    sent.append('問問看五樓')
    sent.append('我幫你問柯P')
    sent.append('我幫你問痞客幫')
    sent.append('google壞了膩?')

    randomsent = random.randrange(len(sent))
    return sent[randomsent]

def algorithm(question_string):
    answer_string = algorithm_doc2v(question_string)
    return answer_string

@listen_to("『問題』" + ' (.*)')
def receive_question(message, question_string):
    if message._client.users[message._get_user_id()][u'name'] == "pixbot":
        answer = algorithm(question_string)
        message.send(answer)
        rando = random.sample([i for i in range(len(all_vector))], 528000)

main()