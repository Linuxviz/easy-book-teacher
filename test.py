from db import do_with_db
import re
from googletrans import Translator


test_data = {'train':          2955, 'platform': 2958, 'hogwarts': 2970, 'twins': 2976, 'scabbers': 2988, 'fred': 2992,
             'compartment':    3002, 'trunk': 3009, 'barrier': 3017, 'george': 3018, 'toad': 3021, 'hermione': 3023,
             'wizard':         3037, 'wand': 3038, 'rons': 3042, 'malfoy': 3048, 'hedwig': 3052, 'threequarters': 3058,
             'cart':           3064, 'platforms': 3066, 'percy': 3069, 'pale': 3081, 'frogs': 3086, 'goyle': 3087,
             'station':        3094, 'wizards': 3096, 'girl': 3101, 'crowd': 3103, 'brothers': 3121, 'card': 3123,
             'side':           3124, 'firs': 3125, 'castle': 3126, 'boats': 3127, 'many': 3130, 'kings': 3133,
             'cross':          3134, 'show': 3135, 'magic': 3137, 'guard': 3149, 'money': 3153, 'diagon': 3155,
             'alley':          3156, 'sort': 3167, 'loads': 3176, 'flavor': 3180, 'neville': 3183, 'scared': 3185,
             'interesting':    3189, 'need': 3194, 'lift': 3196, 'ticket': 3197, 'idea': 3209, 'packed': 3213,
             'plump':          3214, 'ginny': 3218, 'oldest': 3219, 'youngest': 3227, 'freckles': 3228, 'lost': 3232,
             'haired':         3234, 'followed': 3235, 'please': 3236, 'added': 3242, 'hang': 3247, 'prefect': 3249,
             'blown':          3250, 'clambered': 3252, 'weasleys': 3258, 'wizarding': 3259, 'names': 3262,
             'fields':         3266, 'corridor': 3267, 'sandwiches': 3268, 'beans': 3269, 'pasty': 3270,
             'unwrapped':      3271, 'eating': 3272, 'toadless': 3281, 'granger': 3284, 'gringotts': 3286, 'says': 3287,
             'draco':          3288, 'cliff': 3291, 'pleased': 3298, 'nervous': 3313, 'talked': 3317, 'plastic': 3320,
             'laughing':       3323, 'looks': 3325, 'part': 3327, 'tapping': 3330, 'third': 3331, 'pushing': 3339,
             'joking':         3345, 'brother': 3346, 'excuse': 3348, 'worry': 3354, 'students': 3366, 'hanging': 3367,
             'faced':          3368, 'hairy': 3370, 'steps': 3371, 'leaned': 3377, 'sounded': 3379, 'send': 3381,
             'houses':         3384, 'weasley': 3387, 'charlie': 3391, 'quidditch': 3392, 'percys': 3393,
             'others':         3394, 'bills': 3395, 'charlies': 3396, 'ears': 3398, 'afford': 3400, 'youknowwhos': 3404,
             'learn':          3406, 'quick': 3409, 'pockets': 3414, 'mars': 3415, 'bars': 3416, 'botts': 3417,
             'pumpkin':        3418, 'pasties': 3419, 'cakes': 3420, 'share': 3423, 'agrippa': 3425, 'cards': 3426,
             'witches':        3427, 'frog': 3428, 'picture': 3430, 'modern': 3433, 'dragons': 3435, 'morgana': 3439,
             'bean':           3440, 'grass': 3441, 'spell': 3443, 'nevilles': 3446, 'teeth': 3447, 'magical': 3453,
             'gryffindor':     3454, 'ravenclaw': 3455, 'crabbe': 3460, 'unless': 3462, 'follow': 3472, 'narrow': 3473,
             'path':           3474, 'lake': 3475, 'fleet': 3476, 'smooth': 3477, 'journey': 3478, 'quarters': 3479,
             'himin':          3483, 'terrified': 3485, 'acted': 3487, 'improvement': 3490, 'depressing': 3493,
             'history':        3496, 'magichis': 3497, 'vacuum': 3501, 'anymore': 3502, 'mice': 3504, 'ticked': 3505,
             'pinned':         3508, 'august': 3512, 'quiz': 3514, 'eruncle': 3517, 'toto': 3518, 'grunt': 3519,
             'carpets':        3524, 'punctures': 3525, 'realizing': 3526, 'rubbish': 3528, 'barking': 3529,
             'bother':         3530, 'friendly': 3531, 'hospital': 3532, 'growled': 3533, 'ruddy': 3534,
             'removed':        3535, 'goes': 3536, 'excited': 3540, 'jeans': 3541, 'robeshed': 3542, 'checked': 3543,
             'list':           3544, 'cage': 3547, 'paced': 3548, 'loaded': 3550, 'dumped': 3551, 'wheeled': 3552,
             'facing':         3554, 'nineplatform': 3557, 'built': 3559, 'term': 3560, 'nastier': 3561,
             'attract':        3566, 'annoyed': 3571, 'desperate': 3573, 'strode': 3574, 'muttering': 3575,
             'wasters':        3576, 'panic': 3578, 'according': 3579, 'arrivals': 3581, 'board': 3582,
             'stranded':       3583, 'inspectors': 3585, 'speaker': 3589, 'flaming': 3590, 'himand': 3592,
             'piped':          3594, 'headed': 3596, 'marched': 3597, 'blink': 3598, 'itbut': 3600, 'dividing': 3601,
             'tourists':       3602, 'swarming': 3603, 'backpack': 3604, 'tellim': 3607, 'gonebut': 3608,
             'briskly':        3610, 'thereand': 3611, 'hello': 3613, 'sons': 3614, 'gangling': 3616, 'isthe': 3617,
             'erokay':         3622, 'trolley': 3623, 'solid': 3624, 'jostled': 3625, 'smash': 3626,
             'troubleleaning': 3627, 'broke': 3628, 'runthe': 3629, 'nearerhe': 3630, 'stopthe': 3631,
             'controlhe':      3632, 'awayhe': 3633, 'scarlet': 3635, 'steam': 3636, 'express': 3638, 'wrought': 3639,
             'archway':        3641, 'threequarterson': 3642, 'smoke': 3643, 'drifted': 3644, 'chattering': 3645,
             'color':          3647, 'wound': 3648, 'hooted': 3650, 'disgruntled': 3651, 'babble': 3652,
             'scraping':       3653, 'trunks': 3654, 'carriages': 3655, 'seats': 3656, 'search': 3657, 'gran': 3658,
             'nevillehe':      3659, 'sigh': 3660, 'dreadlocks': 3661, 'surrounded': 3662, 'lifted': 3664,
             'shrieked':       3666, 'poked': 3667, 'shove': 3669, 'heave': 3670, 'raise': 3671, 'dropped': 3672,
             'painfully':      3673, 'panted': 3674, 'cmere': 3675, 'sweaty': 3677, 'blimey': 3678, 'arent': 3679,
             'potterchorused': 3680, 'gawked': 3681, 'floating': 3684, 'trains': 3685, 'hopped': 3686, 'jerk': 3690,
             'rubbing':        3692, 'momgeroff': 3693, 'wriggled': 3694, 'aaah': 3696, 'ronnie': 3697,
             'somefink':       3698, 'nosie': 3699, 'striding': 3701, 'billowing': 3703, 'badge': 3706, 'chest': 3707,
             'prefects':       3708, 'compartments': 3709, 'themselves': 3710, 'prefectpercy': 3711,
             'prefectsaid':    3714, 'fondly': 3715, 'termsend': 3716, 'twothis': 3719, 'behave': 3721,
             'yourselves':     3722, 'youveyouve': 3724, 'funnyand': 3725, 'ronniekins': 3726, 'safe': 3727,
             'rubbed':         3728, 'girls': 3729, 'goggle': 3731, 'therelike': 3732, 'dearno': 3733, 'wonder': 3734,
             'polite':         3736, 'remembers': 3737, 'became': 3738, 'forbid': 3740, 'needs': 3741,
             'reminding':      3742, 'whistle': 3743, 'waving': 3746, 'crying': 3747, 'gathered': 3748, 'speed': 3749,
             'disappear':      3751, 'rounded': 3752, 'flashed': 3753, 'excitement': 3755, 'redheaded': 3756,
             'glanced':        3759, 'mark': 3761, 'trainlee': 3763, 'jordans': 3764, 'tarantula': 3766,
             'introduce':      3768, 'ourselves': 3769, 'blurted': 3770, 'georges': 3771, 'jokes': 3772, 'gotyou': 3773,
             'eagerly':        3776, 'welli': 3777, 'moments': 3779, 'moms': 3782, 'accountant': 3784,
             'horriblewell':   3786, 'wish': 3787, 'sixth': 3790, 'leftbill': 3792, 'captain': 3793, 'mess': 3794,
             'marks':          3795, 'thinks': 3796, 'expects': 3797, 'deal': 3798, 'useless': 3800, 'wakes': 3801,
             'affi':           3803, 'namesaid': 3814, 'impressed': 3817, 'braveor': 3818, 'voicing': 3820,
             'cows':           3827, 'sheep': 3828, 'lanes': 3829, 'flick': 3830, 'clattering': 3831, 'dimpled': 3833,
             'dears':          3834, 'candy': 3836, 'rattling': 3837, 'carrybut': 3839, 'bettie': 3840,
             'droobles':       3841, 'cauldron': 3843, 'licorice': 3844, 'wands': 3845, 'wanting': 3847, 'miss': 3848,
             'paid':           3849, 'sickles': 3850, 'bronze': 3851, 'knuts': 3852, 'tipped': 3853, 'starving': 3855,
             'bite':           3856, 'forgets': 3861, 'corned': 3862, 'beef': 3863, 'swap': 3864, 'indeed': 3866,
             'candies':        3868, 'reallyfrogs': 3870, 'knowchocolate': 3873, 'collectfamous': 3874, 'hundred': 3875,
             'ptolemy':        3876, 'halfmoon': 3880, 'flowing': 3883, 'thisis': 3886, 'agrippathanks': 3887,
             'currently':      3888, 'headmaster': 3889, 'considered': 3890, 'particularly': 3892, 'defeat': 3893,
             'grindelwald':    3894, '1945': 3895, 'discovery': 3896, 'uses': 3897, 'blood': 3898, 'alchemy': 3899,
             'partner':        3900, 'nicolas': 3901, 'flamel': 3902, 'enjoys': 3904, 'chamber': 3905, 'music': 3906,
             'tenpin':         3907, 'bowling': 3908, 'astonishment': 3909, 'strayed': 3912, 'pile': 3913,
             'photos':         3914, 'amazed': 3915, 'weird': 3916, 'sidled': 3917, 'interested': 3918, 'hengist': 3919,
             'woodcroft':      3920, 'alberic': 3921, 'grunnion': 3922, 'circe': 3923, 'paracelsus': 3924,
             'merlin':         3925, 'tore': 3926, 'druidess': 3927, 'cliodna': 3928, 'bertie': 3930, 'warned': 3931,
             'meanevery':      3932, 'flavoryou': 3933, 'ordinary': 3934, 'ones': 3935, 'peppermint': 3936,
             'spinach':        3938, 'liver': 3939, 'tripe': 3940, 'reckons': 3941, 'boogerflavored': 3942,
             'bleaaarghsee':   3944, 'sprouts': 3945, 'coconut': 3947, 'baked': 3948, 'strawberry': 3949, 'curry': 3950,
             'coffee':         3951, 'sardine': 3952, 'brave': 3953, 'nibble': 3954, 'touch': 3955, 'pepper': 3956,
             'countryside':    3957, 'becoming': 3959, 'wilder': 3960, 'woods': 3962, 'twisting': 3963, 'rivers': 3964,
             'hills':          3965, 'tearful': 3967, 'keeps': 3969, 'bothered': 3971, 'snoozing': 3973,
             'rummaged':       3978, 'battered': 3979, 'chipped': 3980, 'glinting': 3983, 'unicorn': 3984,
             'hairs':          3985, 'poking': 3986, 'bossy': 3988, 'lets': 3992, 'aback': 3993, 'erall': 3994,
             'sunshine':       3995, 'daisies': 3996, 'butter': 3997, 'mellow': 3998, 'simple': 4001, 'spells': 4002,
             'familys':        4005, 'witchcraft': 4006, 'heardive': 4007, 'enoughim': 4008, 'stunned': 4010,
             'coursei':        4011, 'extra': 4012, 'background': 4013, 'historyand': 4014, 'rise': 4015,
             'artsand':        4017, 'events': 4018, 'twentieth': 4019, 'century': 4020, 'dazed': 4021,
             'goodness':       4022, 'sounds': 4024, 'shes': 4026, 'spellgeorge': 4028, 'gloom': 4029, 'settling': 4030,
             'wouldbe':        4032, 'slytherin': 4034, 'flopped': 4036, 'depressed': 4037, 'ends': 4038,
             'whiskers':       4039, 'romania': 4044, 'studying': 4045, 'africa': 4046, 'daily': 4047,
             'prophetbut':     4048, 'mugglessomeone': 4049, 'security': 4050, 'vault': 4051, 'mustve': 4052,
             'powerful':       4053, 'happens': 4054, 'prickle': 4055, 'mentioned': 4057, 'entering': 4058,
             'team':           4061, 'confessed': 4062, 'dumbfounded': 4063, 'explaining': 4064, 'positions': 4066,
             'players':        4067, 'describing': 4068, 'broomstick': 4070, 'points': 4072, 'recognized': 4074,
             'malkins':        4076, 'robe': 4077, 'interest': 4079, 'shown': 4080, 'thickset': 4082, 'extremely': 4083,
             'bodyguards':     4085, 'carelessly': 4086, 'slight': 4088, 'cough': 4089, 'snigget': 4091,
             'children':       4092, 'coolly': 4099, 'tinge': 4100, 'cheeks': 4102, 'politer': 4104, 'riffraff': 4105,
             'bravely':        4109, 'ronron': 4113, 'yell': 4116, 'finger': 4117, 'sunk': 4119, 'goyles': 4120,
             'knucklecrabbe':  4121, 'flew': 4123, 'rats': 4124, 'lurking': 4125, 'among': 4126, 'footsteps': 4127,
             'hasbeen':        4128, 'picking': 4130, 'ithes': 4132, 'bewitched': 4136, 'doesnt': 4137, 'malfoys': 4138,
             'conductor':      4139, 'scowling': 4141, 'righti': 4142, 'childishly': 4144, 'corridors': 4146,
             'sniffy':         4147, 'dirt': 4148, 'glared': 4149, 'mountains': 4151, 'forests': 4152, 'slowing': 4154,
             'jackets':        4155, 'sneakers': 4157, 'echoed': 4158, 'luggage': 4161, 'separately': 4162,
             'lurched':        4164, 'nerves': 4165, 'crammed': 4166, 'joined': 4167, 'thronging': 4168, 'slowed': 4169,
             'familiar':       4174, 'beamed': 4175, 'cmon': 4176, 'meany': 4177, 'stumbling': 4180, 'steep': 4181,
             'trees':          4183, 'losing': 4184, 'bend': 4187, 'loud': 4188, 'oooooh': 4189, 'atop': 4192,
             'mountain':       4193, 'starry': 4196, 'turrets': 4198, 'towers': 4199, 'moren': 4200, 'shore': 4202,
             'thenforward':    4204, 'gliding': 4206, 'towered': 4210, 'sailed': 4211, 'curtain': 4213, 'opening': 4215,
             'tunnel':         4217, 'harbor': 4219, 'rocks': 4220, 'pebbles': 4221, 'climbed': 4223, 'trevor': 4224,
             'blissfully':     4226, 'passageway': 4227, 'shadow': 4230, 'flight': 4231, 'fist': 4235}


