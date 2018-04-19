# Первый модуль проекта "Генератор текста"
# Обучение модели на заданных текстах
# Версия: 2.0
# Создано: Левашов Артём, МФТИ ФИВТ 790, 2018

# coding: utf-8
import re
import json
import argparse
import sys
import os
from collections import defaultdict


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


def push_bigrams_from_file(result_dict, input_file, lc):
    """Извлечь биграммы из файла в модель"""
    for line in input_file:
        tmp = re.findall(r'[a-zA-Zа-яА-Я]+', line)
        for i, word in enumerate(tmp[:-1]):
            if lc:
                result_dict[word.lower()][tmp[i+1].lower()] += 1
            else:
                result_dict[word][tmp[i+1]] += 1


def create_model(result_dict, input_dir, lc):
    """Создание модели"""
    if input_dir is None:
        push_bigrams_from_file(result_dict, sys.stdin, lc)
    else:
        for path, dirs, files in os.walk(input_dir):
            for filename in files:
                f = open(os.path.join(path, filename), 'r')
                push_bigrams_from_file(result_dict, f, lc)


if __name__ == "__main__":
    # Парсинг аргументов консольной команды
    namespace = input_parser().parse_args(sys.argv[1:])
    # Словарь словарей, хранящий частоты пар
    pairs_freq = defaultdict(lambda: defaultdict(int))
    create_model(pairs_freq, namespace.input_dir, namespace.lc)
    # Загрузка модели в формате JSON
    with open(namespace.model, 'w') as f:
        json.dump(pairs_freq, f, ensure_ascii=False)
