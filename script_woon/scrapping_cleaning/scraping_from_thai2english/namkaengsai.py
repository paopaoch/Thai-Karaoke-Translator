# coding=utf-8

from bs4 import BeautifulSoup
import pandas as pd
import os
from time import sleep
import requests
from tqdm import tqdm

data={
    'thai': [],
    'karaoke': []
}

CURRENT_PATH = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = r'C:\Users\Chulabutrach\Documents\Coding\Projects\woonplaeparsar\data\raw_data\wikipedia\clean_thai.csv'
WEBSITE_URL = 'https://www.thai2english.com/?q='    
COMPLETE_NAME = r'C:\Users\Chulabutrach\Documents\Coding\Projects\woonplaeparsar\data\scraped_data\thai_karaoke.csv'
CHANGE_LETTERS = (
    ('é','e')
    ,('ê','e')
    ,('è','e')
    ,('ĕ','e')
    ,('ă','a')
    ,('â','a')
    ,('á','a')
    ,('à','a')
    ,('û','u')
    ,('ŭ','u')
    ,('ú','u')
    ,('ù','u')
    ,('ò','o')
    ,('ŏ','o')
    ,('ó','o')
    ,('ô','o')
    ,('î','i')
    ,('í','i')
    ,('ì','i')
    ,('ĭ','i')

    ,('-','')
    ,('·','')
    ,('bp','p') # ป
    ,('dt','t') # ต
    ,('aai','ai') # าย เช่น ชาย, บาย
    ,('aa','ar') # า
    ,('ii','i')

    ,('ก', 'gor')
    ,('ข', 'kor')
    ,('ฃ', 'kor')
    ,('ค', 'kor')
    ,('ฅ', 'kor')
    ,('ฆ', 'kor')
    ,('ง', 'ngor')
    ,('จ', 'jor')
    ,('ฉ', 'chor')
    ,('ช', 'chor')
    ,('ซ', 'sor')
    ,('ฌ', 'chor')
    ,('ญ', 'yor')
    ,('ฎ', 'dor')
    ,('ฏ', 'tor')
    ,('ฐ', 'tor')
    ,('ฑ', 'tor')
    ,('ฒ', 'tor')
    ,('ณ', 'nor')
    ,('ด', 'dor')
    ,('ต', 'tor')
    ,('ถ', 'tor')
    ,('ท', 'tor')
    ,('ธ', 'tor')
    ,('น', 'nor')
    ,('บ', 'bor')
    ,('ป', 'bor')
    ,('ผ', 'por')
    ,('ฝ', 'for')
    ,('พ', 'por')
    ,('ฟ', 'for')
    ,('ภ', 'por')
    ,('ม', 'mor')
    ,('ย', 'yor')
    ,('ร', 'ror')
    ,('ล', 'lor')
    ,('ว', 'wor')
    ,('ศ', 'sor')
    ,('ษ', 'sor')
    ,('ส', 'sor')
    ,('ห', 'hor')
    ,('ฬ', 'lor')
    ,('อ', 'or')
    ,('ฮ', 'hor')
    ,('ฯ', '')

)

def clean_text(some_text):
    for item in CHANGE_LETTERS:
        some_text = some_text.replace(item[0], item[1])
    return some_text

# LOAD IN DATA AS DATAFRAME AND PUT TEXTS TO LIST
df = pd.read_csv(DATA_FILE, sep='|')
texts = df['text'].tolist()

count = 0
for text in tqdm(texts):
    count += 1
    try:
        text = '%20'.join(text.split())
        url = WEBSITE_URL + text

        source = requests.get(url).text

        soup = BeautifulSoup(source, 'lxml')
        thai_words = soup.find('div', class_='thai-line').text
        thai_words = ' '.join(thai_words.replace('·','').split())

        tlit_words = soup.find('div', class_='tlit-line').text
        tlit_words = ' '.join(clean_text(tlit_words).split()) 

        data['thai'].append(thai_words)
        data['karaoke'].append(tlit_words)
    except:
        print('there was an error at itteration', count)
        pass

df_output = pd.DataFrame(data=data)
df_output.to_csv(COMPLETE_NAME, sep='|', index=False)