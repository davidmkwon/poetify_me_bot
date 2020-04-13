# Used libraries
from poem_generation import *
import pronouncing
import random
from nltk.corpus import wordnet as wn
import praw
import config

reddit = praw.Reddit(user_agent=config.USER_AGENT,
                            client_id=config.CLIENT_ID,
                            client_secret=config.CLIENT_SECRET,
                            username=config.USERNAME,
                            password=config.PASSWORD)

subreddit = reddit.subreddit('testingground4bots')

'''
for submission in subreddit.new(limit=5):
    submission_pointer = submission
    submission_pointer.comment_sort = 'new'

    for comment in submission_pointer.comments:
        rep = '{}:author, {}:body'.format(comment.author, comment.body)
        print(rep)
'''

submission = reddit.submission('fjtxfk')
for comment in submission.comments:
    # print(comment.body)
    # print(len(comment.replies))
    try:
        if comment.author.name == 'turdyturdle':
            comment.reply('hi\n\nhi \n\n hi\n\nhi')
    except:
        pass
