import pg_manager as pgm
import raw_parser as raw
import cleaner_utils as ut
import os

def generate_clean_file(out_path, in_file):
    file_name = os.path.basename(in_file)
    file_name = file_name.split('.')[0]

    config = ut.config(section='cleaner')
    query = f'''select string_agg(a.word, ' ')
    from (
        select dspf.word word, dspt.word_line word_line
        from {file_name}_text dspt 
        inner join {file_name}_dict dspf on dspf.word_code = dspt.word_code
        where length(dspf.word) >= {config['min_word_len']}
        and dspf.freq >= {config['min_freq']} 
        and dspf.word ~ {config['regex_filter']}
        order by word_line, word_position asc
    ) as a
    group by a.word_line
    '''
    result = pgm.pg_run_query(query, True)
    print('Query done! Now Joining...')
    print(len(result))
    with open(out_path, 'w+', encoding='utf-8') as out_file:
        for line in result:
            out_file.write(line[0] + '\n')

def run_all(raw_dir_path, out_path, file_name):
    if not os.path.isdir(out_path):
        os.mkdir(out_path)
    out_path = f'{out_path}\\{file_name}'
    if not os.path.isdir(out_path):
        os.mkdir(out_path)

    raw.process_and_join(raw_dir_path, out_path, file_name)

    preprocessed_file_path = f'{out_path}\\{file_name}_temp.txt'
    pgm.pg_create_dataset_from_file(preprocessed_file_path, file_name)

    print('Starting cleaning file!')
    processed_file_path = f'{out_path}\\{file_name}.txt'
    generate_clean_file(processed_file_path,preprocessed_file_path)
    print('Finished!')

def run_raw_processing(raw_dir_path, out_path, file_name):
    if not os.path.isdir(out_path):
        os.mkdir(out_path)
    out_path = f'{out_path}\\{file_name}'
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