# def translate(words: dict) -> dict[str: (int, str)]:
#     print(words)
#     """Принимает словарь с ключами в виде англ слов и значением - частотой употребления слов, возвращает
#         словарь с теми же ключами но в качестве значений кортеж частота, автоперевод"""
#     print("перевод слов")
#     translator = Translator()
#     translator.raise_Exception = True
#     # используя генератор по ключам словаря создается список слов которые нужно перевести.
#     list_words_for_translations = [i for i in words.keys()]
#     # Монолитный список разбивается на группы по ззо слов, потому что у Gtrnlt есть лимит на 5k знаков.
#     list_grouped_words = [list_words_for_translations[x:x + 150] for x in
#                           range(0, len(list_words_for_translations), 150)]
#     for group_words in list_grouped_words:
#         # Добавляем кавычки к каждому слову иначе перевод будет некорректен, Gtrnlt постоянно слепляет слова.
#         group_words_with_quotes = [f'"{i}"' for i in group_words]
#         megastring = ';  '.join(group_words_with_quotes)
#         result = translator.translate(text=megastring, src='en', dest='ru')
#         print(result)
#         # Разделяем переведенные слова и чистим их от кавычек
#         pars_result_text = re.split(r';', result.text.lower())
#         pars_result_text = [re.sub(r'["«»]', '', i).strip() for i in pars_result_text]
#         trans = dict(zip(group_words, pars_result_text))
#         # заменяем значения на кортежи в исходном словаре
#         for origin_word in trans:
#             words[origin_word] = (words[origin_word], trans[origin_word])
#     return words

