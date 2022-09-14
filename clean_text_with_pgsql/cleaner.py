from unittest import result
import pg_manager as pgm
import raw_parser as raw
import cleaner_utils as ut
from simplemma import lemmatize
import spacy
from tqdm import tqdm 
import os

def generate_clean_file(out_path, file_name):
    result = pgm.get_filtered_data(out_path, file_name)

    print(len(result))
    
    with open(out_path, 'w+', encoding='utf-8') as out_file:
        for line in result:
            out_file.write(line[0] + '\n')

def generate_clean_file_lemmatized(out_path, file_name):
    result = pgm.get_filtered_data(out_path, file_name)

    print(len(result))

    with open(out_path, 'w+', encoding='utf-8') as out_file:
        i=0
        for line in tqdm(result):
            splitted_line = line[0].split()
            lemmatized_splitted_line = []
            for word in splitted_line:
                lemmatized_splitted_line.append(lemmatize(word,  lang=('it', 'en')))
            out_file.write(' '.join(lemmatized_splitted_line) + '\n')
            i += 1

def generate_clean_file_lemmatized_spacy(out_path, file_name):
    result = pgm.get_filtered_data(out_path, file_name)

    print(len(result))

    load_model = spacy.load('it_core_news_sm', disable=['parser', 'ner'])
    with open(out_path, 'w+', encoding='utf-8') as out_file:
        i=0
        string_buffer = ''
        for line in tqdm(result):
            string_line = line[0]
            string_buffer += string_line + '\n'
            if i % 5000 == 0 or i >= len(result) - 1:
                string_buffer_lemm = load_model(string_buffer)
                string_buffer_lemm = ' '.join([token.lemma_ for token in string_buffer_lemm])
                string_buffer = ''
                string_buffer_lemm = string_buffer_lemm.split(' \n ')
                out_file.write('\n'.join(string_buffer_lemm))
            i += 1

def run_all(raw_dir_path, out_path, file_name):
    if not os.path.isdir(out_path):
        os.mkdir(out_path)
    out_path = f'{out_path}/{file_name}'
    if not os.path.isdir(out_path):
        os.mkdir(out_path)

    raw.process_and_join(raw_dir_path, out_path, file_name)
    preprocessed_file_path = f'{out_path}/{file_name}_temp.txt'
    pgm.pg_create_dataset_from_file(preprocessed_file_path, file_name)
    print('Starting cleaning file!')
    processed_file_path = f'{out_path}/{file_name}.txt'
    generate_clean_file(processed_file_path,file_name)
    print('Finished!')

def run_raw_processing(raw_dir_path, out_path, file_name):
    if not os.path.isdir(out_path):
        os.mkdir(out_path)
    out_path = f'{out_path}/{file_name}'
    if not os.path.isdir(out_path):
        os.mkdir(out_path)
        
    raw.process_and_join(raw_dir_path, out_path, file_name)
    print('Finished!')

def run_create_dataset(file_path, file_name):
    pgm.pg_create_dataset_from_file(file_path, file_name)
    print('Finished!')

def run_generate_clean_file(out_file, table_prefix):
    print('Starting cleaning file!')
    generate_clean_file(out_file, table_prefix)
    print('Finished!')

#run_all('E:\\Download\\data\\days_2019\\raw', 'E:\\Programmi Python\\clean_text', 'days_2019')
#run_raw_processing('E:\\Download\\data\\days_2019\\raw', 'E:\\test_cleaner', 'days_2019')
#run_create_dataset('E:\\test_cleaner\\days_2019\\days_2019_temp.txt', 'days_2019')
#run_generate_clean_file('E:\\test_cleaner\\days_2019\\days_2019_clean.txt', 'days_2019')
#generate_clean_file_lemmatized('../data/2019_clean/days_2019/days_2019_spacy.txt', 'days_2019')
