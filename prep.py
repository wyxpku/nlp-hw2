#!/usr/local/bin/python3
from xml.etree import ElementTree as ET
from googletrans import Translator
import pickle
import random
import time
import os

TRAIN_DIR = 'evsam03/发布数据/'
TEST_DIR = 'evdata03/跨语言情感分类测试数据/'


def random_sleep():
    t = random.randint(0, 1)
    time.sleep(t)


def translate(text, src, dst):
    random_sleep()
    translator = Translator(service_urls=[
        'translate.google.cn',
    ])
    try:
        ts = translator.translate(text, src=src, dest=dst)
        return ts.text
    except Exception as e:
        print(e)
        return None
        print('--------------------')
        print('FUCK OFF: From %s to %s' % (src, dst))
        print(text)
        fname = input('Please input filename: ')
        while not os.path.exists(fname):
            fname = input('Please input filename: ')
        tfile = open(fname)
        text = tfile.read()
        tfile.close()
        return text
    return None


class Review:
    en_summary = None
    cn_summary = None
    en_text = None
    cn_text = None
    polarity = None
    category = None
    rid = None

    def __init__(self, dom, src='en'):
        # print(dom.find('review_id').text)
        if src == 'en':
            self.en_summary = dom.find('summary').text
            self.en_text = dom.find('text').text
            self.polarity = 0 if dom.find('polarity').text == 'N' else 1
        elif src == 'test':
            self.cn_summary = dom.find('summary').text
            self.cn_text = dom.find('text').text
            self.rid = dom.find('review_id').text
        else:
            self.cn_summary = dom.find('summary').text
            self.cn_text = dom.find('text').text
            self.polarity = 0 if dom.find('polarity').text == 'N' else 1

        self.category = dom.find('category').text

    def translate(self, src):
        if src == 'en':
            self.cn_summary = translate(self.en_summary, 'en', 'zh-CN')
            self.cn_text = translate(self.en_text, 'en', 'zh-CN')
        else:
            self.en_summary = translate(self.cn_summary, 'zh-CN', 'en')
            self.en_text = translate(self.cn_text, 'zh-CN', 'en')

    def hasNone(self):
        return self.en_text is None\
            or self.cn_text is None\
            or self.en_summary is None\
            or self.cn_summary is None


def load_review(fname, src='en'):
    reviews = []
    for item in ET.parse(fname).getroot():
        # print(item[0].text)
        reviews.append(Review(item, src))
    return reviews


def load_en():
    bookfname = TRAIN_DIR + 'Train_EN/book/train.data'
    dvdfname = TRAIN_DIR + 'Train_EN/dvd/train.data'
    musicfname = TRAIN_DIR + 'Train_EN/music/train.data'
    train_en = load_review(bookfname)
    train_en.extend(load_review(dvdfname))
    train_en.extend(load_review(musicfname))
    return train_en


def load_cn():
    bookfname = TRAIN_DIR + 'Train_CN/book/sample.data'
    dvdfname = TRAIN_DIR + 'Train_CN/dvd/sample.data'
    musicfname = TRAIN_DIR + 'Train_CN/music/sample.data'
    train_cn = load_review(bookfname, src='cn')
    train_cn.extend(load_review(dvdfname, src='cn'))
    train_cn.extend(load_review(musicfname, src='cn'))
    return train_cn


def load_test():
    bookfname = TEST_DIR + 'book/test.data'
    dvdfname = TEST_DIR + 'dvd/test.data'
    musicfname = TEST_DIR + 'music/test.data'
    train_cn = load_review(bookfname, src='test')
    train_cn.extend(load_review(dvdfname, src='test'))
    train_cn.extend(load_review(musicfname, src='test'))
    return train_cn


if __name__ == '__main__':

    # print(translate('你好啊', src='zh-CN', dst='en'))
    # # exit(0)
    # train_en = load_en()
    # train_cn = load_cn()
    test = load_test()

    # print('Labled EN review: %d' % len(train_en))
    # print('Labled CN review: %d' % len(train_cn))
    print('Labled test review: %d' % len(test))
    # trainslate reviews

    # en_num = len(train_en)
    # cn_num = len(train_cn)

    # for i in range(cn_num):
    #     print('Translating CN: %d of %d' % (i + 1, cn_num))
    #     train_cn[i].translate('cn')

    # for i in range(en_num):
    #     print('Translating EN: %d of %d' % (i + 1, en_num))
    #     train_en[i].translate('en')

    # output = open('train.pkl', 'wb')
    # pickle.dump(train_en, output)
    # pickle.dump(train_cn, output)
    # output.close()
    test_num = len(test)


    for i in range(test_num):
        print('Translating test: %d of %d' % (i + 1, test_num))
        test[i].translate('cn')
    output = open('test.pkl', 'wb')
    pickle.dump(test, output)
    output.close()
    exit(0)
