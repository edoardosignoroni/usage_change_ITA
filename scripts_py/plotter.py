# -*- coding: utf-8 -*-
"""
Created on Wed Sep 23 15:13:56 2020

@author: Edo
"""

#DATA VISUALIZATION v.1
import gensim
from sklearn.manifold import TSNE

import matplotlib.pyplot as plt
import pandas as pd

model = gensim.models.Word2Vec.load('C:/Users/Edo/Tesi/models/2020_210103_1709_300sg20.model')

vocab = list(model.wv.vocab)
X = model[vocab]

tsne = TSNE(n_components=2, perplexity=30, random_state=0)
X_tsne = tsne.fit_transform(X)

df = pd.DataFrame(X_tsne, index=vocab, columns=['x', 'y'])

fig = plt.figure(num=None, figsize=(100, 100), dpi=300, facecolor='w', edgecolor='k')
ax = fig.add_subplot(1,1,1)

ax.scatter(df['x'], df['y'], marker='.')

for word, pos in df. iterrows():
    ax.annotate(word, pos)
    
plt.show()

# # DATA VISUALIZATION from GENSIM DOCS
# from sklearn.manifold import TSNE                   # final reduction
# import numpy as np                                  # array handling


# def reduce_dimensions(model):
#     num_dimensions = 2  # final num dimensions (2D, 3D, etc)

#     vectors = [] # positions in vector space
#     labels = [] # keep track of words to label our data again later
#     for word in model.wv.vocab:
#         vectors.append(model.wv[word])
#         labels.append(word)

#     # convert both lists into numpy vectors for reduction
#     vectors = np.asarray(vectors)
#     labels = np.asarray(labels)

#     # reduce using t-SNE
#     vectors = np.asarray(vectors)
#     tsne = TSNE(n_components=num_dimensions, random_state=0)
#     vectors = tsne.fit_transform(vectors)

#     x_vals = [v[0] for v in vectors]
#     y_vals = [v[1] for v in vectors]
#     return x_vals, y_vals, labels


# x_vals, y_vals, labels = reduce_dimensions(model)

# def plot_with_plotly(x_vals, y_vals, labels, plot_in_notebook=True):
#     from plotly.offline import init_notebook_mode, iplot, plot
#     import plotly.graph_objs as go

#     trace = go.Scatter(x=x_vals, y=y_vals, mode='text', text=labels)
#     data = [trace]

#     if plot_in_notebook:
#         init_notebook_mode(connected=True)
#         iplot(data, filename='word-embedding-plot')
#     else:
#         plot(data, filename='word-embedding-plot.html')


# def plot_with_matplotlib(x_vals, y_vals, labels):
#     import matplotlib.pyplot as plt
#     import random

#     random.seed(0)

#     plt.figure(figsize=(12, 12))
#     plt.scatter(x_vals, y_vals)

#     #
#     # Label randomly subsampled 25 data points
#     #
#     indices = list(range(len(labels)))
#     selected_indices = random.sample(indices, 25)
#     for i in selected_indices:
#         plt.annotate(labels[i], (x_vals[i], y_vals[i]))

# try:
#     get_ipython()
# except Exception:
#     plot_function = plot_with_matplotlib
# else:
#     plot_function = plot_with_plotly

# plot_function(x_vals, y_vals, labels)