# twitter-framework

#### Example script to stream tweets to sqlite database

### Instructions
* Create environment and install dependencies using `requirements.txt` (pip) or `environment.yml` (conda)
* Change name of config_ex.py to config.py (actual config file should be excluded from git)
* Update constants in config file with twitter API tokens and keys.
* Update database name & table constants if desired
* Update `TOPICS` constant in `stream.py` with topics you would like to stream ex `TOPICS = ["baseball", "football"]`
* Run `python stream.py` from command line.
* Stream should continue to run unless you receive a 420 (rate limit error) from twitter API
* Data for chosen fields will be streamed to sqlite db in `data` folder

I have chosen specific fields to store but any field defined in the twitter/tweepy API can be added to stream. The combination of sqlite & `dataset` lets you easily configure new fields.

Thanks to [tweepy](https://github.com/tweepy/tweepy) and [dataset](https://github.com/pudo/dataset) for making this a breeze.
