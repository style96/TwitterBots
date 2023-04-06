# tweepy-bots/bots/config.py
import tweepy
import logging
import os
from utils.credentials import CONSUMER_KEY, CONSUMER_SECRET, BEARER_TOKEN, ACCESS_TOKEN, ACCESS_TOKEN_SECRET

logger = logging.getLogger()

CONSUMER_KEY = os.getenv("CONSUMER_KEY") if os.getenv("CONSUMER_KEY") is not None else CONSUMER_KEY
CONSUMER_SECRET = os.getenv("CONSUMER_SECRET") if os.getenv("CONSUMER_SECRET") is not None else CONSUMER_SECRET
BEARER_TOKEN = os.getenv("BEARER_TOKEN") if os.getenv("BEARER_TOKEN") is not None else BEARER_TOKEN
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN") if os.getenv("ACCESS_TOKEN") is not None else ACCESS_TOKEN
ACCESS_TOKEN_SECRET = os.getenv("ACCESS_TOKEN_SECRET") if os.getenv("ACCESS_TOKEN_SECRET") is not None else ACCESS_TOKEN_SECRET

def create_api():
    consumer_key = CONSUMER_KEY
    consumer_secret = CONSUMER_SECRET
    bearer_token = BEARER_TOKEN
    access_token = ACCESS_TOKEN
    access_token_secret = ACCESS_TOKEN_SECRET

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth, wait_on_rate_limit=True)
    try:
        api.verify_credentials()
    except Exception as e:
        logger.error("Error creating API", exc_info=True)
        raise e
    logger.info("API created")
    return api


def create_client():
    consumer_key = CONSUMER_KEY
    consumer_secret = CONSUMER_SECRET
    bearer_token = BEARER_TOKEN
    access_token = ACCESS_TOKEN
    access_token_secret = ACCESS_TOKEN_SECRET
    # Gainaing access and connecting to Twitter API using Credentials
    client = tweepy.Client(
        bearer_token=bearer_token,
        consumer_key=consumer_key,
        consumer_secret=consumer_secret,
        access_token=access_token,
        access_token_secret=access_token_secret,
        wait_on_rate_limit=True,
    )
    return client


def create_streaming_client():
    bearer_token = BEARER_TOKEN
    # Gainaing access and connecting to Twitter API using Credentials
    streaming_client = tweepy.StreamingClient(bearer_token)
    return streaming_client
