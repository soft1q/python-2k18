# coding: utf-8
import json
import random
import argparse
import sys


def input_parser():
    """Создает парсер аргументов для вызова из консоли"""
    parser = argparse.ArgumentParser(description="Сгенерировать последовательность"
                                                 " слов заданной длины начиная с заданного слова")
    parser.add_argument('--model', action='store', required=True,
                        metavar='model.txt', help="Директория где сохранится модель")
    parser.add_argument('--seed', action='store', required=False,
                        metavar='word', help="Начальное слово")
    parser.add_argument('--length', action='store', required=True, metavar='n', type=int,
                        help="Длина генерируемой последовательности")
    parser.add_argument('--output', action='store', required=False, metavar='output.txt',
                        help="Файл для вывода сгенерированного текста")
    return parser


namespace = input_parser().parse_args(sys.argv[1:])
# Загрузка модели из файла в формате JSON
f = open(namespace.model, 'r')
model = json.load(f)
f.close()
# Входные данные - начальное слово и длина последовательности
if namespace.seed is None:
    prevWord = random.choice(list(model.keys()))
else:
    prevWord = namespace.seed
n = namespace.length
# Фиксируем файл вывода
if namespace.output is None:
    f = sys.stdout
else:
    f = open(namespace.output, 'w')
f.write(prevWord + ' ')
# Генерирование текста с помощью выбора из всех последователей
#   слова умноженных на частоту посредством random.choice
for i in range(1, n):
    choiceList = list()
    for word in model[prevWord].keys():
        choiceList.extend([word] * model[prevWord][word])
    random.shuffle(choiceList)
    prevWord = random.choice(choiceList)
    f.write(prevWord + ' ')
if namespace.output is not None:
    f.close()
