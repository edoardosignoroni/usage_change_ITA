# -*- coding: utf-8 -*-
"""
Created on Wed Sep 23 11:18:34 2020

@author: Edo
"""

import logging

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

#Makes a list of files in directory to be joined

import os

year = 2019
directory = r'C:\Users\Edo\Tesi\days_{}\processed\processed_days'.format(year)

file_list =[]

for entry in os.scandir(directory):
    if entry.path.endswith("{}_clean_sentencesL.txt".format(year)):
        file_list.append(entry)
        
i=0
for file in file_list:
    
    file = open(file,'r', encoding = 'utf-8')
    text = file.read().lower()
    
    print (text, file=open('days_{}\processed\days_{}_sentencesL.txt'.format(year, year), 'a+', encoding='utf-8'))
    print ('\n\n', file=open('days_{}\processed\\days_{}_sentencesL.txt'.format(year, year), 'a+', encoding = 'utf-8')) 
    
    i+=1
    print ('Processed {} of {} files'.format(i, len(file_list)))
    file.close()        