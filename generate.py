# Второй модуль проекта "Генератор текста"
# Генерация последовательности слов по модели
# Версия: 2.0
# Создано: Левашов Артём, МФТИ ФИВТ 790, 2018

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


def choose_first_word(seed, freq_model):
    """Выбирает первое слово в зависимости от seed"""
    if seed is None:
        return random.choice(list(freq_model.keys()))
    elif seed not in list(freq_model.keys()):
        raise KeyError('Такого слова нет в модели!')
    else:
        return seed


def output_file(output):
    """Определяет файл вывода или stdout"""
    if output is None:
        return sys.stdout
    else:
        try:
            return open(output, 'w')
        except OSError:
            print("Не удалось открыть файл!")


def close_output(file, output):
    """Закрывает файл, если вывод не в консоль"""
    if output is not None:
        file.close()


def generate_sequence(prev_word, model, output, length):
    """Создание и вывод сгенерированной последовстельности"""
    output.write(prev_word + ' ')
    for i in range(1, length):
        choice_list = list()
        if len(model[prev_word].items()) != 0:
            for word in model[prev_word].keys():
                choice_list.extend([word] * model[prev_word][word])
        else:
            break
        prev_word = random.choice(choice_list)
        output.write(prev_word + ' ')


if __name__ == "__main__":
    namespace = input_parser().parse_args(sys.argv[1:])
    # Загрузка модели из файла в формате JSON
    with open(namespace.model, 'r') as f:
        model = json.load(f)
    # Определяем первое слово последовательности
    firstWord = choose_first_word(namespace.seed, model)
    n = namespace.length
    # Фиксируем файл вывода
    f = output_file(namespace.output)
    # Генерирование текста с помощью выбора из всех последователей
    #   слова умноженных на частоту посредством random.choice
    generate_sequence(firstWord, model, f, namespace.length)
    close_output(f, namespace.output)
