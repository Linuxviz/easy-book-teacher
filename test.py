def translate(words: dict) -> dict[str: (int, str)]:
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
        pars_result_text = [re.sub(r'["«»]', '', i) for i in pars_result_text]
        trans = dict(zip(group_words, pars_result_text))
        # заменяем значения на кортежи в исходном словаре
        for origin_word in trans:
            words[origin_word] = (words[origin_word], trans[origin_word])
    return words