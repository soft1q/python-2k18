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
                        metavar='input.txt', help="Путь к тексту для обучения")
    parser.add_argument('--model', action='store',
                        required=True, metavar='model.txt',
                        help="Директория где сохранится модель")
    parser.add_argument('--lc', action='store_true', required=False,
                        help="Приводит все слова к нижнему регистру")
    return parser


def list_from_file(input_file):
    """Преобразовывает текст из данного файла к списку слов"""
    result_list = list()
    for line in input_file:
        result_list.extend(re.findall(r'[a-zA-Zа-яА-Я]+', line))
    return result_list


def list_from_directory(input_dir):
    """Преобразовывает все тексты из данной директории к списку слов"""
    result_list = list()
    for path, dirs, files in os.walk(input_dir):
        for filename in files:
            f = open(os.path.join(path, filename), 'r')
            for line in f:
                result_list.extend(re.findall(r'[a-zA-Zа-яА-Я]+', line))
    return result_list


def make_frequency_model(words_list):
    """Создает на основе списка слов модель \"пары - частоты\""""
    result_dict = defaultdict(lambda: defaultdict(int))
    for i in range(1, len(words_list)):
        result_dict[words_list[i-1]][words_list[i]] += 1
    return result_dict


# Парсинг аргументов консольной команды
namespace = input_parser().parse_args(sys.argv[1:])
# Составляем список слов
if namespace.input_dir is None:
    words = list_from_file(sys.stdin)
else:
    words = list_from_directory(namespace.input_dir)
# Переводим слова в нижний регистр, если нужно
if namespace.lc:
    words = ' '.join(words).lower().split()
# Словарь словарей, хранящий частоты пар
pairs_freq = make_frequency_model(words)
# Загрузка модели в формате JSON
f = open(namespace.model, 'w')
json.dump(pairs_freq, f, ensure_ascii=False)
f.close()
