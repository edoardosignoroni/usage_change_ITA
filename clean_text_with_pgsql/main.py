import pg_manager as pgm
import os

def freqs_db(in_file):

    freqs = {}

    file_name = os.path.basename(in_file)
    file_name = file_name.split('.')[0]

    with open(in_file, 'r', encoding="utf8") as in_file:
        text = in_file.readlines()

        for line in text:
            line = line.split()
            for word in line:
                word = word.replace("'", "''")

                if word not in freqs.keys():
                    freqs[word] = 1
                else:
                    freqs[word] += 1
    print('Freq dictionary done!')
    pgm.create_freq_table(file_name)
    pgm.pg_upsert_from_dictionary(f"{file_name}_freq", ["word", "freq"], freqs, "word")
    return freqs

def generate_clean_file(out_path):
    config = pgm.config(section='cleaner')
    query = f'''select string_agg(a.word, ' ')
    from (
        select dspt.word word, dspt.word_line word_line
        from days_2020_sentencesl_prepost_text dspt 
        where dspt.word in (
            select dspf.word 
            from days_2020_sentencesl_prepost_freq dspf 
            where 
            length(dspf.word) >= {config['min_freq']}
            and dspf.freq >=  {config['min_word_len']} 
            and dspf.word ~ {config['regex_filter']}
        )
        order by word_line, word_position asc
    ) as a
    group by a.word_line
    '''
    result = pgm.pg_run_query(query, True)
    print('Query done! Now Joining...')
    print(len(result))
    with open(out_path, 'w+', encoding='utf-8') as out_file:
        for line in result:
            out_file.write(line[0])

def run_all(in_file, out_file, force_update=False):
    if(not pgm.check_text_cleaner_tables_exists(in_file) or force_update):
        print('Starting freq calculation!')
        freqs_db(in_file)
        print('Starting file upload!')
        pgm.pg_upsert_from_text(in_file)
    print('Starting cleaning file!')
    generate_clean_file(out_file)
    print('Finished!')

run_all('E:\Programmi Python\clean_text\days_2020_sentencesL_prepost_2.txt', 'E:\Programmi Python\clean_text\days_2020_sentencesL_prepost_clean2.txt')