import os

# Twitter API credentials if not using ENV variables
# Add credentials here:
CONSUMER_KEY = ""
CONSUMER_SECRET = ""
ACCESS_KEY = ""
ACCESS_SECRET = ""


# DO NOT CHANGE
# Check for twitter credentials in ENV variable first falls back on what is entered above
CONSUMER_KEY = os.getenv('T_CONSUMER_KEY', CONSUMER_KEY)
CONSUMER_SECRET = os.getenv('T_CONSUMER_SECRET', CONSUMER_KEY)
ACCESS_KEY = os.getenv('T_ACCESS_KEY', CONSUMER_KEY)
ACCESS_SECRET = os.getenv('T_ACCESS_SECRET', CONSUMER_KEY)