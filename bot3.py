# coding=UTF-8

import sys, os, datetime, time, re
import random
from slackbot import bot

from slackbot.bot import Bot
from slackbot.bot import respond_to
from slackbot.bot import listen_to

import jieba
import pickle
from gensim import models

TOKEN_MYBOT = os.environ['SLACK_BOT_TOKEN']
bot.settings.API_TOKEN  = TOKEN_MYBOT

b=pickle.load(open('222.p','rb'))

jieba.set_dictionary('dict.txt.big')
fin = open('my_stopwords.txt', encoding='utf-8')
stopwords = [line[:-1] for line in fin]
fin.close()

data=pickle.load(open('ptt_qa_40w.p','rb'))
a=[]
b=[]
score=[]
for i in data:
    a.append(i[0])
    b.append(i[1])

model=models.Doc2Vec.load('ptt_dov2vec_model.p')

def main():
    bot = Bot()
    print('bot is running...')
    bot.run()

def str_to_jieba(ss):
    t=jieba.lcut(ss)
    text=[]
    for i in t:
        if i not in stopwords:
            text.append(i)
    return text

def algorithm_word2v(question_string):
    s=question_string
    # flag = 0
    score=[]
    ss=str_to_jieba(s)
    for i in a:
        if len(i)==0:
            score.append(0)
            continue
        try:
            fx=model.n_similarity(ss,i)
            score.append(fx)
            if fx>0.8677:
                # print(b[a.index(i)],fx)
                return "".join(b[a.index(i)])
                # flag=1
                # break
        except Exception:
            score.append(0)
        
    #　if flag!=1:
        # print("".join(b[score.index(max(score))]))
    x = max(score)
    if x < 0.6:
        return randomsentences()

    return "".join(b[score.index(x)])

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
        answer_string = algorithm_word2v(question_string)
    except:
        answer_string = randomsentences()

    return answer_string

@listen_to("『問題』" + ' (.*)')
def receive_question(message, question_string):
    if message._client.users[message._get_user_id()][u'name'] == "pixbot":
        answer = algorithm(question_string)
        message.send(answer)

main()