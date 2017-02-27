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

# determine if all characters of sentence_string are English
def is_english(sentence_string):
   return all([ord(i)<128 for i in list(sentence_string)])

# basic string cleaning
def clean(string):
   string = re.sub('/s', '', string) # remove /s at end
   string = ' '.join(string.split()) # remove extra spaces within text 
   return string

# main method
def main():
   # EDIT THESE THREE USER-DEFINED VALUES AS NEEDED
   input_filename = '/n/fs/nlpdatasets/reddit_unzipped/RC_2015-01'
   target_filename = './cleaned'
   month_year = '01_2015'

   with open(target_filename, 'w') as csvfile:
      fieldnames = ['comment_string', 'user', 'subreddit', 'num_upvotes', 'month_year','sarcasm_label']
      writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
      writer.writeheader()

      with open(input_filename) as inputfile:
         for line in inputfile:
            line_dict = json.loads(line)
            
            if is_english(line_dict['body']):
               new_dict = {}
               new_dict['comment_string'] = clean(line_dict['body']) 
               new_dict['user'] = line_dict['author']
               new_dict['subreddit'] = line_dict['subreddit']
               new_dict['num_upvotes'] = line_dict['score']
               new_dict['month_year'] = month_year

               if re.search('/s$', line_dict['body']) != None:
                  new_dict['sarcasm_label'] = 1
               else:
                  new_dict['sarcasm_label'] = 0

               writer.writerow(new_dict)
               
if __name__ == "__main__": main()
