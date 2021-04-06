import re
import os
from pathlib import Path
from db import *
from googletrans import Translator


def parse(file_path: str, book_new_name: str):
    try:
        conn = db_connect()
        # сделать автоопределение имени книги
        if not is_db_created():
            create_and_init_db(conn)
        # сделать првоерку книги с таким именем
        db_add_book(book_new_name, conn)
        book_id = db_get_book_id(book_new_name, conn)
        if not is_dir_created(book_new_name):
            book_dir_path = create_dir(book_new_name)
        else:
            book_dir_path = f"./{book_new_name}"
        parse_book(file_path, book_dir_path, book_new_name, book_id, conn)
        analyze_chapters(book_dir_path, book_new_name, conn)

    except psycopg2.Error as error:
        print("Ошибка при подключении к sqlite", error)

    finally:
        if conn:
            conn.close()


def is_db_created():
    files = os.listdir()
    if 'sqlite_pars.db' in files:
        return True
    else:
        return False


def is_dir_created(book_name):
    files = os.listdir()
    if book_name in files:
        return True
    else:
        return False


def create_dir(book_name) -> str:
    """
    Создает директорию для хранения глав книги
    :param book_name:
    :return book_name_path:
    """
    os.mkdir(book_name)
    return f"./{book_name}"


def parse_book(file_path: str, book_dir_path: str, book_name: str, book_id: int, conn):
    """
    Разделяет файл по главам по закрывающему тегу секции
    и записывает полученные главы в отдельные файлы
    в директорию созданную для книги.
    :param conn:
    :param book_id:
    :param file_path:
    :param book_dir_path:
    :param book_name:
    :return:
    """
    chapter_number = 0
    with open(file_path, 'r', encoding='utf-8') as file:
        print(file_path)
        buffer = []
        for line in file:
            if "</section>" in line:
                chapter_number += 1
                chapter_name = f'chapter_{chapter_number}'
                with open(f'{book_dir_path}/{chapter_name}.txt', 'w', encoding='utf-8') as sec:
                    sec.write(''.join(buffer))
                buffer = []
                db_add_chapter(chapter_name, book_name, book_id, conn)
            line = re.sub('<[^>]*>', '', line)
            buffer.append(line)


def analyze_chapters(book_dir_path: str, book_name: str, conn):
    for root, dirs, files in os.walk(f"./{book_dir_path}"):
        for file in files:
            print(f'обработка {file}')
            chapter_name = Path(file).stem
            count_chapter_words, count_chapter_uniq_words, chapter_words = analyze_chapter(f"{book_dir_path}/{file}")
            normal_words, common_words = decompose_words_into_groups(chapter_words)
            count_n_w = count_words_without_common(normal_words)
            chapter_id = db_get_chapter_id(book_name, chapter_name, conn)
            db_set_chapter_count_all_and_uniq_words(count_chapter_words, count_chapter_uniq_words, conn, count_n_w,
                                                    chapter_id)
            print('Начало обработки группы обычных слов главы:', file)
            process_group_of_words(normal_words, 'word', chapter_id, conn)
            print(normal_words)
            print('Конец обработки группы обычных слов главы:', file)
            print('Начало обработки группы частых слов главы:', file)
            process_group_of_words(common_words, 'common_word', chapter_id, conn)
            print(common_words)
            print('Конец обработки группы частых слов главы:', file)
    db_update_book(book_name, conn)


def analyze_chapter(file: str) -> (int, int, dict):
    words = {}
    all_words_counter = 0
    with open(file, 'r', encoding='utf-8') as f:
        print(file)
        for line in f:
            ws = re.sub(r'[^a-zA-Z0-9 \n]|\.', '', line.lower())
            x = ws.split()
            all_words_counter += len(x)
            for word in x:
                if word in words:
                    words[word] = words[word] + 1
                else:
                    words[word] = 1
    words = sorted(words.items(), key=lambda item: -item[1])
    return all_words_counter, len(words), {i: j for i, j in words}


def decompose_words_into_groups(chapter_words: dict) -> (dict, dict):
    common_words = {}
    normal_words = {}
    for word in chapter_words:
        if len(word) <= 3 or chapter_words[word] > 100:
            common_words[word] = chapter_words[word]
        else:
            normal_words[word] = chapter_words[word]
    return normal_words, common_words


def process_group_of_words(words, table_name, chapter_id, conn):
    # Принять словарь слово -> частота
    # Внести в таблицу без конфликата(если есть то просто обновить частоты)
    # Вернуть id origin translate, если translate пустой == Null или none? Занести на перевод
    # Перевести
    # Обновить перевод, частота уже внесена.
    need_to_translate_words = db_add_words(words, table_name, chapter_id, conn)
    translated_words = translate(need_to_translate_words)
    db_update_translate(translated_words, table_name, conn)


def translate(words: dict) -> dict[str: (int, str)]:
    print(words)
    """Принимает словарь с ключами в виде англ слов и значением - частотой употребления слов, возвращает
        словарь с теми же ключами но в качестве значений кортеж частота, автоперевод"""
    print("перевод слов")
    translator = Translator()
    translator.raise_Exception = True
    # используя генератор по ключам словаря создается список слов которые нужно перевести.
    list_words_for_translations = [i for i in words.keys() if i not in ('oooooh', 'toadless')]
    # Монолитный список разбивается на группы по ззо слов, потому что у Gtrnlt есть лимит на 5k знаков.
    list_grouped_words = [list_words_for_translations[x:x + 320] for x in
                          range(0, len(list_words_for_translations), 320)]
    for group_words in list_grouped_words:
        # Добавляем кавычки к каждому слову иначе перевод будет некорректен, Gtrnlt постоянно слепляет слова.
        group_words_with_quotes = [f'"{i}"' for i in group_words]
        megastring = ';  '.join(group_words_with_quotes)
        result = translator.translate(text=megastring, src='en', dest='ru')
        # Разделяем переведенные слова и чистим их от кавычек
        pars_result_text = re.split(r';', result.text.lower())
        pars_result_text = [re.sub(r'["«»]', '', i).strip() for i in pars_result_text]
        trans = dict(zip(group_words, pars_result_text))
        # заменяем значения на кортежи в исходном словаре
        for origin_word in trans:
            words[origin_word] = (words[origin_word], trans[origin_word])
    return words


def count_words_without_common(normal_words) -> int:
    count = 0
    for word in normal_words:
        count = count + normal_words[word]
    return count


parse('Book.txt', 'Гарри Поттер')
