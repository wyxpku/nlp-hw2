#!/usr/local/bin/python3
import pickle, re
from prep import Review, translate


if __name__ == '__main__':
    trainfile = open('train1.pkl', 'rb')
    train_en = pickle.load(trainfile)
    train_cn = pickle.load(trainfile)
    trainfile.close()
    count = 0
    # for review in train_en:
    #     if review.cn_text is None:
    #         print(len(review.en_text))
    #         sentences = re.split('\n', review.en_text)
    #         review.cn_text = ''
    #         for s in sentences:
    #             if s is '' or s.isspace():
    #                 continue
    #             ts = translate(s, 'en', 'zh-CN')
    #             if ts is None:
    #                 review.cn_text = None
    #                 break
    #             else:
    #                 review.cn_text += ts

    for review in train_en:
        if review.hasNone():
            print(review.en_text)
            ts = translate(review.en_text, 'en', 'zh-CN')
            count += 1
    for review in train_cn:
        if review.hasNone():
            count += 1
    print(count)
    output = open('train1.pkl', 'wb')
    pickle.dump(train_en, output)
    pickle.dump(train_cn, output)
    output.close()
    # print(len(train_en))
    # print(len(train_cn))
    # print(train_en[0].en_text)
