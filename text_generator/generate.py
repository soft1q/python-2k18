'''
 Второй модуль проекта "Генератор текста"
 Генерация последовательности слов по модели
 Версия: 2.0
 Создано: Левашов Артём, МФТИ ФИВТ 790, 2018
'''

# coding: utf-8
import json
import random


class NonPositiveLength(Exception):
    message = 'Given length is less or equals zero'


def generate_sequence(model_path, length):
    """Создание и вывод сгенерированной последовстельности"""
    if length <= 0:
        raise NonPositiveLength
    with open(model_path, 'r') as f:
        model = json.load(f)
    prev_word = random.choice([key for key in model.keys()])
    sequence = prev_word
    for i in range(1, length):
        if len(model[prev_word].items()) == 0:
            break
        choice_list = list()
        for word in model[prev_word].keys():
            choice_list.extend([word] * model[prev_word][word])
        prev_word = random.choice(choice_list)
        sequence = ' '.join([sequence, prev_word])
    return sequence
