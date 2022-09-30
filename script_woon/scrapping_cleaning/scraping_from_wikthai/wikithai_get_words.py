from bs4 import BeautifulSoup
import os
import requests
from time import time


CURRENT_PATH = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(CURRENT_PATH, 'data')
WORD_FILE_NAME = os.path.join(DATA_PATH, 'word_list.txt')

FIRST_WEBSITE_URL = r'https://th.wiktionary.org/wiki/พิเศษ:หน้าทั้งหมด?from=ก&to=&namespace=0'
URL_PRE = r'https://th.wiktionary.org/wiki/พิเศษ:หน้าทั้งหมด?from='
URL_POST = r'to=&namespace=0'
WHILE_CHECK = True

TRUNCATE = True

start = time()

if TRUNCATE == False:
    open_type = 'a+'
else:
    open_type = 'w+'

f = open(WORD_FILE_NAME, open_type, encoding='utf-8')

url = FIRST_WEBSITE_URL
count = 0
while WHILE_CHECK:
    source = requests.get(url).text
    soup = BeautifulSoup(source, 'lxml')

    find_list = soup.find_all('li')
    find_list = find_list[:-25]

    for item in find_list:
        f.write(item.text)
        f.write('\n')
        if item.text == 'ไฮ้':
            WHILE_CHECK = False
            break

    # Set new URL
    next_page_name = soup.find('div', class_='mw-allpages-nav').text
    new_text = next_page_name.split('หน้าถัดไป')[1].replace('(', '').replace(')', '').strip()
    url = URL_PRE + new_text + URL_POST
    print(new_text)
    if count == 10:
        print('Time: ', time() -  start)
        count = 0
    else:
        count += 1
f.close()
