import os
from tqdm import tqdm

from simplemma import lemmatize
import spacy
import stanza

# OUR .py FILES
import pg_manager as pgm

def lemmatize_file(in_file, out_path, lemmatizer='stanza'):

    # GET CHECK POINT IF EXISTS
    dir_path = os.path.dirname(os.path.realpath(out_path))
    file_name = os.path.basename(out_path)
    file_name = os.path.splitext(file_name)[0]
    check_point_path = f'{dir_path}/{file_name}.checkpoint'

    check_point_line = -1

    if os.path.exists(check_point_path):
        with open(check_point_path, 'r', encoding="utf8") as text_file:        
            check_point_line = int(text_file.readline())

    # READ FILE
    text = []

    with open(in_file, 'r', encoding="utf8") as text_file:        
        text = text_file.readlines()

    # TEXT LEMMATIZATION
    response = {}

    if lemmatizer == 'stanza':
        response = stanza_lemmatize(text, check_point_line)
    elif lemmatizer == 'spacy':
        response = spacy_lemmatize(text, 'it_core_news_lg')
    elif lemmatizer == 'simplemma':
        response = simplemma_lemmatize(text)
    
    # GENERATING LEMMATIZED FILE
    if check_point_line == -1:
        # CREATING A NEW FILE IF THERE WAS NO CHECKPOINT  
        with open(out_path, 'w+', encoding='utf-8') as out_file:
            for line in tqdm(response['text']):
                out_file.write(line + '\n')
    else:
        # APPENDING THE OLD FILE IF THERE WAS A CHECKPOINT
        with open(out_path, 'a', encoding='utf-8') as out_file:
            for line in tqdm(response['text']):
                out_file.write(line + '\n')

    # CREATING CHECKPOINT IN CASE OF ERROR
    if response['error'] == True:
        with open(check_point_path, 'w+', encoding='utf-8') as out_file:
            out_file.write(f"{response['line']}\n{response['message']}")

def spacy_lemmatize(text, model):
    response = {}
    text_lemm = []

    load_model = spacy.load(model, disable=['parser', 'ner'])
    i=1
    string_buffer = ''
    line_check_point = 1
    for line in tqdm(text):
        line = line.replace('\n', '')
        string_buffer += line + '\n'
        if i % 5000 == 0 or i >= len(text):
            string_buffer_lemm = load_model(string_buffer)
            string_buffer_lemm = ' '.join([token.lemma_ for token in string_buffer_lemm])
            string_buffer = ''
            string_buffer_lemm = string_buffer_lemm.split(' \n ')
            text_lemm.extend(string_buffer_lemm)
            line_check_point = i
        i += 1

    response['line'] = line_check_point
    response['error'] = False
    response['text'] = text_lemm
    return response

def stanza_lemmatize(text, checkpoint = -1):
    response = {}
    text_lemm = []
    nlp = stanza.Pipeline(lang='it', processors='tokenize,mwt,pos,lemma', use_gpu=True, tokenize_no_ssplit=True, lemma_batch_size=25)

    i=1
    string_buffer = ''
    check_point_line = 1
    checkpoint_set = checkpoint <= 0
    for line in tqdm(text):
        if checkpoint_set:
            line = line.replace('\n', '')
            string_buffer += line + '\n\n'
            if i % 50 == 0 or i >= len(text):

                try:
                    string_buffer_lemm = nlp(string_buffer)
                except Exception as e: 
                    response['line'] = check_point_line
                    response['error'] = True
                    response['text'] = text_lemm
                    response['message'] = e
                    return response

                for sent in string_buffer_lemm.sentences:
                    string_lemm = ' '.join([word.lemma for word in sent.words])
                    text_lemm.append(string_lemm)
                string_buffer = ''
                check_point_line = i
        elif i == checkpoint:
            checkpoint_set = True
            check_point_line = i

        i += 1
    response['line'] = check_point_line
    response['error'] = False
    response['text'] = text_lemm
    return response

def simplemma_lemmatize(text):
    response = {}
    text_lemm = []

    for line in tqdm(text):
        line = line.replace('\n','')
        splitted_line = line.split()
        lemmatized_splitted_line = []
        for word in splitted_line:
            if word.istitle():
                lemmatized_splitted_line.append(lemmatize(word,  lang=('it', 'en')).capitalize())
            else:
                lemmatized_splitted_line.append(lemmatize(word,  lang=('it', 'en')))
        text_lemm.append(' '.join(lemmatized_splitted_line) + '\n')
    
    response['line'] = -1
    response['error'] = False
    response['text'] = text_lemm
    return response