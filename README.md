# usage_change_ITA
Code, data, and trained models for the r/italy COVID-19 Usage Change Corpus. A corpus was created by scraping text from submissions on the [Italian subreddit](https://www.reddit.com/r/italy) between Jan 30 and Nov 30 of 2019 and 2020. Scraping was done with [praw](https://github.com/praw-dev/praw/blob/master/docs/index.rst) and [psaw](https://github.com/openai/psaw.)

The data was analyzed with the method from [Gonen et al. 2020](https://github.com/gonenhila/usage_change) to detect short-term usage change in Italian between 2019 and 2020.


## Download data
Raw and preprocessed data can be downloaded [here](https://drive.google.com/file/d/125kNZOOgBB1SsHQ3CQAODriQdGRxPcyN/view?usp=sharing)

## Algorithm output
The output of the usage change detection algorithm by [Gonen et al. 2020](https://github.com/gonenhila/usage_change) is saved in the file "detect_2019_2020_.txt". This is the outcome for the lemmatized corpora.

## Visualization
The data were visualized with the [Embedding Projector](https://projector.tensorflow.org/). The files are available in the models directory. To visualize the data, load *tensors_[year].tsv* and *tensors_[year]_meta.tsv* in the projector. You can then run one of the dimensionality reduction algorithms provided by the tool, or *load tensors_[year]_bookmark.txt* to use the already labeled one (t-SNE, 10000 iterations).
