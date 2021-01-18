# -*- coding: utf-8 -*-
"""
Created on Wed Sep 23 15:09:08 2020

@author: Edo
"""

#WORD2VEC TRAINING
# import modules 
import gensim
import logging

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

year = 2020

model = gensim.models.Word2Vec(corpus_file = 'days_{}/processed/days_{}_sentencesL.txt'.format(year, year), size=300, min_count=20, workers=6, sg=1, max_vocab_size=50000)
model_name = ''
model.save('models/{}_{}.model'.format(year, model_name))
word_vectors = model.wv
word_vectors.save('models\\{}_{}.kv'.format(year, model_name))

w2v_path = 'models\\{}_{}.kv'.format(year, model_name)
file_name = '{}_{}'.format(year, model_name)
w2v = gensim.models.KeyedVectors.load(w2v_path)

import io

#converts gensim .kv into .tsv to use in the Embedding Projector
# Vector file, `\t` seperated the vectors and `\n` seperate the words
"""
0.1\t0.2\t0.5\t0.9
0.2\t0.1\t5.0\t0.2
0.4\t0.1\t7.0\t0.8
"""
out_v = io.open('models/{}.tsv'.format(file_name), 'w', encoding='utf-8')

# Meta data file, `\n` seperated word
"""
token1
token2
token3
"""
out_m = io.open('models/{}_meta.tsv'.format(file_name), 'w', encoding='utf-8')

# Write meta file and vector file
for index in range(len(w2v.index2word)):
    word = w2v.index2word[index]
    vec = w2v.vectors[index]
    out_m.write(word + "\n")
    out_v.write('\t'.join([str(x) for x in vec]) + "\n")
out_v.close()
out_m.close()


 