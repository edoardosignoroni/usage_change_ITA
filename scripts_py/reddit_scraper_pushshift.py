# -*- coding: utf-8 -*-

from re import sub
from xml.dom.pulldom import END_DOCUMENT
import praw
from psaw import PushshiftAPI
import datetime as dt
import time
import os
import sys

r = praw.Reddit(client_id = 'z1sHTaSdDhF4HQ',
                      client_secret = 'xS3qUXdvGvZpUiRewMJ9zaNb3aY',
                       password = 'q1w2e3r4t5',
                      user_agent = 'windows:ita_scraper_test.v0.1 (by /u/EdwardGreatlords)',
                       username = 'EdwardGreatlords')
api = PushshiftAPI(r)

def shards_check():
    down = True
    while down == True:
        shards = api.metadata_.get('shards')
        if shards==None:
            print('NO SHARDS FOUND!')
            time.sleep(60)
            continue
        t_shards = shards['total']
        s_shards = shards['successful']
        if int(s_shards) < int(t_shards):    
            print(f'SHARDS DOWN! ONLY {s_shards} OUT OF {t_shards}')
            time.sleep(60)
            continue
        down = False
        print('ALL SHARDS UP! PROCEEDING TO SCRAPE DATA')
    return down

def scrape(start_date, end_date=None, out_path='../data'):

    if not end_date:
        end_date=[start_date[0], 12, 31]

    start_epoch = int(dt.datetime(start_date[0], start_date[1], start_date[2]).timestamp())
    end_epoch = int(dt.datetime(end_date[0], end_date[1], end_date[2]).timestamp())

    print('Gathering submissions...')
    submissions = list(api.search_submissions(before=end_epoch, after=start_epoch, subreddit='italy'))

    print(len(submissions))

    # All the posts and comments, without the BOT ones. Comments of megathreads and stickied submissions. Title and post taken only one time. All divided by day.
    print('Saving submissions...')
    
    for submission in submissions:
        sub_time = time.gmtime(submission.created_utc).tm_yday
        
        file_name = f'{out_path}/days_{start_date[0]}/day_{sub_time}_{start_date[0]}.txt'

        if not os.path.isdir(f'{out_path}/days_{start_date[0]}'):
            os.mkdir(f'{out_path}/days_{start_date[0]}')

        with open(file_name, 'a+', encoding = 'utf-8', errors = 'ignore') as out_file:        
            
            if submission.stickied: #evita doppioni e vedi sotto
            
                text = []

                print (f'date: {sub_time}')
                
                submission.comments.replace_more(limit=None)
                
                for comment in submission.comments.list():
                    
                    if not comment.stickied: #la maggior parte dei post dei bot è sticky
                    
                        if comment.author != 'RedditItalyBot' and comment.author != 'AutoModerator':
                    
                            text.append(comment.body.strip('>').replace('\n', ''))   
                
                out_file.write(' '.join(text)+'\n')         
                
            else:
                
                text = []

                print (f'date: {sub_time}')
                text.append(submission.title.replace('\n', ''))
                text.append(submission.selftext.replace('\n', ''))
                
                submission.comments.replace_more(limit=None)
                    
                for comment in submission.comments.list():
                    
                    if not comment.stickied:
                                
                        if comment.author != 'RedditItalyBot' and comment.author != 'AutoModerator':
                    
                            text.append(comment.body.strip('>').replace('\n', ''))             
                
                        # if len(comment.replies) > 0:
                        #     for reply in comment.replies:
                        #         print(reply.body, out_file)
                out_file.write(' '.join(text)+'\n')
                # print(r.auth.limits)

    print ("___FINISHED___ ")

down = shards_check()

if down == False: 
    scrape([2020,1,1], [2020,12,31], '../data')