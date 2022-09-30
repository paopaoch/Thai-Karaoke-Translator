import os
from bs4 import BeautifulSoup
import requests
from tqdm import tqdm

CURRENT_PATH = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(CURRENT_PATH, 'data')
WORD_FILE_NAME = os.path.join(DATA_PATH, 'word_list.txt')
OUTPUT_FILE_NAME = os.path.join(DATA_PATH, 'thai_karaoke.txt')
URL_PRE = r'https://th.wiktionary.org/wiki/'
TRUNCATE = True

if TRUNCATE == False:
    open_type = 'a+'
else:
    open_type = 'w+'

output_f = open(OUTPUT_FILE_NAME, open_type, encoding='utf-8')

with open(WORD_FILE_NAME, 'r', encoding='utf-8') as f:
    for item in tqdm(f):
        word = item.strip().replace(' ', '_')
        url = URL_PRE + word
        source = requests.get(url).text
        soup = BeautifulSoup(source, 'lxml')
        table_elem = soup.find('table')
        if table_elem is None:
            continue
        table_elem_list = table_elem.find_all('span', {'class':'tr'})
        if table_elem_list is None:
            continue
        if len(table_elem_list) >= 2:
            karaoke = table_elem_list[-1].text.strip().replace('-', '')
            found = True
        else:
            found = False
        
        if found:
            output_f.write(word.replace('_', ''))
            output_f.write('|')
            output_f.write(karaoke)
            output_f.write('\n')

output_f.close()