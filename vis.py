# -*- coding: utf-8 -*-
"""
given a word and visualize near words
"""
import word2vec_boostpython as w2v
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import matplotlib.font_manager

font = matplotlib.font_manager.FontProperties(fname='./ipag.ttc')
FONT_SIZE = 10
TEXT_KW = dict(fontsize=FONT_SIZE, fontweight='bold', fontproperties=font)

filename = 'word2vec/jawiki.bin'
#filename = 'word2vec/orj.bin'
print 'loading'
data = w2v.load(filename)
print 'loaded'
nbest = 15

while True:
    query = raw_input('query: ')
    if query.startswith('nbest='):
        nbest = int(query[6:])
        continue
    if ', ' not in query:
        words = [query] + w2v.search(data, query)[:nbest]
    else:
        words = query.split(', ')
    print ', '.join(words)
    mat = w2v.get_vectors(data)
    word_indexes = [w2v.get_word_index(data, w) for w in words]
    if word_indexes == [-1]:
        print 'not in vocabulary'
        continue

    # do PCA
    X = mat[word_indexes]
    pca = PCA(n_components=2)
    pca.fit(X)
    print pca.explained_variance_ratio_
    X = pca.transform(X)
    xs = X[:, 0]
    ys = X[:, 1]

    # draw
    plt.clf()
    plt.scatter(xs, ys, marker = 'o')
    for i, w in enumerate(words):
        plt.annotate(
            w.decode('utf-8', 'ignore'),
            xy = (xs[i], ys[i]), xytext = (3, 3),
            textcoords = 'offset points', ha = 'left', va = 'top',
            **TEXT_KW)

    plt.savefig('last.png')
    print 'ok.'
