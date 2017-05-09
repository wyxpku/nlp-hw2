#!/usr/local/bin/python3
import pickle, re, string
from prep import Review


def clean_en(s):
    exclude = set(string.punctuation)
    return ''.join(ch for ch in s if ch not in exclude)


def clean_cn(s):
    return ''.join(re.findall(u'[\u4e00-\u9fff]+', s))


if __name__ == '__main__':
    trainfile = open('train2.pkl', 'rb')
    train_en = pickle.load(trainfile)
    train_cn = pickle.load(trainfile)
    trainfile.close()
    print(train_en[0].en_text)
    print(clean_en(train_en[0].en_text))

    print(train_en[0].cn_text)
    print(clean_cn(train_en[0].cn_text))