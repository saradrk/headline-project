#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 11 12:14:12 2021

@author: Sara Derakhshani
"""

import spacy
from newspaper_headline_corpus import NewspaperHeadlineCorpus
import os
import logging
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

logging.basicConfig(filename='headline_analyser.log',
                    level=logging.INFO,
                    format='%(asctime)s %(message)s')


class HeadlineAnalyser:
    """Class for automatic text analysis of newspaper headlines.

    Attributes
    ----------
    spacy_pipeline : str, optional
        The spacy pipeline used for analyzing (default: 'de_core_news_sm')

    Methods
    -------
    compute_n_top_features(corpus, features=None, n=3):
        Computes the most frequent tokens by part-of-speech tags.
    """

    pipelines = ('de_core_news_sm',
                 'de_core_news_md',
                 'de_core_news_lg',
                 'de_dep_news_trf'
                 )
    pos_tags = {'NOUN', 'VERB', 'ADJ'}

    def __init__(self, spacy_pipeline='de_core_news_sm'):
        if spacy_pipeline not in self.pipelines:
            raise ValueError
        self.nlp = spacy.load(spacy_pipeline)

    @staticmethod
    def tfidf_cos_similarity(corpus, heatmap_png=None):
        """Compute TF-IDF representation of corpora and cosine similarity.

        Compute TF-IDF matrix and cosine similarity of TF-IDF vectors.
        Saves heatmap representation as png if filename is passed as argument.

        Args
        ----
        corpus : NewspaperHeadlineCorpus object
            Collection of different newspaper headline corpora
        heatmap_png : str, optional
            Name of the png file for the cosine similarity heatmap.

        Returns
        -------
        dict in the form of {newspaper: {POS: [(token, token count), ], }, }
        """
        if isinstance(corpus, NewspaperHeadlineCorpus):
            doc_order = []
            docs = []
            logging.info('Compute TF-IDF...')
            for newspaper, headlines in corpus.corpora.items():
                logging.info(f'Processing {newspaper}')
                hl_texts = [hl.all_lines for hl in headlines]
                docs.append(' '.join(hl_texts))
                doc_order.append(newspaper)
            vectorizer = TfidfVectorizer()
            X = vectorizer.fit_transform(docs)
            if heatmap_png:
                X = np.array(cosine_similarity(X))
                mask = np.zeros_like(X)
                mask[np.triu_indices_from(mask)] = True
                with sns.axes_style("white"):
                    ax = sns.heatmap(X,
                                     annot=True,
                                     xticklabels=doc_order,
                                     yticklabels=doc_order,
                                     mask=mask,
                                     vmax=1,
                                     square=True,
                                     cmap="YlGnBu")
                ax.set_title("Cosine similarity")
                plt.savefig(heatmap_png)
                logging.info(f'Heatmap saved as: {heatmap_png}')
            return cosine_similarity(X)
        else:
            raise ValueError

    def compute_n_top_features(self, corpus, features=None, n=3, case_insensitive=False):
        """Compute most frequent tokens by part-of-speech tags.

        Args
        ----
        corpus : NewspaperHeadlineCorpus object
            Collection of different newspaper headline corpora
        features : list, optional
            The POS tags that are counted (default are predefined tags
            ['NOUN', 'VERB', 'ADJ'])
        n : int, optional
            The number of top features to output (default is 3)
        case_insensitive : bool, optional
            If the computation should be case-insensitive (default is False)

        Returns
        -------
        dict in the form of {newspaper: {POS: [(token, token count), ], }, }
        """
        logging.info(f'Computing {n} top features (case insensitive: {case_insensitive})')
        # use predefined POS tags as features if features are not given as arg
        # else use input features if all features are valid/in predefined tags
        pos_tags = self.pos_tags
        if features:
            if set(features).issubset(pos_tags):
                pos_tags = features
            else:
                raise ValueError
        out_dict = {}
        if isinstance(corpus, NewspaperHeadlineCorpus):
            for newspaper, headlines in corpus.corpora.items():
                logging.info(f'Computing {newspaper} features...')
                out_dict[newspaper] = {}
                # count tokens for each POS tag: {POS: {token: count, }, }
                all_tokens = {}
                for hl in headlines:
                    doc = self.nlp(hl.all_lines)
                    for token in doc:
                        tok = token.text
                        # handle case-sensitivity
                        if case_insensitive:
                            tok = token.text.lower()
                        # if top features for the POS tag should be counted:
                        # count occurence +1 if tag and token already exist
                        # in all_tokens, add new key and count 1
                        if token.pos_ in self.pos_tags:
                            if token.pos_ in all_tokens:
                                if tok in all_tokens[token.pos_]:
                                    all_tokens[token.pos_][tok] += 1
                                else:
                                    all_tokens[token.pos_][tok] = 1
                            else:
                                all_tokens[token.pos_] = {tok: 1}
                for pos_tag in all_tokens:
                    pos_toks = [(tok, count) for tok, count in all_tokens[pos_tag].items()]
                    toks_freq_sorted = sorted(pos_toks,
                                              key=lambda tok_c: tok_c[1],
                                              reverse=True)
                    out_dict[newspaper][pos_tag] = toks_freq_sorted[0:n]
                logging.info(out_dict[newspaper])
            logging.info('Process finished.')
            return out_dict
        else:
            raise ValueError


if __name__ == '__main__':
    AfD_Corpus = NewspaperHeadlineCorpus()
    path = 'local/data/csv/'
    for file in os.listdir(path):
        if file.endswith(".csv"):
            newspaper_name = file.split('_')[-1][0:-4]
            AfD_Corpus.add_corpus(newspaper_name,
                                  os.path.join(path, file)
                                  )
    HA = HeadlineAnalyser()
    HA.tfidf_cos_similarity(AfD_Corpus, heatmap_png='cosine_similarity.png')
#    HA.compute_n_top_features(AfD_Corpus, case_insensitive=True)
