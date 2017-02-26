# determine if all characters of sentence_string are English
def is_english(sentence_string):
   return all([ord(i)<128 for i in list(sentence_string)])

# basic string cleaning
def clean(string):
   string = re.sub('/s', '', string) # remove /s at end
   string = ' '.join(string.split()) # remove extra spaces within text 

# main method
def main():
   input_filename = '/n/fs/nlpdatasets/reddit_unzipped/RC_2015-01'
   target_filename = input_file + '_cleaned'
   with open(input_filename) as f:
      for line in f:
         line_dict = json.loads(line)
         
         if is_english(line_dict['body']):
            new_dict = {}
            new_dict['comment_string'] = clean(line_dict['body']) 
            new_dict['user_id'] = line_dict['id']
            new_dict['subreddit'] = line_dict['subreddit']
            new_dict['num_upvotes'] = line_dict['score']
            new_dict['month_year'] = '01_2015'

            if r.search('/s$', line_dict['body']) != None:
               new_dict['sarcasm_label'] = 1
            else
               new_dict['sarcasm_label'] = 0

         # output new_dict as csv to targetfile


if __name__ == "__main__": main()
