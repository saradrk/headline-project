#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 10 15:56:19 2021

@author: Sara Derakhshani
"""


class NewspaperHeadline:
    """Class for newspaper headline objects.

    Attributes:
        headline (str) -- the headline
        overline (str) -- the overline (default: None)
        subline (str) -- the subline (default: None)
        year (int or str) -- the publication year (default: None)
        month (int or str) -- the publication month (default: None)
        day (int or str) -- the publication day (default: None)
        date_string (str) -- date (d.m.y or m.y) as string

    Methods:
        add_corpus(newspaper, corpus_csv) -- add a corpus in csv format to a
            NewspaperHeadlineCorpus object
    """

    def __init__(self, headline):
        self.headline = headline
        self.__overline = None
        self.__subline = None
        self.__all_lines = None
        self.__year = None
        self.__month = None
        self.__day = None
        self.__date_string = None

    @property
    def overline(self):
        return self.__overline

    @overline.setter
    def overline(self, value):
        self.__overline = value

    @property
    def subline(self):
        return self.__subline

    @subline.setter
    def subline(self, value):
        self.__subline = value

    @property
    def all_lines(self):
        self.__all_lines = self.headline
        if self.__overline:
            self.__all_lines = self.__overline + ' ' + self.__all_lines
        if self.__subline:
            self.__all_lines += (' ' + self.__subline)
        return self.__all_lines

    @property
    def date_string(self):
        """Get publication date as string.

        Return:
            '{day}.{month}.{year}' if day, month, year;
            '{month}.{year}' if month, year;
            None otherwise
        """
        d, m, y = self.__day, self.__month, self.year
        if (d and m and y):
            return f'{d}.{m}.{y}'
        elif (m and y):
            return f'{m}.{y}'

    @property
    def year(self):
        """Get or set year of the publication date.
        Setting the year will reconfigure date attribute automatically.
        """
        return self.__year

    @year.setter
    def year(self, value):
        self.__year = value

    @property
    def month(self):
        """Get or set month of the publication date.
        Setting the month will reconfigure date attribute automatically.
        """
        return self.__month

    @month.setter
    def month(self, value):
        self.__month = value

    @property
    def day(self):
        """Get or set day of the publication date.
        Setting the day will reconfigure date attribute automatically.
        """
        return self.__day

    @day.setter
    def day(self, value):
        self.__day = value


if __name__ == '__main__':
    NH = NewspaperHeadline('Test HL!')
    NH.subline = 'Hallo'
    print(NH.all_lines)
    NH.year = 2003
    NH.month = 8
    NH.day = 28
    print(NH.date_string)
