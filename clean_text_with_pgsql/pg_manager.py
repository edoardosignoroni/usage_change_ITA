from fileinput import filename
import psycopg2
import os
import cleaner_utils as ut

def pg_select(table, where_cond=''):
    try:
        params = ut.config()        
        connection = psycopg2.connect(**params)

        cursor = connection.cursor()
        postgreSQL_select_Query = f'select * from {table}'
        if(where_cond != ''):
            postgreSQL_select_Query += f' where {where_cond}'
        cursor.execute(postgreSQL_select_Query)
        response_records = cursor.fetchall()
        return response_records

    except (Exception, psycopg2.Error) as error:
        print("Error while fetching data from PostgreSQL", error)

    finally:
        # closing database connection.
        if connection:
            cursor.close()
            connection.close()

def pg_run_query(query, with_response=False):
    conn = None
    response = None
    try:
        params = ut.config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        cur.execute(query)
        if(with_response):
            response = cur.fetchall()
        conn.commit()
        cur.close()
        if(with_response):
            return response

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

    return response

def pg_upsert(table, query_params, values, conflict = ''):
    conn = None
    sql = f"INSERT INTO {table}({','.join(query_params)}) VALUES({','.join(values)})"
    if(conflict != ''):
        sql += f" ON CONFLICT ({conflict}) DO UPDATE SET"
        for param in query_params:
            if(param != conflict):
                sql += f" {param} = EXCLUDED.{param} "
    try:
        params = ut.config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        cur.execute(sql)
        conn.commit()
        cur.close()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
        
def create_dict_table(file_name):
    print(f'Creating table public.{file_name}_dict!')

    query = f'''
    DROP TABLE IF EXISTS public.{file_name}_dict CASCADE;
    CREATE TABLE IF NOT EXISTS public.{file_name}_dict (
	id int8 NOT NULL GENERATED BY DEFAULT AS IDENTITY,
	word varchar NOT NULL,
	freq int8 NULL DEFAULT 0,
	word_code int8 NOT NULL,
	CONSTRAINT {file_name}_dict_pk PRIMARY KEY (id),
	CONSTRAINT {file_name}_dict_un UNIQUE (word_code));'''
    pg_run_query(query)

def create_text_table(file_name):
    print(f'Creating table public.{file_name}_text!')

    query = f'''
    DROP TABLE IF EXISTS public.{file_name}_text CASCADE;
    CREATE TABLE IF NOT EXISTS public.{file_name}_text (
	id int8 NOT NULL GENERATED BY DEFAULT AS IDENTITY,
	word_code int8 NOT NULL,
	word_line int8 NOT NULL,
	word_position int8 NOT NULL,
	CONSTRAINT {file_name}_text_pk PRIMARY KEY (id),
	CONSTRAINT {file_name}_text_un UNIQUE (word_line, word_position));'''
    pg_run_query(query)

def check_text_cleaner_tables_exists(in_file):
    file_name = os.path.basename(in_file)
    file_name = file_name.split('.')[0]

    query = f'''SELECT 
    COUNT(table_name)
    FROM 
        information_schema.tables 
    WHERE 
    table_schema ILIKE 'public' AND 
    table_type ILIKE 'BASE TABLE' AND
	(table_name  ILIKE '{file_name}_dict' or table_name  ILIKE '{file_name}_text');'''
    response = pg_run_query(query, True)
    return response[0][0] == 2

def pg_create_dataset_from_file(in_file, file_name):
    create_text_table(file_name)
    create_dict_table(file_name)

    conn = None

    word_dict = {}   
    
    try:
        params = ut.config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()

        # READING FILE FOR DICTIONARY GENARATIONE AND WORD POSITION UPLOADING
        with open(in_file, 'r', encoding="utf8") as in_file:
            text = in_file.readlines()
            print(f'Start elaboration of {len(text)} lines!')

            line_counter = 0
            word_id = 1
            ut.progress_bar(line_counter, len(text))
            for line in text:
                line = line.replace('\n','')
                line = line.replace("'","''")

                line = line.split()
                coded_line = ''          
                for word in line:
                    # POPULATING THE FREQ/WORD/CODE DICTIONARY
                    if word not in word_dict.keys():
                        word_dict[word] = {}
                        word_dict[word]['freq'] = 1
                        word_dict[word]['code'] = word_id
                        word_id += 1
                    else:
                        word_dict[word]['freq'] += 1

                    if(coded_line == ''):
                        coded_line += f"{word_dict[word]['code']}"
                    else:
                        coded_line += f",{word_dict[word]['code']}"

                # WORD POSITION INSERT
                if(coded_line != ''):
                    sql = f"insert into {file_name}_text(word_code, word_line, word_position) select a, {line_counter}, ROW_NUMBER () OVER ( ORDER BY (select null) ) rank_number from unnest(ARRAY[{coded_line}]) a ;"
                    cur.execute(sql)

                line_counter += 1
                if line_counter % 1000 == 0 or line_counter == len(text):
                    ut.progress_bar(line_counter, len(text))

        # UPLOADING DICTIONAY
        dict_counter = 0
        print(f'\nUploading dictionary with {len(word_dict.keys())} keys!\n')
        ut.progress_bar(dict_counter, len(word_dict.keys()))
        for key in word_dict.keys():            
            sql = f"INSERT INTO {file_name}_dict(word, freq, word_code) VALUES('{key}','{word_dict[key]['freq']}','{word_dict[key]['code']}')"
            cur.execute(sql)
            dict_counter += 1
            if dict_counter % 1000 == 0 or dict_counter == len(word_dict.keys()):
                ut.progress_bar(dict_counter, len(word_dict.keys()))

        print('\nCleaning dictionary uppercase!\n')

        clean_inner_uppercase = f'UPDATE {file_name}_dict SET word = LOWER(word) WHERE SUBSTRING(word, 2) != LOWER(SUBSTRING(word, 2))'
        
        cur.execute(clean_inner_uppercase)

        clean_first_word_uppercase = f'''
            UPDATE {file_name}_dict dict
            set word = LOWER(word)
            from {file_name}_text dt
            WHERE dt.word_code = dict.word_code
            and dt.word_position = 1
        '''
        cur.execute(clean_first_word_uppercase)

        conn.commit()
        cur.close()

        print('Upload Committed!')

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()