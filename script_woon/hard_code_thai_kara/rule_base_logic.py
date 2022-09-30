""" script to translate thai language to karaoke using rule-based and lexicon """

import json
import os
from pythainlp import word_tokenize, Tokenizer
from radnhar import float_to_thai

""" import all lexicon and dictionary. all files will be placed in the same as this script """
CURRENT_PATH = os.path.dirname(os.path.abspath(__file__))

# Load lexicon
with open(CURRENT_PATH + r'\lexicon.json', encoding='utf8') as lexicon_file:
    LEXICON = json.load(lexicon_file)

# Load thai alphabet
with open(CURRENT_PATH + r'\thai_alphabet.json', encoding='utf8') as thai_alpha_file:
    ALPHABET_DICT = json.load(thai_alpha_file)

# Load thai vowels
with open(CURRENT_PATH + r'\vowels.json', encoding='utf8') as vowels_file:
    VOWELS_DICT = json.load(vowels_file)

LETTERS_DICT = {**ALPHABET_DICT, **VOWELS_DICT}

# Load thai sounds
with open(CURRENT_PATH + r'\sounds.csv', 'r', encoding='utf8') as sounds_file:
    SOUNDS = [item.rstrip() for item in sounds_file]

# Load emoji
with open(CURRENT_PATH + r'\emojis.txt', 'r', encoding='utf8') as emojis_file:
    EMOJIS = [item.rstrip() for item in emojis_file]

# Load english alphabet
with open(CURRENT_PATH + r'\english_alphabet.csv', 'r', encoding='utf8') as english_alpha_file:
    ENGLISH_ALPHABET = [item.rstrip() for item in english_alpha_file]

# Load emoji
with open(CURRENT_PATH + r'\emojis.txt', 'r', encoding='utf8') as emojis_file:
    EMOJIS = [item.rstrip() for item in emojis_file]

# Load symbols
with open(CURRENT_PATH + r'\symbols.txt', 'r', encoding='utf8') as symbols_file:
    SYMBOLS = [item.rstrip() for item in symbols_file]

UNWANTED = EMOJIS + SYMBOLS

""" Remove sounds from thai words because sounds cannot be shown in karaoke """


def remove_sound(text):
    for sound in SOUNDS:
        text = text.replace(sound, '')

    return text


""" translate thai to karaoke using rule-based logic """


def translate_thai(thai_input):

    oh_no_numbers = False

    sara_ae = False
    sara_ai = False
    sara_oh = False
    sara_ua = False
    sara_ao = False
    sara_o = False
    sara_aee = False
    sara_er = False

    translate_output_list = list()

    # remove sound
    thai_input = remove_sound(thai_input)

    # separate string into two dimensional array
    word_array = thai_input.strip().split()
    for i in range(len(word_array)):
        word = word_array[i]
        if word.isnumeric():
            oh_no_numbers = True
            if '.' in word:
                word = float(word)
            else:
                word = int(word)
            translate_output_list.append([float_to_thai(word)])

        else:
            oh_no_numbers = False
        word_array[i] = list(word_array[i])
        translate_word_list = list()
        counter = 0

        for j in range(len(word_array[i])):
            letter = word_array[i][j]
            if letter in ('1', '2', '3', '4', '5', '6', '7', '8', '9', '0'):
                oh_no_numbers = True
                continue
            if letter in ENGLISH_ALPHABET:
                translate_word_list.append(letter)

            if letter in LETTERS_DICT:  # replace main letters
                if letter == 'ว' and sara_ua == True:
                    sara_ua = False
                elif letter == 'ญ' and len(word_array[i]) >= 2:
                    if word_array[i][j-1] == 'ั':
                        translate_word_list.append('n')
                else:
                    translate_word_list.append(LETTERS_DICT[letter])

            if letter == 'ๆ':
                previous_word = ''.join(translate_output_list[-1])
                translate_word_list.append(previous_word)

            # สระ โ ะ
            if len(word_array[i]) == 2 and word_array[i][0] in ALPHABET_DICT and word_array[i][1] in ALPHABET_DICT:
                if sara_o == True:
                    sara_o = False
                else:
                    translate_word_list.append('o')
                    sara_o = True

            # สระ ะ
            if letter == 'ะ':
                if word_array[i][j-1] == 'า':
                    pass
                elif len(word_array[i]) >= 3:
                    if word_array[i][j-2] != 'โ':
                        translate_word_list.append('a')
                else:
                    translate_word_list.append('a')

            if letter == 'ิ':
                if sara_er == True:
                    translate_word_list.append('er')
                    sara_er = False
                else:
                    translate_word_list.append('i')

            # สระ า และ เ า
            if letter == 'า':
                if sara_ao == True:
                    sara_ao = False
                elif j == len(word_array[i]) - 1:
                    translate_word_list.append('ar')
                elif word_array[i][j+1] == 'ย':
                    translate_word_list.append('ai')
                elif word_array[i][j+1] in LETTERS_DICT:
                    translate_word_list.append('a')

            # ไม้หันอากาศและสระ  ัว
            if letter == 'ั':
                if len(word_array[i]) > j + 1:
                    if word_array[i][j+1] == 'ว':
                        translate_word_list.append('ua')
                        sara_ua = True
                    else:
                        translate_word_list.append('u')
                else:
                    translate_word_list.append('u')

            # words like เป็น เด็ด
            if letter == '็' and j >= 2:
                if word_array[i][j-2] != 'เ':
                    translate_word_list.append('or')

            # สระ แ
            if sara_aee == True:
                translate_word_list.append('ae')
                sara_aee = False

            # สระ เ
            if sara_ae == True:
                translate_word_list.append('e')
                sara_ae = False

            # สระ ไ
            if sara_ai == True:
                translate_word_list.append('ai')
                sara_ai = False

            # สระ โ
            if sara_oh == True:
                translate_word_list.append('o')
                sara_oh = False

            if sara_ao == True:
                if len(word_array[i]) > j + 2:
                    if word_array[i][j+2] == 'ะ':
                        translate_word_list.append('or')
                    else:
                        translate_word_list.append('ao')
                else:
                    translate_word_list.append('ao')

            if letter == 'แ':
                sara_aee = True

            if letter == 'ใ' or letter == 'ไ':
                sara_ai = True

            # สระ เ และ เ า
            if letter == 'เ':
                if len(word_array[i]) - counter >= 3:
                    if word_array[i][j+2] == 'า':
                        sara_ao = True
                    else:
                        sara_ae = True
                elif len(word_array[i]) - counter >= 3:
                    if word_array[i][j+2] == 'ิ':
                        sara_er = True
                    else:
                        sara_ae = True
                elif len(word_array[i]) - counter >= 4:
                    if word_array[i][j+3] == 'ิ':
                        sara_er = True
                    else:
                        sara_ae = True
                else:
                    sara_ae = True

            if letter == 'โ':
                sara_oh = True

            # ตัวการันต์
            if letter == '์':
                translate_word_list = translate_word_list[:-1]

            counter += 1

        translate_output_list.append(translate_word_list)

    for i in range(len(translate_output_list)):
        translate_output_list[i] = ''.join(translate_output_list[i])

    translate_output = ' '.join(translate_output_list)
    return translate_output


