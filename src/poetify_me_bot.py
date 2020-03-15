# Used libaries
import config
import praw

reddit = praw.Reddit(config.USER_AGENT,
                    config.CLIENT_ID,
                    config.CLIENT_SECRET,
                    config.USERNAME,
                    config.PASSWORD)