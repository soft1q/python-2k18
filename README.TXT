Обучение модели генератора
train.py [-h] [--input-dir input.txt] --model model.txt [--lc]

  --input-dir input.txt
                        Путь к тексту для обучения
  --model model.txt     Директория где сохранится модель
  --lc                  Приводит все слова к нижнему регистру

Генератор текста на основе данной модели
usage: generate.py [-h] --model model.txt [--seed word] --length n
                   [--output output.txt]

  --model model.txt    Директория где сохранится модель
  --seed word          Начальное слово
  --length n           Длина генерируемой последовательности
  --output output.txt  Файл для вывода сгенерированного текста
