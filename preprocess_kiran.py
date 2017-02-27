"""
preprocess.py
Writes Reddit data to CSV file, with 1 post per line. 
Each post contains the following attributes:
(1) comment_string
(2) user
(3) subreddit
(4) num_upvotes
(5) month_year
"""

import re
import csv
import json
import os

# determine if all characters of sentence_string are English
def is_english(sentence_string):
   return all([ord(i)<128 for i in list(sentence_string)])

# basic string cleaning
def clean(string):
   string = re.sub('/s', '', string) # remove /s at end
   string = ' '.join(string.split()) # remove extra spaces within text 
   return string

# year = int from 2007 - 2016 inclusive, month = int from 1 to 12 inclusive
# valid_user_set is a set of users which have said something sarcastic in the past
# and are therefore valid to be added to the set. 
def load_reddit_file(year, month, valid_user_set):
   assert((year >= 2007) and (year <= 2016))
   assert((month >= 1) and (month <= 12))

   if month < 10:
      mstr = str(0) + str(month)
   else:
      mstr = str(month)

   input_fname = '/n/fs/nlpdatasets/reddit_data/RC_' + str(year) + "-" + mstr
   target_dir = './filtered_reddit/'
   target_fname = 'filtered_reddit_' + mstr + '-' + str(year)

   # check if target_dir exists; if not create it in current directory
   if not os.path.exists(target_dir):
      os.makedirs(target_dir)

   target_fname += target_dir

   with open(target_fname, 'bw') as csvfile:

      fieldnames = ['comment_string', 'user', 'subreddit', 'num_upvotes', 'month_year','sarcasm_label']
      writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
      writer.writeheader()

      with open(input_fname) as inputfile:
         for line in inputfile:
            line_dict = json.loads(line)
            if is_english(line_dict['body']):
               curr_user = line_dict['author']
               new_dict = {}
               new_dict['comment_string'] = clean(line_dict['body']) 
               new_dict['user'] = curr_user
               new_dict['subreddit'] = line_dict['subreddit']
               new_dict['num_upvotes'] = line_dict['score']
               new_dict['month_year'] = month_year

               if re.search('/s$', line_dict['body'].strip()) != None:
                  new_dict['sarcasm_label'] = 1
               else:
                  new_dict['sarcasm_label'] = 0

               if curr_user in valid_user_set:
                  writer.writerow(new_dict)
               else:
                  if curr_user not in valid_user_set:
                     if new_dict['sarcasm_label'] == 1:
                        # curr_user is using sarcasm for the first time
                        writer.writerow(new_dict)
                        valid_user_set.add(curr_user)

   return valid_user_set

# main method
def main():
   valid_user_set = set()
   for year in range(2007, 2017):
      for month in range(1, 13):
         valid_user_set = load_reddit_file(year, month, valid_user_set)

               
if __name__ == "__main__": main()
