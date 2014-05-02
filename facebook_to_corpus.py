# -*- coding: utf-8 -*-
"""
make corpus from Facebook
"""
import bs4
import csv
import MeCab
import re

IN_PATH = 'inbox/facebook-nishiohirokazu/html'
TXT_PATH = 'txt/facebook.txt'
CORPUS_PATH = 'corpus/facebook-wakati.txt'

def main(path=PATH, txt=TXT_PATH, corpus=CORPUS_PATH):
    tagger = MeCab.Tagger('-Owakati')
    fo = file(txt, 'w')
    fow = file(corpus, 'w')

    soup = bs4.BeautifulSoup(file(path + '/wall.htm').read())
    for div in soup.find_all('div', 'comment'):
        if 'Nishio Hirokazu updated his status.' in div.parent.text:
            line = div.text
            line = ' '.join(line.split('\n'))
            line = re.sub('https?://.*', '', line)
            line = line.encode('utf-8')
            fo.write(line + '\n')
            fow.write(tagger.parse(line))

    soup = bs4.BeautifulSoup(file(path + '/messages.htm').read())
    for div in soup.find_all('div', 'thread'):
        for p in div.find_all('p'):
            line = p.text
            line = ' '.join(line.split('\n'))
            line = re.sub('https?://.*', '', line)
            line = line.encode('utf-8')
            fo.write(line + '\n')
            fow.write(tagger.parse(line))

    fo.close()
    fow.close()

if __name__ == '__main__':
    main()
