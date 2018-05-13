'''
 Statistics module on project "Telegram Bot"
 Count all statistic properties of model
 Version: beto 1.0
 Creator: Levashov Artem, MIPT DIHT 790, 2018
'''

from numpy import mean, std
from collections import OrderedDict
from text_generator.generate import NonPositiveLength
import json


class NonDefinedOrder(Exception):
    message = 'Cannot define given order expression'


class PreCountStat:
    '''Class for saving ordered frequency dict, middle value and dispersion'''
    def __init__(self, path):
        with open(path, 'r') as f:
            stats = json.load(f)
        values = [i for i in stats.values()]
        self.mean_freq = int(mean(values))
        self.dev = int(std(values))
        self.ordered_stats = OrderedDict(sorted(stats.items(),
                                                key=lambda t: t[1]))

    def find_top(self, n, order):
        '''Finds top n words which are close enough to middle frequency'''
        if n <= 0:
            raise NonPositiveLength
        if order != 'asc' and order != 'desc':
            raise NonDefinedOrder
        if order == 'asc':
            # Reordering dict if its needed
            ordered_stats = OrderedDict(sorted(self.ordered_stats.items(),
                                               key=lambda t: t[1],
                                               reverse=True))
        else:
            ordered_stats = self.ordered_stats
        result = {}
        # Choose suitable words
        for word, freq in ordered_stats.items():
            if self.mean_freq + 3 * self.dev > freq > self.mean_freq - 3 * self.dev:
                result.update({word: freq})
                n -= 1
            if n == 0:
                break
        return result

    def stop_words(self):
        '''Find stop words which are far enough from middle frequency'''
        result = {}
        for word, freq in self.ordered_stats.items():
            if self.mean_freq + 3 * self.dev < freq or \
                    freq < self.mean_freq - 3 * self.dev:
                result.update({word: freq})
        return result
