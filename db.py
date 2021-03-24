import sqlite3
from main import words


def do_with_db(query):
    try:
        # создание подключения
        sqlite_connection = sqlite3.connect('sqlite_python.db')
        # создание элемента выполняющего инструкцию
        cursor = sqlite_connection.cursor()
        print("База данных подключена к SQLite")
        # выполнение команды
        cursor.executescript(query)
        # завершение транзакции, тоесть логическое отделение всех команд в блок который должен быть
        # выполнен с соблюдением ACID
        sqlite_connection.commit()
        print("Запрос SQL выполнен")
        cursor.close()

    except sqlite3.Error as error:
        print("Ошибка при подключении к sqlite", error)

    finally:
        if (sqlite_connection):
            sqlite_connection.close()
            print("Соединение с SQLite закрыто")


sqlite_create_book_table_query = '''
                                CREATE TABLE book (
                                book_id INTEGER PRIMARY KEY,
                                about TEXT NULL,
                                number_all_words INTEGER NULL,
                                number_all_words_without_short INTEGER NULL,
                                number_uniq_words INTEGER NULL
                                );
                                '''

sqlite_create_chapter_table_query = '''
                                CREATE TABLE chapter (
                                chapter_id INTEGER PRIMARY KEY,
                                book INTEGER NOT NULL,
                                number_all_words INTEGER NULL,
                                number_all_words_without_short INTEGER NULL,
                                number_uniq_words INTEGER NULL,
                                FOREIGN KEY (book) REFERENCES book(book_id)
                                );
                                    '''

sqlite_create_common_word_table_query = '''
                                        CREATE TABLE common_word (
                                        common_word_id INTEGER PRIMARY KEY,
                                        origin TEXT NOT NULL,
                                        chapter INTEGER,
                                        FOREIGN KEY (chapter) REFERENCES chapter(chapter_id)
                                        );
                                        '''

sqlite_create_word_table_query = '''
                                        CREATE TABLE word (
                                        word_id INTEGER PRIMARY KEY,
                                        origin TEXT NOT NULL,
                                        translate TEXT NULL,
                                        frequency INTEGER NULL,
                                        count_shows INTEGER NULL,
                                        correct_decisions REAL NULL,
                                        rang INTEGER NULL
                                        );
                                        '''

sqlite_create_word_chapter_table_query = '''
                                            CREATE TABLE word_chapter (
                                            word_chapter_id INTEGER PRIMARY KEY,
                                            word INTEGER,
                                            chapter INTEGER,
                                            FOREIGN KEY (word) REFERENCES word(word_id),
                                            FOREIGN KEY (chapter) REFERENCES chapter(chapter_id)
                                            );
                                         '''

sqlite_insert_book_query = '''
                            INSERT INTO book(
                                            about,
                                            number_all_words,
                                            number_all_words_without_short,
                                            number_uniq_words)
                            VALUES ('Гарри Поттер и филосовский камень',Null,Null,Null)
                            '''


def sql_insert_word_command_str(origin, translate, frequency) -> str:
    if translate == '':
        translate = 'Null'
    else:
        translate = f'"{translate}"'
    return f'''
            INSERT INTO word(
                        origin,
                        translate,
                        frequency,
                        count_shows,
                        correct_decisions,
                        rang  
            )
            VALUES ("{origin}",{translate},{frequency},0,0,0);
            '''


def sql_insert_chapter_command_str(book, number_all_words, number_all_words_without_short, number_uniq_words,
                                   name) -> str:
    return f'''
    INSERT INTO chapter(
                        book,
                        number_all_words,
                        number_all_words_without_short,
                        number_uniq_words,
                        name
                        )
    VALUES ({book},{number_all_words},{number_all_words_without_short},{number_uniq_words},"{name}");   
           '''


def sql_insert_dict_words_command_str(words: dict, chapter_name: str, book_id: int) -> str:
    sql_command_list = [sql_insert_chapter_command_str(book_id, 0, 0, 0, chapter_name)]
    for word in words:
        sql_command_list.append(sql_insert_word_command_str(word, words[word][1], words[word][0]))
    return ''.join(sql_command_list)

# query = sql_insert_chapter_command_str(1, 0, 0, 0, 'x')
# query = sql_insert_dict_words_command_str(words)
# print(query)
# do_with_db(query)