def translate(words: dict) -> dict[str: (int, str)]:
    print(words)
    """Принимает словарь с ключами в виде англ слов и значением - частотой употребления слов, возвращает
        словарь с теми же ключами но в качестве значений кортеж частота, автоперевод"""
    print("перевод слов")
    translator = Translator()
    translator.raise_Exception = True
    # используя генератор по ключам словаря создается список слов которые нужно перевести.
    list_words_for_translations = [i for i in words.keys()]
    # Монолитный список разбивается на группы по ззо слов, потому что у Gtrnlt есть лимит на 5k знаков.
    list_grouped_words = [list_words_for_translations[iot:iot + 150] for iot in
                          range(0, len(list_words_for_translations), 150)]
    for group_words in list_grouped_words:
        # Добавляем кавычки к каждому слову иначе перевод будет некорректен, Gtrnlt постоянно слепляет слова.
        group_words_with_quotes = [f'[{i}]' for i in group_words]
        megastring = ';.'.join(group_words_with_quotes)
        result = translator.translate(text=megastring, src='en', dest='ru')
        print(result)
        # Разделяем переведенные слова и чистим их от кавычек
        pars_result_text = re.findall(r'\[(.*?)]', result.text)
        print(pars_result_text)
        print(result.origin)
        pars_result_text = re.split(r';.', result.text.lower())
        pars_result_text = [re.sub(r'["«»]', '', i).strip() for i in pars_result_text]
        trans = dict(zip(group_words, pars_result_text))
        # заменяем значения на кортежи в исходном словаре
        for origin_word in trans:
            words[origin_word] = (words[origin_word], trans[origin_word])
    return words

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


print(test_data)
x = translate(test_data)