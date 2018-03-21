import re
import json
import argparse
import sys


def input_parser():
    """Создает парсер аргументов для вызова из консоли"""
    parser = argparse.ArgumentParser(description="Обучение генератора текста")
    parser.add_argument('--input-dir', action='store', required=False,
                        metavar='input.txt', help="Путь к тексту для обучения")
    parser.add_argument('--model', action='store', required=True,
                        metavar='model.txt', help="Директория где сохранится модель")
    parser.add_argument('--lc', action='store_true', required=False, help="Приводит все слова к нижнему регистру")
    return parser


def list_from_input(input_file):
    """Преобразовывает входной текст к списку слов"""
    result_list = list()
    for line in input_file:
        result_list.extend(re.findall(r'\w+', line))
    if namespace.input_dir is not None:
        input_file.close()
    return result_list


def make_frequency_model(words_list):
    """Создает на основе списка слов модель \"пары - частоты\""""
    result_dict = dict()
    for i in range(1, len(words_list)):
        if namespace.lc:
            words_list[i] = words_list[i].lower()
        if words_list[i - 1] in result_dict.keys():
            if words_list[i] in result_dict[words_list[i - 1]]:
                result_dict[words_list[i - 1]][words_list[i]] += 1
            else:
                result_dict[words_list[i - 1]].update({words_list[i]: 1})
        else:
            result_dict.update({words_list[i - 1]: {words_list[i]: 1}})
    return result_dict


# Парсинг аргументов консольной команды
namespace = input_parser().parse_args(sys.argv[1:])
# Фиксируем файл ввода
if namespace.input_dir is None:
    f = sys.stdin
else:
    f = open(namespace.input_dir, 'r')
# Составление списка всех слов в тексте
words = list_from_input(f)
if namespace.input_dir is not None:
    f.close()
# Переводим слова в нижний регистр, если нужно
if namespace.lc:
    for word in words:
        word = word.lower()
# Словарь словарей, хранящий частоты пар
pairs_freq = make_frequency_model(words)
# Загрузка модели в формате JSON
f = open(namespace.model, 'w')
json.dump(pairs_freq, f, ensure_ascii=False)
f.close()
