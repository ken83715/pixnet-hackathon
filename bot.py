# coding=UTF-8

import sys, os, datetime, time, re
import random
from slackbot import bot

TOKEN_MYBOT = os.environ['SLACK_BOT_TOKEN']
bot.settings.API_TOKEN  = TOKEN_MYBOT


from slackbot.bot import Bot
from slackbot.bot import respond_to
from slackbot.bot import listen_to

def main():
    bot = Bot()
    print('bot is running...')
    bot.run()

def algorithm(question_string):
    answer_string = u"我是回答"
    return answer_string

@listen_to("『問題』" + ' (.*)')
def receive_question(message, question_string):
    if message._client.users[message._get_user_id()][u'name'] == "pixbot":
        answer = algorithm(question_string)
        message.send(answer)

main()