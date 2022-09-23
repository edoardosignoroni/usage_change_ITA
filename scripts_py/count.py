# -*- coding: utf-8 -*-
"""
Created on Tue Jan 12 11:56:55 2021

@author: Edo
"""

import os
import operator

year = 2020
directory = r'C:\Users\Edo\Tesi\days_{}\processed\processed_days'.format(year)

file_list =[]

d = {}

for entry in os.scandir(directory):
    if entry.path.endswith("_clean_sentencesL.txt".format(year)):
        file_list.append(entry)
        
for file in file_list:
    # with open(file,'r', encoding= 'utf-8') as infile:
    file_name = int(os.path.basename(file).strip('day_').strip('_clean_sentencesL.txt')[:-5])
    file=open(file, 'r', encoding=('utf-8'))
    text = file.read()
    text = text.split(' ')
    d[file_name]=len(text)
        
d = dict(sorted(d.items(), key=operator.itemgetter(0),reverse=False))
# print(file_name, file=open('C:/Users/Edo/Tesi/days_{}/{}_count.txt'.format(year, year), 'a+', encoding='utf-8'))
for key, value in d.items():
    print(value,  file=open('C:/Users/Edo/Tesi/days_{}/{}_count_lemma.txt'.format(year, year), 'a+', encoding='utf-8'))
