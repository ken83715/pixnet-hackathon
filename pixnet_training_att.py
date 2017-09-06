# -*- coding: utf-8 -*-

import pickle
import sys

import numpy as np
import random

from keras.utils import np_utils
from keras.models import Sequential
from keras.layers import Dense, Activation, LSTM, RepeatVector, TimeDistributed, Merge
from keras.layers.core import *


sys.setrecursionlimit(1200000000)

fpath = 'X1_input.p'
fopen = open(fpath, 'rb')
X_train = pickle.load(fopen) # load the object from the file
fopen.close()

fpath2 = 'Y1_output.p'
fopen2 = open(fpath2, 'rb')
Y_train = pickle.load(fopen2) # load the object from the file
fopen2.close()


''' Shuffle training data '''
from sklearn.utils import shuffle
X_train,Y_train =shuffle(X_train,Y_train,random_state=100)

''' set the size of mini-batch and number of epochs'''
batch_size = 100
nb_epoch = 200
INPUT_DIM = 800
TIME_STEPS = 17

''' Import keras to build a DL model '''

branch1 = Sequential()

branch1.add(Permute((2, 1), input_shape=(TIME_STEPS,INPUT_DIM)))

branch1.add(Reshape((INPUT_DIM, TIME_STEPS)))

branch1.add(Dense(TIME_STEPS, activation='softmax'))

branch1.add(Permute((2, 1), name='attention_vec'))



branch2 = Sequential()

branch2.add(Permute((2, 1), input_shape=(TIME_STEPS,INPUT_DIM)))

branch2.add(Permute((2, 1), name='input_vec'))



model = Sequential()

model.add(Merge([branch1, branch2], name='attention_mul', mode='mul'))

model.add(LSTM(1000, return_sequences=True, input_shape=(TIME_STEPS,INPUT_DIM))) 

# model.add(LSTM(125,return_sequences=False))#1

# model.add(LSTM(625))#2

# model.add(Dense(125, activation='sigmoid')(attention_mul))

# model.add(RepeatVector(17))

# model.add(LSTM(625))#3

# model.add(LSTM(1250))#4

model.add(LSTM(900, return_sequences=True))#5


model.add(TimeDistributed(Dense(INPUT_DIM)))
model.add(Activation('linear'))

from keras.optimizers import RMSprop
rmsprop = RMSprop(lr=0.01, rho=0.9, epsilon=1e-08, decay=0.0)

model.compile(loss= 'mean_squared_error',
              		optimizer=rmsprop,
              		metrics=['mae'])

print('Train...')

history_adam = model.fit([X_train, X_train], Y_train,
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

model.save('model_att.h5')
#print(np.array(val_acc_adam))
