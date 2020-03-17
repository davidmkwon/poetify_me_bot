# Used libaries
import config
import praw
from poem_generation import generate_raw_poem, rhyme_poem

reddit = praw.Reddit(user_agent=config.USER_AGENT,
                            client_id=config.CLIENT_ID,
                            client_secret=config.CLIENT_SECRET,
                            username=config.USERNAME,
                            password=config.PASSWORD)

monitor_subreddits = ['testingground4bots']

bot_call = 'u/poetify_me_bot'

bot_name = 'i-am-fruit-snack'

def run():
    '''
    This method ...
    '''

    for subreddit_title in monitor_subreddits:
        subreddit = reddit.subreddit(subreddit_title)

        for submission in subreddit.new(limit=5):
            print(submission.id)
            reply_to_submission_comments(submission)

def reply_to_submission_comments(submission):
    '''
    This method iterates through the comments of the given submission, delegating to
    the reply_to_comment method that will recursively check down the reponse thread of
    each comment, and reply accordingly
    '''
    
    submission_pointer = submission
    submission_pointer.comment_sort = 'new'
    for comment in submission_pointer.comments:
        reply_to_comment(comment)

def generate_poem():
    '''
    This method genertes and returns a randomly rhymed poem using the corresponding
    methods from poem_generation
    '''

    raw_poem = generate_raw_poem()
    rhymed_poem = rhyme_poem(raw_poem)
    return rhymed_poem

def generate_reply():
    '''
    This method generates a poem and returns a response that can be used to reply to a reddit
    comment that mentions the bot
    '''

    poem = generate_poem()
    poem_str_1 = ' '.join(word for word in poem[0])
    poem_str_2 = ' '.join(word for word in poem[1])

    reply = 'A randomly generated poem, just for you: \n\n{}\n\n{}\n\nI am a bot. Summon me with {}'.format(poem_str_1, poem_str_2, bot_call)
    return reply

def reply_to_comment(comment):
    '''
    This method recursively checks if a comment, or any of it's replies (children), contain
    the mention of the bot. If so, the method will reply with a randomly generated reply.
    '''

    if comment.author and comment.body != '[deleted]':
        if comment.author.name != bot_name and bot_call in comment.body:
            reply = generate_reply()
            comment.reply(reply)

    if comment.replies:
        for comment_reply in comment.replies:
            reply_to_comment(comment_reply)

if __name__ == "__main__":
    run()








