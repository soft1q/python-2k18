# coding: utf-8
import json
import random
import argparse
import sys


def input_parser():
    """Создает парсер аргументов для вызова из консоли"""
    desc = "Сгенерировать последовательность слов заданной длины, начиная с" \
           " заданного слова. Последовательность также может закончиться" \
           " словом, у которого не определено никакое следующее в модели"
    help_model = "Путь к файлу с сохраненной моделью"
    help_seed = "Начальное слово"
    help_length = "Длина генерируемой последовательности"
    help_output = "Файл для вывода сгенерированного текста"
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument('--model', action='store', required=True,
                        metavar='model.txt', help=help_model)
    parser.add_argument('--seed', action='store', required=False,
                        metavar='word', help=help_seed)
    parser.add_argument('--length', action='store', required=True, metavar='n',
                        type=int, help=help_length)
    parser.add_argument('--output', action='store', required=False,
                        metavar='output.txt', help=help_output)
    return parser


namespace = input_parser().parse_args(sys.argv[1:])
# Загрузка модели из файла в формате JSON
f = open(namespace.model, 'r')
model = json.load(f)
f.close()
# Фиксируем файл вывода
if namespace.output is None:
    f = sys.stdout
else:
    f = open(namespace.output, 'w')
# Входные данные - начальное слово и длина последовательности
if namespace.seed is None:
    prevWord = random.choice(list(model.keys()))
else:
    if namespace.seed not in list(model.keys()):
        raise KeyError('Такого слова нет в модели!')
    else:
        prevWord = namespace.seed
n = namespace.length
f.write(prevWord + ' ')
# Генерирование текста с помощью выбора из всех последователей
#   слова умноженных на частоту посредством random.choice
for i in range(1, n):
    choiceList = list()
    try:
        for word in model[prevWord].keys():
            choiceList.extend([word] * model[prevWord][word])
    except KeyError:
        break
    random.shuffle(choiceList)
    prevWord = random.choice(choiceList)
    f.write(prevWord + ' ')
if namespace.output is not None:
    f.close()
