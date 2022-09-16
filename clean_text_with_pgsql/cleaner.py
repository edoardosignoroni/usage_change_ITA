from ast import arg
from unittest import result
import pg_manager as pgm
import raw_parser as raw
import cleaner_utils as ut
from simplemma import lemmatize
import spacy
from tqdm import tqdm 
import os
import argparse
import stanza

def generate_clean_file(out_path, file_name):
    result = pgm.get_filtered_data(file_name)

    print(len(result))
    config = ut.config(section='cleaner')
    
    with open(out_path, 'w+', encoding='utf-8') as out_file:
        for line in result:
            splitted_line = line[0].split()
            if len(splitted_line) >= int(config['min_word_in_line']):
                out_file.write(line[0] + '\n')

def generate_clean_file_lemmatized(out_path, file_name):
    result = pgm.get_filtered_data(file_name)

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

def lemmatize_file(in_file, out_path, lemmatizer='stanza'):
    text = []
    with open(in_file, 'r', encoding="utf8") as text_file:        
        text = text_file.readlines()

    if lemmatizer == 'stanza':
        text = stanza_lemmatize(text)
    elif lemmatizer == 'spacy':
        text = spacy_lemmatize(text, 'it_core_news_lg')
    
    with open(out_path, 'w+', encoding='utf-8') as out_file:
        for line in tqdm(text):
            out_file.write(line + '\n')

def spacy_lemmatize(text, model):
    text_lemm = []
    load_model = spacy.load(model, disable=['parser', 'ner'])
    i=1
    string_buffer = ''
    for line in tqdm(text):
        line = line.replace('\n', '')
        string_buffer += line + '\n'
        if i % 5000 == 0 or i >= len(text):
            string_buffer_lemm = load_model(string_buffer)
            string_buffer_lemm = ' '.join([token.lemma_ for token in string_buffer_lemm])
            string_buffer = ''
            string_buffer_lemm = string_buffer_lemm.split(' \n ')
            text_lemm.extend(string_buffer_lemm)
        i += 1
    return text_lemm

def stanza_lemmatize(text):
    text_lemm = []
    nlp = stanza.Pipeline(lang='it', processors='tokenize,mwt,pos,lemma', use_gpu=True)
    '''for line in tqdm(text):
        line = line.replace('\n', '')
        splitted_lemm_line = nlp(line)
        joined_lemm_line = ' '.join([word.lemma for sent in splitted_lemm_line.sentences for word in sent.words])
        text_lemm.append(joined_lemm_line)
    '''
    i=1
    string_buffer = ''
    for line in tqdm(text):
        line = line.replace('\n', '')
        string_buffer += line + '\n'
        if i % 5000 == 0 or i >= len(text):
            string_buffer_lemm = nlp(string_buffer)
            for sent in string_buffer_lemm.sentences:
                string_lemm = ' '.join([word.lemma for word in sent.words])
                text_lemm.append(string_lemm)
            string_buffer = ''
        i += 1
    return text_lemm

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

def run_all_lemm_first(raw_dir_path, out_path, file_name):
    if not os.path.isdir(out_path):
        os.mkdir(out_path)
    out_path = f'{out_path}/{file_name}'
    if not os.path.isdir(out_path):
        os.mkdir(out_path)

    raw.process_and_join(raw_dir_path, out_path, file_name)
    preprocessed_file_path = f'{out_path}/{file_name}_temp.txt'

    preprocessed_lemm_file_path = f'{out_path}/{file_name}_temp_lemm.txt'
    lemmatize_file(preprocessed_file_path,preprocessed_lemm_file_path)

    pgm.pg_create_dataset_from_file(preprocessed_lemm_file_path, file_name)

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

parser = argparse.ArgumentParser(prog='cleaner',
                                    usage='%(prog)s mode [options] name',
                                    description='Filter text data')
parser.add_argument("mode",
                    choices=["all", "raw", "lemm", "dataset", "clean"],
                    help="Execution mode: can run all the cleanings or just some specific part.")
parser.add_argument("-l",
                    action='store_true',
                    help="With lemmatization")
parser.add_argument("-i",
                    action='store',
                    help="Input Path")
parser.add_argument("-o",
                    action='store',
                    help="Output Path")
parser.add_argument("name",
                    help="Name of the produced file")

if __name__ == '__main__':
    #args = parser.parse_args()

    mode = 'lemm'
    i = 'E:\\test_cleaner\\days_2019\\days_2019_temp.txt'
    o = 'E:\\test_cleaner\\days_2019\\days_2019_lemm_test.txt'
    l = True
    name = 'days_2019'
    
    #mode = args.mode
    #i = args.i
    #o = args.o
    #l = args.l
    #name = args.name    

    if mode == "all":        
        if l:
            run_all_lemm_first(i, o, name)
        else:
            run_all(i, o, name)
    elif mode == "raw":
        run_raw_processing(i, o, name)
    elif mode == "lemm":
        lemmatize_file(i, o)
    elif mode == "dataset":
        run_create_dataset(i, name)
    elif mode == "clean":
        run_generate_clean_file(o, name)
