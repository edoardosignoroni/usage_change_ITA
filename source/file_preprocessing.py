# -*- coding: utf-8 -*-
"""
Created on Fri Oct  2 10:16:04 2020

@author: Edo
"""
import logging
import time
import stanza

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

import os

year = 2019

directory = r'C:\Users\Edo\Tesi\days_{}\clean'.format(year)
processed_dir= r'C:\Users\Edo\Tesi\days_{}\processed\processed_days'.format(year)

file_list = []
done_list = []

for entry in os.scandir(directory):
    if entry.path.endswith("_clean.txt"):
        file_list.append(entry)

for entry in os.scandir(processed_dir):
    if entry.path.endswith("sentencesT.txt"):
        entry_name = str(os.path.basename(entry).strip('sentencesT.txt')[:-1])
        done_list.append(entry_name)

for done_entry in done_list:
    done_path = done_entry+'.txt'
    for entry in file_list:
        if entry.path.endswith(done_path):
            file_list.remove(entry)

error = False
for f in done_list:
    if f in file_list:
        error = True
        print(f, 'IN LIST! ERROR!')
if error:
    quit()
else:
    print("Lists OK!")

print (len(file_list))

if len(file_list) == 0:
    print('ALL DONE!')
else:
    init_time = time.time()
    
    nlp = stanza.Pipeline(lang='it', processors='tokenize', tokenize_batch_size=25, mwt_batch_size=25, pos_batch_size=250, lemma_batch_size=25, lemma_max_dec_len=25, logging_level='WARN', use_gpu=True)
    i=0
    for file in file_list:
        
        start_time = time.time()
        file_name = str(os.path.basename(file)[:-4])
        print('Processing file: {}'.format(file_name+'.txt'))
        file = open(file, 'r', encoding='utf-8')
        text = file.read()
        file.close()
        
        
        doc = nlp(text)
        
        for s in doc.sentences:
            s_list = []
            for w in s.words:
                s_list.append(w.text)
           
            print (" ".join(s_list), file=open('days_{}/processed/processed_days/{}_sentencesT.txt'.format(year, file_name), 'a+', encoding = 'utf-8')) 
        
        i+=1
        elapsed_time = time.time() - start_time
        
        print ('Processed {} in {} - {}/{}'.format(file_name+'.txt', time.strftime("%H:%M:%S", time.gmtime(elapsed_time)), i, len(file_list)))
        file.close()
    total_time = time.time() - init_time
    print ('Processed all {} of {} files in {}'.format(i, len(file_list), time.strftime("%H:%M:%S", time.gmtime(total_time))))