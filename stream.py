import dataset
import json
import tweepy
import config

db = dataset.connect(config.CONNECTION_STRING)

auth = tweepy.OAuthHandler(config.CONSUMER_KEY, config.CONSUMER_SECRET)
auth.set_access_token(config.ACCESS_TOKEN, config.ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

# Update with topics to follow
TOPICS = ["baseball", "football"]


class StreamListener(tweepy.StreamListener):
    def on_status(self, status):
        print(status.text)

        description = status.user.description
        loc = status.user.location
        text = status.text
        name = status.user.screen_name
        user_created = status.user.created_at
        followers = status.user.followers_count
        id_str = status.id_str
        created = status.created_at
        retweet_count = status.retweet_count
        friends_count = status.user.friends_count

        # check if retweet, assign attributes
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

        table = db[config.TABLE_NAME]
        table.insert(dict(
            user_description=description,
            user_location=loc,
            text=text,
            user_name=name,
            user_created=user_created,
            user_followers=followers,
            friends_count=friends_count,
            id_str=id_str,
            created=created,
            retweet_count=retweet_count,
            retweet=retweet,
            original_id=None if original_id is None else original_id,
            original_name=None if original_name is None else original_name,
            hashtags=None if hashtags is None else hashtags

        ))

    def on_error(self, status_code):
        '''Twitter is rate limiting, exit'''

        if status_code == 420:
            print('Twitter rate limit error_code {}, exiting...'.format(status_code))
            return False


stream_listener = StreamListener()
stream = tweepy.Stream(auth=api.auth, listener=stream_listener)
stream.filter(track=TOPICS)
