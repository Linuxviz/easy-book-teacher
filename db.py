import psycopg2


def db_connect():
    # создание подключения
    conn = psycopg2.connect(dbname='pars_base', user='db_user',
                            password='1111', host='localhost')
    return conn


def do_with_db(query, conn):
    print(query)
    # создание элемента выполняющего инструкцию
    cursor = conn.cursor()
    # print("База данных подключена к SQLite")
    # выполнение команды
    cursor.execute(query)
    # завершение транзакции, тоесть логическое отделение всех команд в блок который должен быть
    # выполнен с соблюдением ACID
    conn.commit()
    # print("Запрос SQL выполнен")
    cursor.close()


def get_one_result_from_db(query, conn):
    print(query)
    res = 0
    cursor = conn.cursor()
    cursor.execute(query)
    conn.commit()
    res = cursor.fetchone()[0]
    cursor.close()
    return res


def get_one_line_from_db(query, conn):
    print(query)
    res = 0
    cursor = conn.cursor()
    cursor.execute(query)
    conn.commit()
    res = cursor.fetchall()[0]
    print('res', res)
    cursor.close()
    return res


def get_query_set_from_db(query, conn) -> dict:
    print(query)
    res = {}
    cursor = conn.cursor()
    cursor.execute(query)
    conn.commit()
    temp = cursor.fetchall()
    for raw in temp:
        res[raw[1]] = raw[0]
    cursor.close()
    return res


def create_and_init_db(conn):
    print('Инициализация таблиц')
    query = '''
               CREATE TABLE book (
               book_id SERIAL PRIMARY KEY,
               title VARCHAR(120) UNIQUE,
               number_all_words INTEGER,
               number_all_words_without_short INTEGER,
               number_uniq_words INTEGER
               );
                                    
               CREATE TABLE chapter (
               chapter_id SERIAL PRIMARY KEY,
               book INTEGER REFERENCES book (book_id),
               name VARCHAR(120) UNIQUE, 
               number_all_words INTEGER,
               number_all_words_without_short INTEGER,
               number_uniq_words INTEGER
               );
                                        
               CREATE TABLE common_word (
               common_word_id SERIAL PRIMARY KEY,
               origin VARCHAR(120) UNIQUE,
               translate VARCHAR(120) NULL,
               frequency INTEGER
               );
               
               CREATE TABLE word (
               word_id SERIAL PRIMARY KEY,
               origin VARCHAR(120) UNIQUE,
               translate VARCHAR(120) NULL,
               frequency INTEGER,
               count_shows INTEGER,
               correct_decisions REAL,
               rang INTEGER
               );

               CREATE TABLE word_chapter (
               word_chapter_id SERIAL PRIMARY KEY,
               word INTEGER REFERENCES word(word_id),
               chapter INTEGER REFERENCES chapter(chapter_id)
               );
               
               CREATE TABLE common_word_chapter (
               common_word_chapter_id SERIAL PRIMARY KEY,
               common_word INTEGER REFERENCES common_word(common_word_id),
               chapter INTEGER REFERENCES chapter(chapter_id)
               );
            '''
    do_with_db(query, conn)
    print('___________________________________________________________________')


def db_add_book(book_name, conn):
    query = f'''
             INSERT INTO book(
                             title,
                             number_all_words,
                             number_all_words_without_short,
                             number_uniq_words)
             VALUES ('{book_name}', 0, 0, 0);
             '''
    do_with_db(query, conn)


def db_get_book_id(book_name, conn):
    query = f''' 
                 SELECT temp.book_id
                 FROM book AS temp
                 WHERE temp.title = '{book_name}';
            '''
    res = get_one_result_from_db(query, conn)
    return res


def db_add_chapter(chapter_name, book_name, book_id, conn):
    query = f'''INSERT INTO chapter(
                                    book,
                                    name,
                                    number_all_words,
                                    number_all_words_without_short,
                                    number_uniq_words
                                    )
    VALUES ({book_id}, '{book_name}_{chapter_name}', 0, 0, 0);
    '''
    do_with_db(query, conn)


