# -*- coding: utf-8 -*-

import pickle

import theano
import numpy as np
import random
from keras.models import Sequential
from keras.layers import Dense, Activation,LSTM,RepeatVector,TimeDistributed
import jieba
import jieba.posseg as pseg
import sys
from keras.models import Sequential
from keras.layers.core import Dense, Dropout, Activation
sys.setrecursionlimit(1200000000)

fpath = 'X1_input.p'
fopen = open(fpath, 'rb')
X_train = pickle.load(fopen) # load the object from the file
fopen.close()

fpath2 = 'Y1_output.p'
fopen2 = open(fpath2, 'rb')
Y_train = pickle.load(fopen2) # load the object from the file
fopen2.close()

from keras.utils import np_utils

''' Shuffle training data '''
from sklearn.utils import shuffle
X_train,Y_train =shuffle(X_train,Y_train,random_state=100)

''' set the size of mini-batch and number of epochs'''
batch_size = 100
nb_epoch = 200

''' Import keras to build a DL model '''

model = Sequential()

#如果是第一次跑核心就跑Sequential()
#model = load_model('model.h5')

model.add(LSTM(500, return_sequences=True, input_shape=(17,800)))#input

model.add(LSTM(125,return_sequences=False))#1

#model.add(LSTM(625))#2

model.add(Dense(125))

model.add(RepeatVector(17))

#model.add(LSTM(625))#3

#model.add(LSTM(1250))#4

model.add(LSTM(250, return_sequences=True))#5

model.add(TimeDistributed(Dense(800)))
model.add(Activation('linear'))

from keras.optimizers import  Adam
model.compile(loss= 'mae',
              		optimizer='Adam',
              		metrics=['mae'])

print('Train...')

history_adam = model.fit(X_train, Y_train,
							batch_size=batch_size,
							nb_epoch=nb_epoch,
							verbose=1,
							shuffle=True,
                    		validation_split=0.1)

loss_adam= history_adam.history.get('loss')
#acc_adam = history_adam.history.get('acc')
val_loss_adam = history_adam.history.get('val_loss')
#val_acc_adam = history_adam.history.get('val_acc')

# output = open('core.pkl', 'wb')
# pickle.dump(model_adam, output)
# output.close()

model.save('model.h5')
#print(np.array(val_acc_adam))
