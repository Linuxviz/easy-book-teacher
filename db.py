import sqlite3


def create_and_init_db():
    print('Инициализация таблиц')
    query = '''
               CREATE TABLE book (
               book_id INTEGER PRIMARY KEY,
               title TEXT,
               number_all_words INTEGER,
               number_all_words_without_short INTEGER,
               number_uniq_words INTEGER
               );
                                    
               CREATE TABLE chapter (
               chapter_id INTEGER PRIMARY KEY,
               book INTEGER,
               name TEXT, 
               number_all_words INTEGER,
               number_all_words_without_short INTEGER,
               number_uniq_words INTEGER,
               FOREIGN KEY (book) REFERENCES book(book_id)
               );
                                        
               CREATE TABLE common_word (
               common_word_id INTEGER PRIMARY KEY,
               origin TEXT,
               translate TEXT,
               frequency INTEGER
               );
               
               CREATE TABLE word (
               word_id INTEGER PRIMARY KEY,
               origin TEXT,
               translate TEXT,
               frequency INTEGER,
               count_shows INTEGER,
               correct_decisions REAL,
               rang INTEGER
               );

               CREATE TABLE word_chapter (
               word_chapter_id INTEGER PRIMARY KEY,
               word INTEGER,
               chapter INTEGER,
               FOREIGN KEY (word) REFERENCES word(word_id),
               FOREIGN KEY (chapter) REFERENCES chapter(chapter_id)
               );
               
               CREATE TABLE common_word_chapter (
               common_word_chapter_id INTEGER PRIMARY KEY,
               common_word INTEGER,
               chapter INTEGER,
               FOREIGN KEY (common_word) REFERENCES word(common_word_id),
               FOREIGN KEY (chapter) REFERENCES chapter(chapter_id)
               );
            '''
    do_with_db(query)
    print('___________________________________________________________________')


def db_add_book(book_name):
    query = f'''
             INSERT INTO book(
                             title,
                             number_all_words,
                             number_all_words_without_short,
                             number_uniq_words)
             VALUES ('{book_name}', 0, 0, 0);
             '''
    do_with_db(query)


def db_get_book_id(book_name):
    query = f''' 
                 SELECT temp.book_id
                 FROM book AS temp
                 WHERE temp.title = '{book_name}';
            '''
    res = get_one_result_from_db(query)
    return res


def db_add_chapter(chapter_name, book_name, book_id):
    query = f'''INSERT INTO chapter(
                                    book,
                                    name,
                                    number_all_words,
                                    number_all_words_without_short,
                                    number_uniq_words
                                    )
    VALUES ({book_id}, '{book_name}_{chapter_name}', 0, 0, 0);
    '''
    do_with_db(query)


def db_set_chapter_count_all_and_uniq_words(count_chapter_words, count_chapter_uniq_words, chapter_name, book_name):
    query = f'''
                UPDATE chapter 
                SET number_all_words = {count_chapter_words},
                    number_uniq_words = {count_chapter_uniq_words}
                WHERE chapter.name = '{book_name}_{chapter_name}'; 
             '''
    do_with_db(query)


def db_get_count(table_name: str) -> int:
    query = f'''
                 SELECT COUNT({table_name}_id)
                 FROM {table_name};
            '''
    return get_one_result_from_db(query)


def db_get_words(table_name: str, offset: int) -> set:
    query = f'''
                     SELECT origin
                     FROM {table_name}
                     LIMIT 1001
                     OFFSET {offset};
                     '''
    return get_query_set_from_db(query)


def db_add_words(words: dict, table):
    query = []
    print(words)
    if table == 'word':
         for origin in words:
             try:
                 sql_query = f'''
                             INSERT INTO word(
                                              origin,
                                              translate,
                                              frequency,
                                              count_shows,
                                              correct_decisions,
                                              rang 
                                             )
                            VALUES ("{origin}","{words[origin][1]}",{words[origin][0]}, 0, 0.0, 0);   
                         '''
                 query.append(sql_query)
             except:
                 print(f'----------------ERROR----------------------------------->"{origin}", "{words[origin]}"')
         do_with_db(''.join(query))
    else:
        for origin in words:
            try:
                sql_query = f'''
                            INSERT INTO common_word(
                                             origin,
                                             translate,
                                             frequency
                                            )
                           VALUES ("{origin}","{words[origin][1]}",{words[origin][0]});   
                        '''
                query.append(sql_query)
            except:
                print(f'----------------ERROR----------------------------------->"{origin}", "{words[origin]}"')
        do_with_db(''.join(query))

def db_set_number_words_without_common_for_chapter(count_n_w, chapter_name, book_name):
    query = f'''
               UPDATE chapter 
               SET number_all_words_without_short = {count_n_w}
               WHERE chapter.name = '{book_name}_{chapter_name}'; 
            '''
    do_with_db(query)


def do_with_db(query):
    try:
        # создание подключения
        sqlite_connection = sqlite3.connect('sqlite_pars.db')
        # создание элемента выполняющего инструкцию
        cursor = sqlite_connection.cursor()
        # print("База данных подключена к SQLite")
        # выполнение команды
        cursor.executescript(query)
        # завершение транзакции, тоесть логическое отделение всех команд в блок который должен быть
        # выполнен с соблюдением ACID
        sqlite_connection.commit()
        #print("Запрос SQL выполнен")
        cursor.close()

    except sqlite3.Error as error:
        print("Ошибка при подключении к sqlite",query, error)

    finally:
        if sqlite_connection:
            sqlite_connection.close()
            # print("Соединение с SQLite закрыто")


def get_one_result_from_db(query):
    res = 0
    try:
        sqlite_connection = sqlite3.connect('sqlite_pars.db')
        cursor = sqlite_connection.cursor()
        #print("База данных подключена к SQLite")
        cursor.execute(query)
        sqlite_connection.commit()
        #print("Запрос SQL выполнен, запрос одного значения")
        res = cursor.fetchone()[0]
        cursor.close()

    except sqlite3.Error as error:
        print("Ошибка при подключении к sqlite",query, error)

    finally:
        if (sqlite_connection):
            sqlite_connection.close()
            # print("Соединение с SQLite закрыто")
    return res


def get_query_set_from_db(query):
    res = set()
    try:
        sqlite_connection = sqlite3.connect('sqlite_pars.db')
        cursor = sqlite_connection.cursor()
        # print("База данных подключена к SQLite")
        cursor.execute(query)
        sqlite_connection.commit()
        #print("Запрос SQL выполнен, взятие пачки слов")
        temp = cursor.fetchall()
        for raw in temp:
            res.add(raw[0])
        cursor.close()

    except sqlite3.Error as error:
        print("Ошибка при подключении к sqlite, при множественном запросе",query, error)

    finally:
        if (sqlite_connection):
            sqlite_connection.close()
            # print("Соединение с SQLite закрыто")
    print(res)
    return res


def db_update_frequency(word: str, frequency: int, table_name: str):
    query = f'''
             UPDATE {table_name}
             SET frequency = frequency + {frequency}
             WHERE {table_name}.origin = "{word}";
             '''
    do_with_db(query)
