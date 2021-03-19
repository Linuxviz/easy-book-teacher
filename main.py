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
    #print("Длинна всего текста:", all_words_counter, "слов")
    #print("Уникальных", len(words))
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


def translate(words):
    translator = Translator()
    translator.raise_Exception = True
    z = [i for i in words.keys()]
    one_string_words = [z[x:x + 330] for x in range(0, len(z), 330)]
    print(one_string_words)
    print(len(one_string_words))
    for megaword in one_string_words:
        megaword = [f'"{i}"' for i in megaword]
        megaword = ';  '.join(megaword)
        # print(megaword)
        result = translator.translate(text=megaword, src='en', dest='ru')
        # print(result.text)
        pars_result_text = re.split(r'\;|\; |\; |\;', result.text.lower())
        pars_result_text = [re.sub(r'"|«|»| ', '', i) for i in pars_result_text]
        # result.text.lower().split('. ')
        # print('-----')
        print('количество переведенных слов:', len(pars_result_text))
        # print(pars_result_text)
        pars_result_origin = result.origin.lower().split(';  ')
        pars_result_origin = [re.sub(r'"|«|»| ', '', i) for i in pars_result_origin]
        # print('-----')
        print('количество оригинальных слов:', len(pars_result_origin))
        # print(pars_result_origin)
        trans = dict(zip(pars_result_origin, pars_result_text))
        # print(result.text)
        for origin_word in trans:
            words[origin_word] = (words[origin_word], trans[origin_word])
    #print(words)
    return words



words = counter('Глава 5.txt')
# print(words)
words = translate(words)
print(words)
# unic_words = clear_words(words)
# print(unic_words)

# clearing_script('avidreaders.ru__harry-potter-and-the-sorcerer-s.txt')
# Нарезает книгу на главы по заголовку </section> И удаляет все содержимое тегов