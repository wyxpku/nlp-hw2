#!/usr/local/bin/python3
import pickle
from prep import Review
from xml.etree import ElementTree as ET


def load_test_set():
    trainfile = open('test.pkl', 'rb')
    test = pickle.load(trainfile)
    trainfile.close()
    return test


fnames = [
    'evans03/跨语言情感分类答案/book/testResult.data',
    'evans03/跨语言情感分类答案/dvd/testResult.data',
    'evans03/跨语言情感分类答案/music/testResult.data',
]
id_pol = {}
for fname in fnames:
    for item in ET.parse(fname).getroot():
        rid = item.find('review_id').text
        pol = 0 if item.find('polarity').text == 'N' else 1
        id_pol[rid] = pol

reviews = load_test_set()

for review in reviews:
    review.polarity = id_pol[review.rid]

cnt = 0
for review in reviews:
    if review.polarity is None:
        cnt += 1
print(cnt)

output = open('test-ans.pkl', 'wb')
pickle.dump(reviews, output)
output.close()
