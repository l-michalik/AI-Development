import sqlite3
import json
from datetime import datetime

timeframe = '2015-05'
sql_transaction = []

connection = sqlite3.connect('{}.db'.format(timeframe))
c = connection.cursor()

def create_table():
  c.execute("""
    CREATE TABLE IF NOT EXISTS parent_reply(
    parent_id TEXT PRIMARY KEY, 
    comment_id TEXT UNIQUE, 
    parent TEXT, 
    comment TEXT, 
    subreddit TEXT, 
    unix INT, 
    score INT)
    """)
  
# def format_data(data):
#   data = data.replace('\n', ' newlinechar ').replace('\r', ' newlinechar ').replace('"', "'")
#   return data

# def find_parent(pid):
#   try:
#     sql = "SELECT comment FROM parent_reply WHERE comment_id = '{}' LIMIT 1".format(pid)
#     c.execute(sql)
#     result = c.fetchone()
#     if result != None:
#       return result[0]
#     else:
#       return False
#   except Exception as e:
#     return False  

if __name__ == '__main__':
  create_table()
  # row_counter = 0
  # paired_rows = 0

  # with open("~/Desktop/AI-Development/chat-bot/RC_{}-05.json".format(timeframe.split('-')[0], timeframe), 'rb') as f:
  #   for row in f:
  #     row_counter += 1
  #     row = json.loads(row)
  #     parent_id = row['parent_id']
  #     body = format_data(row['body'])
  #     created_utc = row['created_utc']
  #     score = row['score']
  #     subreddit = row['subreddit']
  #     parent_data = find_parent(parent_id)

      # if score >= 2:
      #   if acceptable(body):
      #     existing_comment_score = find_existing_score(parent_id)
      #     if existing_comment_score:
      #       if score > existing_comment_score:
      #         sql_insert_replace_comment(comment_id, parent_id, parent, body, subreddit, created_utc, score)
      #     else:
      #       if parent_data:
      #         sql_insert_has_parent(comment_id, parent_id, parent, body, subreddit, created_utc, score)
      #         paired_rows += 1
      #     if row_counter % 100000 == 0:
      #       print('Total Rows Read: {}, Paired Rows: {}, Time: {}'.format(row_counter, paired_rows, str(datetime.now())))