def db_set_chapter_count_all_and_uniq_words(count_chapter_words, count_chapter_uniq_words,
                                            conn, count_n_w, chapter_id):
    query = f'''
                UPDATE chapter 
                SET number_all_words = {count_chapter_words},
                    number_uniq_words = {count_chapter_uniq_words},
                    number_all_words_without_short = {count_n_w}
                WHERE chapter_id = {chapter_id}; 
             '''
    do_with_db(query, conn)


def db_get_count(table_name: str, conn) -> int:
    query = f'''
                 SELECT COUNT({table_name}_id)
                 FROM {table_name};
            '''
    return get_one_result_from_db(query, conn)


def db_get_words(table_name: str, offset: int, conn) -> dict:
    query = f'''
                     SELECT {table_name}_id, origin
                     FROM {table_name}
                     LIMIT 1001
                     OFFSET {offset};
                     '''
    return get_query_set_from_db(query, conn)


def db_add_words(words: dict, table, chapter_id, conn):
    """Принимает на вход словарь слово - частота, и пытается вставить в таблицу, если
    находит такое слово, обновляет частоту, если не находит возвращает слово и его id и частоту"""
    print('Вставка слов:')
    print('Слова:', words)
    print('Имя таблицы:', table)
    res_dict = {}
    query = ''
    additional_fields = ",count_shows,correct_decisions,rang"
    additional_fields_filling = ", 0, 0.0, 0"
    if table != 'word':
        additional_fields = ""
        additional_fields_filling = ""
    for origin in words:
        try:
            query = f'''
                        INSERT INTO {table} (origin,
                                          translate,
                                          frequency{additional_fields})
                        VALUES ('{origin}', Null, {words[origin]}{additional_fields_filling})  
                        ON CONFLICT (origin)
                        DO UPDATE SET frequency = {table}.frequency + {words[origin]}
                        RETURNING {table}.{table}_id, {table}.origin, {table}.translate;
                     '''
        except:
            print(f'----------------ERROR----------------------------------->"{origin}", "{words[origin]}"')
        temp = get_one_line_from_db(query, conn)
        print('temp', temp[2])
        if temp[2] is None:
            res_dict[temp[1]] = temp[0]
        query2 = f'''
                    INSERT INTO {table}_chapter(
                                                {table},
                                                chapter
                                                )
                    VALUES ({temp[0]}, {chapter_id});
                 '''
        do_with_db(query2, conn)
    return res_dict


def db_update_translate(words: dict[int, str], table_name: str, conn):
    query = []
    if table_name == 'word':
        for word in words:
            sql_query = f'''
                     UPDATE word
                     SET translate = '{words[word][1]}'
                     WHERE word.word_id = {words[word][0]};
                     '''
            query.append(sql_query)
    else:
        for word in words:
            sql_query = f'''
                            UPDATE common_word
                            SET translate = '{words[word][1]}'
                            WHERE common_word.common_word_id = {words[word][0]};  
                            '''
            query.append(sql_query)
    do_with_db(''.join(query), conn)


def db_get_chapter_id(book_name, chapter_name, conn):
    query = f'''
            SELECT chapter_id
            FROM chapter
            WHERE chapter.name = '{book_name}_{chapter_name}'; 
         '''
    return get_one_result_from_db(query, conn)


def db_update_book(book, conn):
    query = f'''
             WITH i(naw, nawws, nuq) AS 
                                    (SELECT  
                                            SUM(number_all_words) AS naw,
                                            SUM(number_all_words_without_short) AS nawws,
                                            SUM(number_uniq_words) AS nuq
                                     FROM chapter
                                     WHERE book = (SELECT book_id 
                                                   FROM book
                                                   WHERE title = '{book}'))
             UPDATE book
             SET number_all_words = book.number_all_words + i.naw,
                 number_all_words_without_short = book.number_all_words_without_short + i.nawws,
                 number_uniq_words = book.number_uniq_words + i.nuq
             FROM i
             WHERE title = '{book}';    
             '''
    do_with_db(query, conn)
