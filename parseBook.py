import re
import os


def parse(file_path: str, book_new_name):
    # сделать автоопределение имени книги
    if is_db_created():
        # сделать првоерку книги с таким именем
        db_add_book(book_new_name)
        if is_dir_created(book_new_name):
            pass
        else:
            book_dir_path = create_dir(book_new_name)
            parse_book(file_path, book_dir_path, book_new_name)
            analyze_chapters(book_dir_path)
    else:
        create_and_init_db()


def is_db_created():
    pass


def create_and_init_db():
    pass


def db_add_book(book_name):
    pass


def is_dir_created(book_name):
    pass


def create_dir(book_name) -> str:
    """
    Создает директорию для хранения глав книги
    :param book_name:
    :return book_name_path:
    """
    os.mkdir(book_name)
    return f"./{book_name}"


def parse_book(file_path: str, book_dir_path: str, book_name: str):
    """
    Разделяет файл по главам по закрывающему тегу секции и записывает полученные главы в отдельные файлы
    в директорию созданную для книги.
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
                chapter_name = f'Chapter_{chapter_number}'
                with open(f'{book_dir_path}/{chapter_name}.txt', 'w', encoding='utf-8') as sec:
                    sec.write(''.join(buffer))
                buffer = []
                db_add_chapter(chapter_name, book_name)
            line = re.sub('<[^>]*>', '', line)
            buffer.append(line)


def db_add_chapter(chapter_name, book_name):
    pass


def analyze_chapters(book_dir_path):
    for root, dirs, files in os.walk(f"./{book_dir_path}"):
        for file in files:
            analyze_chapter(file)


def analyze_chapter(file: str) -> dict:
    pass