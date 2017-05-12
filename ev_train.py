#!/usr/local/bin/python3
import pickle, re, string
from prep import Review, trans


if __name__ == '__main__':
    trainfile = open('test.pkl', 'rb')
    test = pickle.load(trainfile)
    trainfile.close()
    trainfile = open('train.pkl', 'rb')
    train_en = pickle.load(trainfile)
    train_cn = pickle.load(trainfile)
    trainfile.close()
    cnt = 0
    for item in test:
        if item.hasNone():
            cnt += 1
    for item in train_en:
        if item.hasNone():
            cnt += 1
    for item in train_cn:
        if item.hasNone():
            cnt += 1
    print(cnt)
