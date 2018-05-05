'''
 Первый модуль проекта "Генератор текста"
 Обучение модели на заданных текстах
 Версия: 2.0
 Создано: Левашов Артём, МФТИ ФИВТ 790, 2018
'''

# coding: utf-8
import re
import json
import argparse
import sys
import os
from collections import defaultdict
from collections import Counter
from contextlib import contextmanager


def input_parser():
    """Создает парсер аргументов для вызова из консоли"""
    parser = argparse.ArgumentParser(description="Обучение генератора текста")
    parser.add_argument('--input-dir', action='store', required=False,
                        metavar='directory_nm', help="Путь к директории с "
                                                     "обучающими текстами")
    parser.add_argument('--model', action='store',
                        required=True, metavar='model.txt',
                        help="Путь к файлу, в который сохранится модель")
    parser.add_argument('--lc', action='store_true', required=False,
                        help="Приводит все слова к нижнему регистру")
    return parser


def count_bigrams(input_dir, lc):
    """Извлечь биграммы из файла в модель"""
    bigrams_counter = Counter()
    for input_file in get_input(input_dir):
        last_word = "_START_"
        for line in input_file:
            if lc:
                line = line.lower()
            tmp = re.findall(r'[a-zA-Zа-яА-Я]+', line)
            bigrams_counter[last_word, tmp[0]] += 1
            last_word = tmp[-1]
            for word1, word2 in zip(tmp[:-1], tmp[1:]):
                bigrams_counter[word1, word2] += 1
        bigrams_counter[last_word, "_END_"] += 1
    return bigrams_counter


def get_input(input_dir):
    if input_dir is None:
        yield sys.stdin
    for path, dirs, files in os.walk(input_dir):
        for file in files:
            f = open(os.path.join(path, file), 'r')
            yield f
            f.close()


def create_model(bigrams_counter):
    """Создание модели в виде словаря"""
    result_dict = defaultdict(lambda: defaultdict(int))
    for (word1, word2), frequency in bigrams_counter.items():
        if word1 != "_START_":
            if word2 == "_END_" and len(result_dict[word1].keys()) == 0:
                result_dict[word1] = {}
            else:
                result_dict[word1][word2] = frequency
    return result_dict


if __name__ == "__main__":
    # Парсинг аргументов консольной команды
    namespace = input_parser().parse_args(sys.argv[1:])
    # Создание счётчика биграмм
    bigrams = count_bigrams(namespace.input_dir, namespace.lc)
    # Перевод счётчика биграмм в словарь словарей
    pairs_freq = create_model(bigrams)
    # Загрузка модели в формате JSON
    with open(namespace.model, 'w') as f:
        json.dump(pairs_freq, f, ensure_ascii=False)
