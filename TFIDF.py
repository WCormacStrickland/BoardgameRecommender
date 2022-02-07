import sys
from operator import itemgetter

import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

from BggDataProcess import BggDataProcess


class TFIDF:
    def __init__(self):
        pass

    def get_recommendation(self, tags):
        vg_tags = tags

        df = pd.read_csv('word_list.csv')
        bgg_tags = df['0'].to_list()
        for tag in vg_tags:
            if tag not in bgg_tags:
                vg_tags.remove(tag)

        return self.get_matrix(vg_tags)

    def get_matrix(self, vg_tags):
        # bggDataProcess = BggDataProcess()
        # tag_list = bggDataProcess.get_tags()

        bgg_df = pd.read_csv('bgg_data.csv', low_memory=False)

        bgg_tag_df = pd.read_csv('bgg_data3.csv', low_memory=False)
        bgg_tag_list = bgg_tag_df.T.apply(lambda x: x.dropna().tolist()).tolist()

        vectorizer = TfidfVectorizer(analyzer='word', tokenizer=lambda i: i, lowercase=False, token_pattern=None)
        bg_matrix = vectorizer.fit_transform(bgg_tag_list)

        vg_matrix = vectorizer.transform([vg_tags])

        sim_matrix = linear_kernel(bg_matrix, vg_matrix).flatten()

        max_indices = np.argpartition(sim_matrix, -1000)[-1000:]

        bg_dict = {}
        for index in max_indices:
            if not bgg_df.loc[index, 'bayes_rating'] == 'nan':
                bg_dict[bgg_df.loc[index, 'name']] = bgg_df.loc[index, 'bayes_rating'] * sim_matrix[index]
        bg_dict = dict(sorted(bg_dict.items(), key=itemgetter(1), reverse=True)[:10])

        return bg_dict.keys()

    def get_word_list(self):
        bgg_df = pd.read_csv('bgg_data3.csv', low_memory=False)
        tag_list = bgg_df.T.apply(lambda x: x.dropna().tolist()).tolist()

        vectorizer = TfidfVectorizer(analyzer='word', tokenizer=lambda i: i, lowercase=False, token_pattern=None)
        vectorizer.fit_transform(tag_list)
        pd.DataFrame(list(vectorizer.vocabulary_.keys())).to_csv('word_list.csv', index=False)
