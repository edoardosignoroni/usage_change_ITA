# -*- coding: utf-8 -*-
"""
Created on Mon Jan  4 13:47:40 2021

@author: Edo
"""

import csv
import os
import operator

year = 2020
directory = r'C:\Users\Edo\Tesi\days_{}\freq\lemma_freq'.format(year)

file_list =[]

words = ['coronavirus']

for word in words:

    d = {}

    for entry in os.scandir(directory):
        if entry.path.endswith("{}.txt".format(year)):
            file_list.append(entry)
            
    for file in file_list:
        with open(file,'r', encoding= 'utf-8') as infile:
            file_name = int(os.path.basename(file).strip('lemma_').strip('.txt')[:-5])
            reader = csv.reader(infile)
            freq_day = {rows[0]:rows[1] for rows in reader}
            
            # t = ()m,                                                   
            if word in freq_day.keys():
            #     t = (int(file_name), int(freq_day[word]))
                d[file_name]=freq_day[word]
            else:
            #     t = (int(file_name), 0)
                d[file_name]=0
               
    d = dict(sorted(d.items(), key=operator.itemgetter(0),reverse=False))
    print(word, file=open('C:/Users/Edo/Tesi/days_{}/{}_{}.txt'.format(year, word, year), 'a+', encoding='utf-8'))
    for key, value in d.items():
        print(value,  file=open('C:/Users/Edo/Tesi/days_{}/{}_{}.txt'.format(year, word, year), 'a+', encoding='utf-8'))
