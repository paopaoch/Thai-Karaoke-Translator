from rule_base_logic import separate_sentence, translate_thai_lexicon
from tqdm import tqdm

INPUT_FILE = r'C:\Users\Chulabutrach\Documents\Coding\Projects\woonplaeparsar\script_woon\scrapping_cleaning\scraping_from_pantip\pantip_comments.txt'
OUTPUT_FILE = r'C:\Users\Chulabutrach\Documents\Coding\Projects\woonplaeparsar\data\scraped_data\pantip_comments_karaoke.csv'

output = open(OUTPUT_FILE, 'w+', encoding='utf8')
count = 0
num_lines = 0
with open(INPUT_FILE, 'r', encoding='utf8') as f:
    for line in tqdm(f):
        num_lines += 1
        try:
            spaced_sentence = separate_sentence(line.strip())
            karaoke_translation = translate_thai_lexicon(spaced_sentence)
            if karaoke_translation != '':
                output.write(spaced_sentence)
                output.write('|')
                output.write(karaoke_translation)
                output.write('\n')
                count += 1
        except:
            pass

output.close()
print('number of lines in input: ', num_lines)
print('number of successful translations: ', count)