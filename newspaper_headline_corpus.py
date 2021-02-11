#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 10 12:30:22 2021

@author: Sara Derakhshani
"""
import logging
import csv
from newspaper_headline import NewspaperHeadline


logging.basicConfig(filename='newspaper_headline_corpus.log',
                    level=logging.INFO,
                    format='%(asctime)s %(message)s')


class NewspaperHeadlineCorpus:
    """Class for merging newspaper headline corpora to a single corpus.

    Attributes:
        corpora (dict) -- represents the different newspaper corpora
        data_size (int) -- the number of headlines in the corpus

    Methods:
        add_corpus(newspaper, corpus_csv) -- add a corpus in csv format to a
            NewspaperHeadlineCorpus object
    """

    def __init__(self):
        self.corpora = {}
        self.data_size = 0

    def add_corpus(self, newspaper, corpus_csv):
        """Read and process newspaper data from csv file.

        Add name of the newspaper to corpora dict with list of
        NewspaperHeadline objects constructed from the newspaper corpus as
        value.

        Args:
            newspaper (str) -- the name of the newspaper
            corpus_csv (str) -- path to the csv file containing the corpus
        """
        try:
            with open(corpus_csv, 'r', encoding='utf-8') as csvfile:
                logging.info(f'Processing {newspaper} data...')
                self.corpora[newspaper] = []
                reader = csv.DictReader(csvfile)
                entry_count = 0
                for row in reader:
                    self.corpora[newspaper].append(
                        self.__construct_headline_object(row)
                        )
                    entry_count += 1
        except Exception as e:
            logging.info(e)
        else:
            csvfile.close()
            self.data_size += entry_count
            logging.info('{} entries processed'.format(entry_count))

    @staticmethod
    def __construct_headline_object(csv_row):
        """Construct NewspaperHeadline object from newspaper corpus entry.

        Args:
            csv_row (dict) -- csv entry of a headline
        Returns:
            NewspaperHeadline object
        """
        headline = NewspaperHeadline(csv_row['ÜBERSCHRIFT'])
        headline.overline = csv_row['SPITZMARKE']
        headline.subline = csv_row['UNTERÜBERSCHRIFT']
        headline.year = csv_row['JAHR']
        headline.month = csv_row['MONAT']
        headline.day = csv_row['TAG']
        return headline
