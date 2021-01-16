# -*- coding: utf-8 -*-
"""
Created on Wed Nov 11 11:23:48 2020

@author: Edo
"""

import os
import random

year = 2020
directory = r'C:\Users\Edo\Tesi\days_{}\raw'.format(year)
directory_L = r'C:/Users/Edo/Tesi/days_{}/processed/processed_days'.format(year)

file_list = []
file_list_L = []

for entry in os.scandir(directory):
    if entry.path.endswith("{}.txt".format(year)):
        file_list.append(entry)
        
for entry in os.scandir(directory_L):
    if entry.path.endswith("_clean_sentencesL.txt"):
        file_list_L.append(entry)
        
words = ['genio']
# n_collocations = 10
window = 10

#compiles a list of collocations of word

for word in words:
    
    collocations = []
    for file in file_list:
        
        file_name = str(os.path.basename(file))
        file = open(file, 'r', encoding='utf-8')
        text = file.read()
        text = text.split(' ')
        
        for token in text:
            if token == word:
                collocations.append(' '.join(text[text.index(token)-window : text.index(token)+window]))
            
        file.close()

        collocations_p = '\n'.join(collocations)
        print(collocations_p, file=open('C:/Users/Edo/Tesi/collocations/{}_{}_collocations.txt'.format(word, year), 'w+', encoding='utf-8'))
    
    collocations_L = []
    for file_L in file_list_L:
        
        file_L_name = str(os.path.basename(file_L))
        file_L = open(file_L, 'r', encoding='utf-8')
        text_L = file_L.read()
        text_L = text_L.split(' ')
        
        
        for token in text_L:
            if token == word:
                collocations_L.append(' '.join(text_L[text_L.index(token)-window : text_L.index(token)+window]))
            
        file_L.close()

        collocations_L_p = '\n'.join(collocations_L)
        print(collocations_L_p, file=open('C:/Users/Edo/Tesi/collocations/{}_{}_collocations_L.txt'.format(word, year), 'w+', encoding='utf-8'))