""" В этом файле содержится скрипт для парсинга и внесения в базу данных
 на локальной машине словаря в формате XML"""

from xml.etree import ElementTree
import psycopg2
import re

tree = ElementTree.parse('dict.xdxf')
root = tree.getroot()
en_ru = dict()
for word in root.findall('ar'):
    key = re.sub(r"""^\s+|\n|'|"|\r|\s+$""", '', word.find('k').text)
    if word.find('tr') is None:
        main_body = re.sub(r"""^\s+|\n|'|"|\r|\s+$""", '', word.find('k').tail)
        en_ru[key] = {'translation': main_body}
    else:
        transcription = word.find('tr').text
        main_body = re.sub(r"""^\s+|\n|\r|'|"|\s+$""", '', word.find('tr').tail)
        en_ru[key] = {'translation': main_body, 'transcription': transcription}


def db_connect(en_ru: dict):
    try:
        # создание подключения
        conn = psycopg2.connect(dbname='en_ru', user='db_user',
                                password='1111', host='localhost')
        cursor = conn.cursor()
        for key in en_ru:
            temp = en_ru[key].get('transcription')
            if temp is not None:
                query = f'''
                         INSERT INTO en_ru(
                                         origin,
                                         transcription,
                                         translation,
                                         full_info)
                         VALUES ('{key}', '{temp}', NULL, '{en_ru[key]['translation']}');
                         '''
            else:
                query = f'''
                         INSERT INTO en_ru(
                                         origin,
                                         transcription,
                                         translation,
                                         full_info)
                         VALUES ('{key}', NULL, NULL, '{en_ru[key]['translation']}');
                         '''
            try:
                cursor.execute(query)
            except psycopg2.Error as err:
                print(err, query, key)
            conn.commit()
        cursor.close()
        conn.close()
    finally:
        conn.close()