""" Translate using lexicon and rule-base logic """


def translate_thai_lexicon(text):
    text_list = text.split()

    for word in text_list:
        if word in LEXICON:
            text = text.replace(word, LEXICON[word])

    text = translate_thai(text)
    return text


def remove_unwanted(text):
    output = text
    for letter in UNWANTED:
        output = output.replace(letter, '')
    output = output.replace('ๆ', '  ๆ')
    return output

def separate_sentence(text):
    text_list = word_tokenize(remove_unwanted(text))
    valueToBeRemoved = ''
    try:
        for i in range(len(text_list)):
            text_list[i] = text_list[i].replace(' ','')
        while True:
            text_list.remove(valueToBeRemoved)
    except ValueError:
        pass
    return ' '.join(text_list)

if __name__ == '__main__':
    string = 'hello my friend'
    string_1 = 'กะ ให้ เขา เป็น คน หัว โบราณ'
    string_2 = 'อาจ จะ อยาก รู้ สเป็ก ของ น้อง จัง เลย ครับ'
    string_3 = 'เวลา เห็น คน ทำ อะไร แล้ว อยาก ทำ ตาม'
    string_4 = 'เวลา จะ สัก ให้ เป็น ก็ ไม่ มี หาย ไป ทำ ยัง ไง ดี'
    string_5 = 'ยูมิโกะ เป็น คน ที่ หน้า ตา ดี ที่ สุด ใน โลก และ เป็น คน ดี มาก มาก'
    string_6 = 'แฟน เก่า ผม ชื่อ แพรว ซึ่ง เป็น คน ไม่ เพรียบ พร้อม'
    string_7 = 'ผม เป็น คน เกิด ปี มะเส็ง ชอบ กิน เงาะ'
    string_8 = 'ผม ต้อง พา แม่ ไป โรงพยาบาล'
    string_9 = 'ไป หา หมอ นวบุตร'
    string_10 = 'ไง เนเน่ ไป นอน ได้ แล้ว'
    string_11 = 'สวัสดีครับ ประยุทธ์ จันทร์โอชา'
    string_12 = 'เจาะ หู มัน เจ็บ นะ - เปาเปา'
    string_13 = 'เจาะหูมันเจ็บนะเปาเปา'

    some_str = separate_sentence(input("some thai string: "))
    print("spacing: ", some_str)
    print("karaoke translation: ", translate_thai_lexicon(some_str))

    # string_list = [string, string_1, string_2, string_3, string_4, string_5, string_6, string_7, string_8, string_9, string_10, string_11, string_12, separate_sentence(string_13)]

    # for item in string_list:
    #     print(item)
    #     print(translate_thai_lexicon(item), '\n')
