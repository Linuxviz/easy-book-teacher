import re
import os
from pathlib import Path
from db import *
from googletrans import Translator


def parse(file_path: str, book_new_name: str):
    # сделать автоопределение имени книги
    if is_db_created():
        # сделать првоерку книги с таким именем
        db_add_book(book_new_name)
        book_id = db_get_book_id(book_new_name)
        if is_dir_created(book_new_name):
            pass
        else:
            book_dir_path = create_dir(book_new_name)
            parse_book(file_path, book_dir_path, book_new_name, book_id)
            analyze_chapters(book_dir_path, book_new_name)
    else:
        create_and_init_db()


def is_db_created():
    return True


def is_dir_created(book_name):
    return False


def create_dir(book_name) -> str:
    """
    Создает директорию для хранения глав книги
    :param book_name:
    :return book_name_path:
    """
    os.mkdir(book_name)
    return f"./{book_name}"


def parse_book(file_path: str, book_dir_path: str, book_name: str, book_id: int):
    """
    Разделяет файл по главам по закрывающему тегу секции
    и записывает полученные главы в отдельные файлы
    в директорию созданную для книги.
    :param book_id:
    :param file_path:
    :param book_dir_path:
    :param book_name:
    :return:
    """
    chapter_number = 0
    with open(file_path, 'r', encoding='utf-8') as file:
        buffer = []
        for line in file:
            if "</section>" in line:
                chapter_number += 1
                chapter_name = f'chapter_{chapter_number}'
                with open(f'{book_dir_path}/{chapter_name}.txt', 'w', encoding='utf-8') as sec:
                    sec.write(''.join(buffer))
                buffer = []
                db_add_chapter(chapter_name, book_name, book_id)
            line = re.sub('<[^>]*>', '', line)
            buffer.append(line)


def analyze_chapters(book_dir_path: str, book_name: str):
    for root, dirs, files in os.walk(f"./{book_dir_path}"):
        for file in files:
            chapter_name = Path(file).stem
            count_chapter_words, count_chapter_uniq_words, chapter_words = analyze_chapter(file)
            db_set_chapter_count_all_and_uniq_words(count_chapter_words, count_chapter_uniq_words, chapter_name,
                                                    book_name)
            normal_words, common_words = decompose_words_into_groups(chapter_words)
            count_n_w = count_words_without_common(normal_words)
            db_set_number_words_without_common_for_chapter(count_n_w, chapter_name, book_name)
            process_group_of_words(normal_words, 'word', chapter_name)
            process_group_of_words(common_words, 'common_word', chapter_name)


def analyze_chapter(file: str) -> (int, int, dict):
    words = {}
    all_words_counter = 0
    with open(file, 'r', encoding='utf-8') as f:
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


def process_group_of_words(words, table_name, chapter_name):
    need_to_translate_words = {}
    count_words_in_db = db_get_count(table_name)
    for i in range(0, count_words_in_db, 1000):
        words_in_db = db_get_words(table_name, i)
        for word in words.keys():
            if word in words_in_db:
                db_update_frequency(word, words[word], table_name)
            else:
                need_to_translate_words[word] = words[word]
    translated_words = translate(need_to_translate_words)
    db_add_words(translated_words)


def translate(words: dict) -> dict[str: (int, str)]:
    """Принимает словарь с ключами в виде англ слов и значением - частотой употребления слов, возвращает
        словарь с теми же ключами но в качестве значений кортеж частота, автоперевод"""
    translator = Translator()
    translator.raise_Exception = True
    # используя генератор по ключам словаря создается список слов которые нужно перевести.
    list_words_for_translations = [i for i in words.keys()]
    # Монолитный список разбивается на группы по ззо слов, потому что у Gtrnlt есть лимит на 5k знаков.
    list_grouped_words = [list_words_for_translations[x:x + 330] for x in
                          range(0, len(list_words_for_translations), 330)]
    for group_words in list_grouped_words:
        # Добавляем кавычки к каждому слову иначе перевод будет некорректен, Gtrnlt постоянно слепляет слова.
        group_words_with_quotes = [f'"{i}"' for i in group_words]
        megastring = ';  '.join(group_words_with_quotes)
        result = translator.translate(text=megastring, src='en', dest='ru')
        # Разделяем переведенные слова и чистим их от кавычек
        pars_result_text = re.split(r'\;|\; |\; |\;', result.text.lower())
        pars_result_text = [re.sub(r'["«» ]', '', i) for i in pars_result_text]
        trans = dict(zip(group_words, pars_result_text))
        # заменяем значения на кортежи в исходном словаре
        for origin_word in trans:
            words[origin_word] = (words[origin_word], trans[origin_word])
    return words


def count_words_without_common(normal_words) -> int:
    count = 0
    for word in normal_words:
        count = count + normal_words[count]
    return count
