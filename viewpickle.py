import pickle

fpath = 'X1_input.p'
fopen = open(fpath, 'rb')
X_train = pickle.load(fopen) # load the object from the file
fopen.close()

fpath = 'Y1_output.p'
fopen = open(fpath, 'rb')
Y_train = pickle.load(fopen) # load the object from the file
fopen.close()

print(len(X_train))
print(len(Y_train))

print(len(X_train[0]))
print(len(Y_train[0]))

print(len(X_train[0][0]))
print(len(Y_train[0][0]))

print(type(X_train))
print(type(Y_train))

print(type(X_train[0]))
print(type(Y_train[0]))

print(type(X_train[0][0]))
print(type(Y_train[0][0]))

print(X_train[0][0][0], ' ', Y_train[0][0][0])
print(X_train[0][0][1], ' ', Y_train[0][0][1])
print(X_train[0][0][2], ' ', Y_train[0][0][2])
print(X_train[0][0][3], ' ', Y_train[0][0][3])