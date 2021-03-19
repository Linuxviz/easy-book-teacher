import sqlite3


def do_with_db(query):
    try:
        # создание подключения
        sqlite_connection = sqlite3.connect('sqlite_python.db')
        # создание элемента выполняющего инструкцию
        cursor = sqlite_connection.cursor()
        print("База данных подключена к SQLite")
        # выполнение команды
        cursor.execute(query)
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

do_with_db(sqlite_create_book_table_query)
do_with_db(sqlite_create_chapter_table_query)
do_with_db(sqlite_create_common_word_table_query)
do_with_db(sqlite_create_word_chapter_table_query)
do_with_db(sqlite_insert_book_query)
