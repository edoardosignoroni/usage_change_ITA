# -*- coding: utf-8 -*-
"""
Created on Mon Sep 21 16:37:11 2020

@author: Edo
"""
import logging
import time

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

#DATA PREPROCESSING

import re
import os
from nltk.corpus import stopwords

#year of data to process and output directory
year = 2020
directory = r'\days_{}\clean'.format(year)

#user-defined stopwords to be removed
user_stopwords = ['bla', 'peró', 'cosí', 'bon', 'ehm', 'bhe', 'uh', 'aaaah', 'aaah', 'ahhhh', 'noooo', 'ahahahaha', 'hahahah', 'mmh', 'mhh', 'ahahha', 'mmmh', 'ah', 'ehh', 'eheh', 'ohi', 'ehe' ]

#compiles list of files to process. 
file_list =[]

for entry in os.scandir(directory):
    if entry.path.endswith("_{}.txt".format(year)):
        file_list.append(entry)
        
init_time = time.time()
i=0
for file in file_list:
    start_time = time.time()
    
    file_name = str(os.path.basename(file)).strip('.txt')
    print('Processing file: {}'.format(str(os.path.basename(file))))
    file = open(file,'r', encoding = 'utf-8')
    text = file.read().lower() #lowercasing
    text = re.sub(r'http\S+', ' URL', text) #Removes URLs
    text = re.sub(r'[!"”$%&()*+,-.\\:;<=>?@\[\]^_`{|}~…»•😀❤️😀🤔🤣😭😅🙄😉—]', '', text)   #Removes [] and other special chars
    text = re.sub(r'#x200B', '', text)
    
    text = text.split()
    
    
    for word in text:
        if word in stopwords.words('italian') or word in user_stopwords:
            text.remove(word)
        elif len(word)>24:
            text.insert(text.index(word),'LONG')
            text.remove(word)
           
    z=1
    for word in text:
        
        if z%3000==0: #provides buffer for RAM usage
            text.insert(z, '\n\n')
        z+=1    
    
            
    text = ' '.join(text)
    
    print (text, file=open('days_{}\clean\{}.txt'.format(year, file_name), 'w+', encoding='utf-8'))
    
    i+=1
    elapsed_time = time.time() - start_time
    print ('Processed {} in {} - {}/{}'.format(file_name+'.txt', time.strftime("%H:%M:%S", time.gmtime(elapsed_time)), i, len(file_list)))
    file.close()
    
total_time = time.time() - init_time
print ('Processed all {} of {} files in {}'.format(i, len(file_list), time.strftime("%H:%M:%S", time.gmtime(total_time))))
