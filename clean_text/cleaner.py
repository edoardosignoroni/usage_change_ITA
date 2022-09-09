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

def generate_clean_file(out_path, in_file):
    config = pgm.config(section='cleaner')

    file_name = os.path.basename(in_file)
    file_name = file_name.split('.')[0]

    query = f'''select string_agg(a.word, ' ')
    from (
        select dspt.word word, dspt.word_line word_line
        from {file_name}_text dspt 
        where dspt.word in (
            select dspf.word 
            from {file_name}_freq dspf 
            where 
            length(dspf.word) >= {config['min_word_len']}
            and dspf.freq >=  {config['min_freq']} 
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
            out_file.write(line[0]+'\n')

def run_all(in_file, out_file, force_update=False):
    if(not pgm.check_text_cleaner_tables_exists(in_file) or force_update):
        print('Starting freq calculation!')
        freqs_db(in_file)
        print('Starting file upload!')
        pgm.pg_upsert_from_text(in_file)
    print('Starting cleaning file!')
    generate_clean_file(out_file, in_file)
    print('Finished!')

#(^[A-Za-z0-9àáèéìíòóùúüö''’`.-]*$)|(^r/.*$)|(^#.*$)|
#prima parte tiene le lettere concesse, tutto il resto lo cancella
#2a parte tiene le r/
#3a per il cancelletto