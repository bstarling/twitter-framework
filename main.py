import dataset
from datetime import datetime
import json
import os
import sys
import tweepy
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError

from logger import LOGGER as l
from credentials import CONSUMER_KEY, CONSUMER_SECRET, ACCESS_KEY, ACCESS_SECRET


def create_datetime(timestamp):
    """Helper function create datetime for mongo load"""

    try:
        timestamp = datetime.strptime(timestamp, '%a %b %d %H:%M:%S %z %Y')
    except Exception as e:
        l.warn('Could not convert created_at {}\n{}'.format(timestamp, e))
        return None


def mongo_preprocessor(status):
    """Get tweet in JSON format"""

    tweet = status.__dict__['_json']
    tweet['created_at'] = create_datetime(tweet['created_at'])
    return tweet


def sqlite_preprocessor(status):
    """Map tweet to db fields"""

    # Check if retweet
    if hasattr(status, 'retweeted_status'):
        retweet = 'Y'
        original_id = status.retweeted_status.user.id
        original_name = status.retweeted_status.user.name
    else:
        retweet = 'N'
        original_id = None
        original_name = None

    # check for hashtags and save as list
    if hasattr(status, 'entities'):
        hashtags = []
        for tag in status.entities['hashtags']:
            hashtags.append(tag['text'])
        hashtags = json.dumps(hashtags)

    tweet = dict(
        description=status.user.description,
        loc=status.user.location,
        text=status.text,
        name=status.user.screen_name,
        user_created=status.user.created_at,
        followers=status.user.followers_count,
        id_str=status.id_str,
        created=status.created_at,
        retweet_count=status.retweet_count,
        friends_count=status.user.friends_count,
        source=status.source,
        retweet=retweet,

        # do not exist for every tweet
        original_id=None if original_id is None else original_id,
        original_name=None if original_name is None else original_name,
        hashtags=None if hashtags is None else hashtags,
        )
    return tweet


class StreamListener(tweepy.StreamListener):
    def __init__(self, api=None, connection_string=None, table='tweet', verbose=False):
        super(StreamListener, self).__init__()
        self.counter = 0
        self.batch_size = 10
        self.verbose = verbose
        self.tweet_list = []
        self.start = datetime.utcnow()
        self.setup_backend(connection_string, table)

    def setup_backend(self, db, table):
        db_type = db.split(":")[0]
        if db_type == 'mongodb':
            self.client = MongoClient(db)
            self.db = self.client.twitter
            self.table = self.db[table]
            self.backend = db_type
        elif db_type == 'sqlite':
            self.db = dataset.connect(db)
            self.table = self.db[table]
            self.backend = db_type

        else:
            # unable to parse connection string
            l.warning("{} is no a not supported back end\nConnection string: {}".format(db_type, db))
            sys.exit(1)

    def on_status(self, status):
        self.counter += 1
        if self.verbose:
            l.info(status.text)
        self.tweet_list.append(status)

        if self.counter >= self.batch_size:
            td = datetime.utcnow() - self.start
            l.info("Batch time elapsed: {}".format(td))
            self.save_tweets()
            self.reset()

    def reset(self):
        # reset batch counter
        self.counter = 0
        self.tweet_list = []
        self.start = datetime.utcnow()

    def on_error(self, status_code):
        l.warn('Error {}'.format(status_code))

    def save_tweets(self):
        bulk_insert = []
        if self.backend == 'mongodb':
            for tweet in self.tweet_list:
                tweet = mongo_preprocessor(tweet)
                bulk_insert.append(tweet)
            try:
                self.table.insert_many(bulk_insert)
                l.info("Batch complete. Saved {} tweets to db".format(self.counter))
            except DuplicateKeyError as e:
                l.info("{}".format(e))
            except Exception as e:
                l.warn("Unable to save to DB\n{}".format(e))

        elif self.backend == 'sqlite':
            bulk_insert = []
            for tweet in self.tweet_list:
                try:
                    tweet = sqlite_preprocessor(tweet)
                except Exception as e:
                    l.warn("unable to map {}".format(tweet))
                    continue
                bulk_insert.append(tweet)
            try:
                self.table.insert_many(bulk_insert)
                l.info("Batch complete. Saved {} tweets to db".format(len(bulk_insert)))
            except Exception as e:
                # Better to miss a few tweets and keep script running
                l.warn("Unable to save to DB {}".format(e))


def run(**kwargs):
    l.info("Twitter API Keys\nCONSUMER_KEY:{}\nCONSUMER_SECRET:{}\nACCESS_KEY:{}\nACCESS_SECRET:{}\n".format(
        CONSUMER_KEY, CONSUMER_SECRET, ACCESS_KEY, ACCESS_SECRET))

    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
    api = tweepy.API(auth)

    stream_listener = StreamListener(
        connection_string=kwargs['db'], table=kwargs['name'], verbose=kwargs['verbose'])
    stream = tweepy.Stream(auth=api.auth, listener=stream_listener)
    stream.filter(track=kwargs['topics'])
