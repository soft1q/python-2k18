Проект для код-ревью 2 : Телеграм-бот
=========================================

Бот обучается на статьях из википедии или проектов .wikia, а затем способен анализировать данные и генерировать тексты на основе полученной модели.

Принимаемые форматы сообщений:
Ссылка на статью в википедии - https://ru.wikipedia.org/wiki/%D0%A2%D0%BE%D0%B4%D0%B8
Ссылка на статью в любом проекте .wikia - http://ru.marvel.wikia.com/wiki/%D0%9C%D1%8D%D1%82%D1%82%D1%8C%D1%8E_%D0%9C%D1%91%D1%80%D0%B4%D0%BE%D0%BA_(199999)
Название статьи на википедии - Тоди
Название .wikia и название статьи - marvel.wikia Мэттью Мёрдок (199999)
Также в конце указывается глубина поиска (по умолчанию 1) - максимальный уровень вложенности ссылок, по которым надо переходить.

Доступные команды:
 - /help - выводит доступные команды
 - /write N - генерирует последовательность слов длиной N
 - /top N (asc|desc) - показывает первые N самых часто(редко) встречающихся слов (по умолчанию asc - часто)
 - /stopwords - показывает слова в модели, частота которых на три отклонения больше или меньше средней
По умолчанию N = 10

Описание модулей:
 - text_generator - обучение модели + команда /write. Основано на прошлом ревью
 - wiki_parse.py - парсинг входных сообщений бота. Получение из ссылки названия, а также поиск всех вложенных ссылок.
 - statistics.py - обработка модели, связанная со статистикой. Основа команд /top и /stopwords
 - main_bot.py - основной скрипт с ботом. Создает обработчики команд, связывает их с функциями и запускает бота.
 
Отмечу, что документация кода и сам бот на английском, потому что я так начал, а исправлять уже поздно. Но для упрощения понимания этот README.md - на русском.

Сделано: Левашов Артём, группа 790   
ФИВТ МФТИ 2018