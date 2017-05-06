# Twitter streaming framework

This is a small python script plus CLI which can be used to stream tweets to sqlite or mongo database.

### CLI
Called from command line via `stream.py`
* `-D --db` : Connection URI used by sqlite or mongo driver. For more information check dataset docs (sqlite back end) [here](http://dataset.readthedocs.io/en/latest/quickstart.html) or mongodb documentation [here](http://api.mongodb.com/python/current/tutorial.html)
* `-N` `--name` : Name of the table/collection to store tweets. Defaults to `tweet`
* `-T` `--topics` : List of topics to follow.
* `-V` `--verbose`: Prints tweet text to screen/logs

### Example usage:
`python stream.py --topics summer, winter --verbose` will start a collector following the topics `winter, summer` by default data is saved in a sqlite db named `twitter.db` in the current working directory.


`python stream.py --name new -D mongodb://localhost:27017/ -N macrongate -T spring, fall --verbose` to start a collector using mongodb back end. By default tweets are saved to twitter db / tweet collection.

### Requirements
* Written using Python 3.6.1, I have not tested with any other versions.
* Run `pip install -r requirements.txt` to install required packages.

### API Credentials
By default the script will pull twitter API credentials from these environment variables `T_CONSUMER_KEY, T_CONSUMER_SECRET, T_ACCESS_KEY, T_ACCESS_SECRET`. You can set environment variables by running the below commands or adding to your `bash_profile`

```bash
 export T_CONSUMER_KEY='your-key'
 export T_CONSUMER_SECRET='your-secret'

 export T_ACCESS_KEY='access-key'
 export T_ACCESS_SECRET='access-secret'
 ```

If you prefer, you can manually set credentials in the `credentials.py` file

### License
MIT
