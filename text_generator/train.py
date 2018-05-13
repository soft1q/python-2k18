'''
 Первый модуль проекта "Генератор текста"
 Обучение модели на заданных текстах
 Версия: 2.0
 Создано: Левашов Артём, МФТИ ФИВТ 790, 2018
'''

# coding: utf-8
import re
import json
import warnings
import os
from collections import Counter, defaultdict


start_word = "_START_"
end_word = "_END_"


def count_bigrams_and_words(article, max_depth):
    """Извлечь биграммы из файла в модель"""
    bigrams_counter = Counter()
    words_counter = Counter()
    for text in article.linked_articles(max_depth):
        last_word = start_word
        for line in text:
            tmp = re.findall(r'[a-zA-Zа-яА-Я]+', line)
            if not tmp:
                continue
            words_counter.update(tmp)
            bigrams_counter[last_word, tmp[0]] += 1
            last_word = tmp[-1]
            bigrams_counter.update(zip(tmp[:-1], tmp[1:]))
        bigrams_counter[last_word, end_word] += 1
    return bigrams_counter, words_counter


def create_model(bigrams_counter):
    """Создание модели в виде словаря"""
    result_dict = defaultdict(lambda: defaultdict(int))
    for (word1, word2), frequency in bigrams_counter.items():
        if word1 != start_word:
            if word2 == end_word and len(result_dict[word1].keys()) == 0:
                result_dict[word1] = {}
            else:
                result_dict[word1][word2] = frequency
    return result_dict


def train_model(article, max_depth, path, user):
    '''Main function - training users model on given article'''
    # Создание счётчика биграмм
    warnings.simplefilter("ignore")
    bigrams, words_stat = count_bigrams_and_words(article, max_depth)
    warnings.simplefilter("always")
    # Перевод счётчика биграмм в словарь словарей
    pairs_freq = create_model(bigrams)
    # Загрузка модели в формате JSON
    user_model = '{}_model.txt'.format(user)
    user_stats = '{}_stats.txt'.format(user)
    with open(os.path.join(path, user_model), 'w') as f:
        json.dump(pairs_freq, f, ensure_ascii=False)
    with open(os.path.join(path, user_stats), 'w') as f:
        json.dump(words_stat, f, ensure_ascii=False)
