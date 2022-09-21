import os
from re import I
from tqdm import tqdm
import argparse

#OUR .py FILES
import raw_parser as raw
import cleaner_utils as ut
import pg_manager as pgm
import lemmatizer as lem

def generate_clean_file(out_path, file_name):
    print('Launch select query for clean text!')
    result = pgm.get_filtered_data(file_name)

    print('Query ended! Creating the file!')
    config = ut.config(section='cleaner')
    
    with open(out_path, 'w+', encoding='utf-8') as out_file:
        for line in tqdm(result):
            splitted_line = line[0].split()
            if len(splitted_line) >= int(config['min_word_in_line']):
                out_file.write(line[0] + '\n')

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

def run_all(raw_dir_path, out_path, lemmatizer, file_name):    

    if not os.path.isdir(out_path):
        os.mkdir(out_path)
    out_path = f'{out_path}/{file_name}'
    if not os.path.isdir(out_path):
        os.mkdir(out_path)

    joined_file_path = f'{out_path}/{file_name}_joined.txt'
    lemmatized_file_path = f'{out_path}/{file_name}_lemm.txt'
    clean_file_path = f'{out_path}/{file_name}_clean.txt'

    raw.process_and_join(raw_dir_path, out_path, file_name)

    if lemmatizer != 'none':               
        lem.lemmatize_file(joined_file_path, lemmatized_file_path, lemmatizer)    
        run_create_dataset(lemmatized_file_path, file_name)
    else:
        run_create_dataset(joined_file_path, file_name)    
    
    generate_clean_file(clean_file_path,file_name)

# ARGUMENT MANAGMENT
parser = argparse.ArgumentParser(prog='cleaner',
                                    description='Filter text data')
parser.add_argument("mode",
                    choices=["all", "raw", "lemm", "dataset", "clean"],
                    help="Execution mode: can run all the cleanings or just some specific part.")
parser.add_argument("-l",
                    action='store',
                    choices=["stanza", "spacy", "simplemma"],
                    default="none",
                    required=False,
                    help="Choose the lemmatizer, default is no lemmatization")
parser.add_argument("-i",
                    action='store',
                    required=False,
                    help="Input Path")
parser.add_argument("-o",
                    action='store',
                    required=False,
                    help="Output Path")
parser.add_argument("-n",
                    required=False,
                    help="Name of the produced file")

if __name__ == '__main__':
    args = parser.parse_args()
    '''
    mode = 'dataset'
    input = 'F:\test_cleaner\days_2019_10\days_2019_10_temp_lemm.txt'
    output = 'E:/test_cleaner'
    lemm = 'simplemma'
    name = 'days_2019_10'
    '''
    mode = args.mode
    input = args.i
    output = args.o
    lemm = args.l
    name = args.n
    
    err = False

    if not mode:
        print("The MODE argument is not specified, use -h for help.")
        err = True
    if not input and (mode in ['all', 'raw', 'lemm', 'dataset']) :
        print("The INPUT PATH (-i) argument is not specified, use -h for help.")
        err = True
    if not output and (mode in ['all', 'raw', 'lemm', 'clean']):
        print("The OUTPUT PATH (-o) argument is not specified, use -h for help.")
        err = True
    if not name and (mode in ['all', 'raw', 'dataset', 'clean']):
        print("The NAME (-n) argument is not specified, use -h for help.")
        err = True

    if not err:
        if mode == "all":
            run_all(input, output, lemm, name)
        elif mode == "raw":
            run_raw_processing(input, output, name)
        elif mode == "lemm":
            lem.lemmatize_file(input, output, lemm)
        elif mode == "dataset":
            run_create_dataset(input, name)
        elif mode == "clean":
            run_generate_clean_file(output, name)
