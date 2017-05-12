#!/usr/local/bin/python3
import pickle
from prep import Review
from sklearn.feature_extraction.text import TfidfVectorizer
import jieba
from sklearn.naive_bayes import MultinomialNB
import numpy as np
from copy import deepcopy


swset = None


def load_test_set():
    trainfile = open('test-ans.pkl', 'rb')
    test = pickle.load(trainfile)
    trainfile.close()
    return test


def load_train_set():
    trainfile = open('train.pkl', 'rb')
    train_en = pickle.load(trainfile)
    train_cn = pickle.load(trainfile)
    trainfile.close()
    return train_en, train_cn


def load_stopwords_set():
    stopwords = set()
    swfname = 'ChineseStopWords.txt'
    with open(swfname, 'r') as file:
        for line in file.readlines():
            # if line[-1] == '\0':
            # print(line)
            if line[-1] == '\n':
                stopwords.add(line[:-1])
            else:
                stopwords.add(line)
            # print(line[:-1] + '-----')
    return stopwords


def mycut(text):
    words = jieba.cut(text, cut_all=False)
    ret = []
    for word in words:
        if word not in swset:
            ret.append(word)
    return ' '.join(ret)


def accuracy(ys1, ys2, ys):
    pred = ys1 + ys2
    predict = []
    for i in range(len(ys)):
        if pred[i][0] > pred[i][1]:
            predict.append(0)
        else:
            predict.append(1)
    cnt = 0
    for i in range(len(ys)):
        if predict[i] == ys[i]:
            cnt += 1
    return cnt / len(ys)


if __name__ == '__main__':
    train_en, train_cn = load_train_set()
    test = load_test_set()
    labeled_set = deepcopy(train_en + train_cn)
    unlabeled_set = deepcopy(test)

    swset = load_stopwords_set()
    # pre load jieba dict
    mycut('xxx')
    ntimes = 30
    p = 5
    n = 5

    en_vectorizer = TfidfVectorizer(min_df=1, max_features=5000)
    cn_vectorizer = TfidfVectorizer(min_df=1, max_features=5000)

    corpus_en = []
    corpus_cn = []
    for review in train_en + train_cn:
        corpus_en.append(review.en_summary + '.' + review.en_text)
        corpus_cn.append(mycut(review.cn_summary + '。' + review.cn_text))

    en_vectorizer.fit(corpus_en)
    cn_vectorizer.fit(corpus_cn)

    test_en_text = []
    test_cn_text = []
    for review in test:
        test_en_text.append(review.en_summary + '.' + review.en_text)
        test_cn_text.append(mycut(review.cn_summary + '。' + review.cn_text))
    test_ys = [item.polarity for item in test]
    test_en_xs = en_vectorizer.transform(test_en_text)
    test_cn_xs = cn_vectorizer.transform(test_cn_text)

    print('Training for %d times. p=%d, n=%d' % (ntimes, p, n))

    for itime in range(ntimes):
        print('----------Train #%d----------' % itime)

        print('Sample number of labeled set: %d' % len(labeled_set))
        print('Sample number of unlabeled set: %d' % len(unlabeled_set))
        labeled_en_text = []
        labeled_cn_text = []
        labeled_ys = []

        unlabeled_en_text = []
        unlabeled_cn_text = []
        unlabeled_ys = []

        for review in labeled_set:
            labeled_en_text.append(review.en_summary + '.' + review.en_text)
            labeled_cn_text.append(
                mycut(review.cn_summary + '。' + review.cn_text)
            )
            labeled_ys.append(review.polarity)

        for review in unlabeled_set:
            unlabeled_en_text.append(review.en_summary + '.' + review.en_text)
            unlabeled_cn_text.append(
                mycut(review.cn_summary + '。' + review.cn_text)
            )
            unlabeled_ys.append(review.polarity)

        labeled_en_xs = en_vectorizer.transform(labeled_en_text).toarray()
        labeled_cn_xs = cn_vectorizer.transform(labeled_cn_text).toarray()
        unlabeled_en_xs = en_vectorizer.transform(unlabeled_en_text).toarray()
        unlabeled_cn_xs = cn_vectorizer.transform(unlabeled_cn_text).toarray()

        en_clf = MultinomialNB(alpha=0.01)
        cn_clf = MultinomialNB(alpha=0.01)

        en_clf.fit(labeled_en_xs, labeled_ys)
        cn_clf.fit(labeled_cn_xs, labeled_ys)

        en_predict = en_clf.predict(unlabeled_en_xs)
        en_predict_proba = en_clf.predict_proba(unlabeled_en_xs)
        cn_predict = cn_clf.predict(unlabeled_cn_xs)
        cn_predict_proba = cn_clf.predict_proba(unlabeled_cn_xs)
        acc = accuracy(
            en_clf.predict_proba(test_en_xs),
            cn_clf.predict_proba(test_cn_xs),
            test_ys
        )
        print('Accuracy: %f' % acc)

        # print(ans[:100])
        # print(en_predict[:100])
        # print(cn_predict[:100])
        # get index of top p predict_proba in en_predict
        en_idx_proba = []
        for idx, proba in enumerate(en_predict_proba):
            en_idx_proba.append((idx, proba[en_predict[idx]]))
        # print(en_idx_proba)
        sorted_en_proba = sorted(
            en_idx_proba,
            key=lambda tmp: tmp[1],
            reverse=True
        )
        selected_en_idx = [item[0] for item in sorted_en_proba[:p]]

        # get index of top n predict_proba in en_predict
        cn_idx_proba = []
        for idx, proba in enumerate(cn_predict_proba):
            cn_idx_proba.append((idx, proba[cn_predict[idx]]))
        sorted_cn_proba = sorted(
            cn_idx_proba,
            key=lambda tmp: tmp[1],
            reverse=True
        )
        selected_cn_idx = [item[0] for item in sorted_cn_proba[:n]]
        idx_merge = list(set(selected_en_idx) | set(selected_cn_idx))
        idx_merge.sort()
        selected_idx = []
        for idx in idx_merge:
            if en_predict[idx] != cn_predict[idx]:
                continue
            selected_idx.append(idx)
            # label.append(en_predict[idx])

        # train_enx.append(test_enx[idx])
        # print(selected_idx)
        for idx in selected_idx:
            unlabeled_set[idx].polarity = en_predict[idx]
            labeled_set.append(unlabeled_set[idx])
        new_unlabeled_set = []
        for idx in range(len(unlabeled_set)):
            if idx in selected_idx:
                continue
            new_unlabeled_set.append(unlabeled_set[idx])
        unlabeled_set = new_unlabeled_set
        print('label %d sample' % len(selected_idx))
