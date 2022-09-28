import os
import re
import cleaner_utils as ut
from pathlib import Path
from tqdm import tqdm 

def process_raw(in_file, out_path):

    config = ut.config(section='cleaner')
    
    file_name = os.path.basename(in_file)
    file_name = file_name.split('.')[0]
    save_path = f'{out_path}/{file_name}_processed.txt'
    
    if not os.path.isdir(out_path):
        os.mkdir(out_path)

    filter_regex_url = re.compile("https?:\\/\\/(?:www\\.)?[-a-zA-Z0-9@:%._\\+~#=]{1,256}\\.[a-zA-Z0-9()]{1,6}\\b(?:[-a-zA-Z0-9()@:%_\\+.~#?&\\/=]*)")
    #filter_regex_tag = re.compile('\[.*\]')
    filter_regex_tag = re.compile('\[deleted\]|\[removed\]')
    filter_regex_quote = re.compile('^> .*$')    
    filter_regex_newline = re.compile('\n')
    filter_regex_separator = re.compile('[\(\)\{\}\[\]?!.,;:\'"“^”«»~’`®\<\>\+*_]')

    stopword_array = []
    with open('italian_stopwords.txt', 'r', encoding="utf8") as stopwords:        
        stopword_list = stopwords.readlines()
        for stopword in stopword_list:
            stopword = filter_regex_newline.sub('', stopword)
            stopword_array.append(stopword.upper())

    count_row_lines = 0
    count_row_words = 0
    count_clean_lines = 0
    count_clean_words = 0

    with open(in_file, 'r', encoding="utf8") as in_file:        
        data = in_file.readlines()
        count_row_lines = len(data)
        with open(save_path, 'w+', encoding='utf8') as fp:
            for line in data:
                raw_splitted_line = line.split()
                count_row_words += len(raw_splitted_line)

                line = filter_regex_quote.sub('', line)
                line = filter_regex_url.sub('', line)
                line = filter_regex_tag.sub('', line)
                line = filter_regex_newline.sub('', line)
                line = filter_regex_separator.sub(' ', line)
                splitted_line = line.split()
                if len(splitted_line):
                    splitted_line[0] = splitted_line[0].lower()
                splitted_line = [i for i in splitted_line if i.upper() not in stopword_array]
                if len(splitted_line) >= int(config['min_word_in_line']):                
                    count_clean_lines += 1
                    count_clean_words += len(splitted_line)
                    fp.write(' '.join(splitted_line) + '\n')
    
    return [count_row_lines, count_row_words, count_clean_lines, count_clean_words]

def join_files(in_dir, out_path, file_name):
    files = [str(x) for x in Path(f'{in_dir}').glob('**/*.txt')]
    
    if os.path.isfile(f"{out_path}/{file_name}.txt"):
        os.remove(f"{out_path}/{file_name}.txt")
    
    with open(f"{out_path}/{file_name}_joined.txt", 'w+', encoding="utf8") as out_file:
        for path in tqdm(files):
            with open(path, 'r', encoding="utf8") as in_file:
                for line in in_file:
                    out_file.write(line)

def process_all_raw(in_path, out_path):
    files = [str(x) for x in Path(f'{in_path}').glob('**/*.txt')]

    size_counter = [0,0,0,0]

    for file in tqdm(files):
        file_count = process_raw(file, out_path)
        size_counter[0] += file_count[0]
        size_counter[1] += file_count[1]
        size_counter[2] += file_count[2]
        size_counter[3] += file_count[3]
    
    print(f'RAW: {size_counter[0]} lines and {size_counter[1]} words | CLEAN: {size_counter[2]} lines and {size_counter[3]} words')

def process_and_join(in_path, out_path, file_name):
    print('Cleaning all the raw files!')
    preprocess_path = f'{out_path}/{file_name}_processed'
    process_all_raw(in_path, preprocess_path)
    print('Joining all the raw files into one cleaned file!')
    join_files(preprocess_path, out_path, file_name)