from tqdm import tqdm
import os


FILE = r'C:\Users\Chulabutrach\Documents\Coding\Projects\woonplaeparsar\data\raw_data\wikipedia\thai-wikipedia-corpus.csv'
OUTPUT_FILE = r'C:\Users\Chulabutrach\Documents\Coding\Projects\woonplaeparsar\data\raw_data\wikipedia\clean_thai_full.csv'
MAX_LENGTH = 50000
print('max length:', MAX_LENGTH)


if os.path.exists(OUTPUT_FILE):
    print("file exists")
    os.remove(OUTPUT_FILE)

with open(FILE, 'r', encoding='UTF-8') as f:
    with open(OUTPUT_FILE, 'a', encoding='utf-8') as g:
        count = -1
        for line in tqdm(f):
            clean_list = line.strip().split(',')
            clean_list = clean_list[1:]
            clean_str = ','.join(clean_list)
            if len(clean_str) > MAX_LENGTH:
                clean_str = clean_str[:MAX_LENGTH]

            # clean_str = '%20'.join(clean_str.split(' '))
            clean_str = clean_str.replace('"','').replace("'",'').replace('|','')
            clean = str(count) + '|' + clean_str + '\n'
            g.write(clean)
            count += 1