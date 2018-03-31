Проект для код-ревью 1 : Генератор текста
=========================================

Программа анализирует входные (обущающие) тексты, создает на их основе модель,
в которой хранятся частоты встречаемых пар слов. Затем, на основе созданной модели
генерирует последовательность заданной длины.

Программа состоит из двух модулей: 
 - обучающий модель(train.py)
 - генерирующий текст (generate.py)
 
train.py - обучение генератора текста (создание модели)   
Принимаемые аргументы:   

    -h, --help            Показывает принимаемые аргументы и информацию о модуле
	--input-dir input.txt Путь к директории с текстами для обучения (поддердивается любой уровень вложенности).
    					  Если путь не передан, ввод осуществляется из sys.stdin   
	--model model.txt     (Обязательный) Путь к файлу, куда модуль сохранит модель    
	--lc                  Перед сохранением в модель, приведет все слова к нижнему регистру

generate.py - генерация последовательности слов заданной длины, начиная с переданного
слова по составленной ранее модели. Последовательность также может закончиться словом,
у которого не определено никакое следующее в модели   
Принимаемые аргументы:

	-h, --help           Показывает принимаемые аргументы и информацию о модуле
	--model model.txt    (Обязательный) Директория где сохранится модель
	--seed word          Начальное слово. Генерирует исключение, если такого слова нет в модели.
	--length n           (Обязательный) Длина генерируемой последовательности. Может быть сгенерирована
    					 последовательность меньше, если встретилось слово без последующих в модели.
	--output output.txt  Путь к файлу, куда сохранится результат работы программы. 
    					 Если не передан - вывод осуществляется в sys.stdout
						

Сделано: Левашов Артём, группа 790   
ФИВТ МФТИ 2018
