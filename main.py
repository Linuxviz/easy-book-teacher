import re
from googletrans import Translator


def clearing_script(string: str):
    inter = 0
    with open(string, 'r', encoding='utf-8') as f:
        buffer = []
        for line in f:
            if "</section>" in line:
                inter += 1
                with open(f'Глава {inter}.txt', 'w', encoding='utf-8') as sec:
                    sec.write(''.join(buffer))
                buffer = []
            line = re.sub('<[^>]*>', '', line)
            buffer.append(line)


def counter(st: str):
    words = {}
    all_words_counter = 0
    with open(st, 'r', encoding='utf-8') as f:
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
    # for i, j in words:
    #     print(i, j)
    # print("Длинна всего текста:", all_words_counter, "слов")
    # print("Уникальных", len(words))
    return {i: j for i, j in words}


def clear_words(words: dict) -> dict:
    common_words = {'the', 'there', 'what', 'from',
                    'and', 'know', 'not', 'hagrid',
                    'was',
                    'his',
                    'that',
                    'dursley',
                    'had',
                    'dumbledore',
                    'have',
                    'all',
                    'said',
                    'but',
                    'professor',
                    'you',
                    'him',
                    'she',
                    'for',
                    'mcgonagall',
                    'were',
                    'they',
                    'out',
                    'mrs',
                    'people',
                    'didnt',
                    'her',
                    'cat',
                    'harry',
                    'very',
                    "them'",
                    'with',
                    'over',
                    'this',
                    'them',
                    }
    res = {}
    for i in words.keys():
        if len(i) > 2 and i not in common_words:
            res[i] = words[i]
    print(res)
    return res


def translate(words: dict) -> dict:
    """Принимает словарь с ключами в виде англ слов и значением - частотой употребления слов, возвращает
    словарь с теми же ключасми но в качестве значений кортеж частота, автоперевод"""
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


words = counter('Глава 5.txt')
words = translate(words)
print(words)
# unic_words = clear_words(words)
# print(unic_words)

# clearing_script('avidreaders.ru__harry-potter-and-the-sorcerer-s.txt')
# Нарезает книгу на главы по заголовку </section> И удаляет все содержимое тегов
