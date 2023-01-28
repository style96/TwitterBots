#!/usr/bin/env python
# tweepy-bots/bots/mentionChecker.py

import tweepy
import logging
from config import create_api
import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


def check_mentions(api, keywords, last_mention_id):
    logger.info("Retrieving mentions")
    # Get new tweets
    mentions = api.mentions_timeline(since_id=last_mention_id)
    # Iterate through mentions and reply to each mention
    for mention in reversed(mentions):
        if mention.in_reply_to_status_id is not None:
            continue
        if mention.id > last_mention_id:
            if any(keyword in mention.text.lower() for keyword in keywords):
                logger.info(f"Answering to {mention.user.name}")	
                print(mention.text)
                last_mention_id = max(mention.id, last_mention_id)
                api.update_status(
                    status="Thanks for mentioning me!",
                    in_reply_to_status_id=mention.id,
                )
    return last_mention_id


def main():
    api = create_api()
    last_mention_id = 1
    # Get new tweets
    mentions = api.mentions_timeline(since_id=last_mention_id)
    for mention in mentions:
        last_mention_id = max(mention.id, last_mention_id)
    keywords = ["download"]
    while True:
        last_mention_id = check_mentions(api, keywords, last_mention_id)
        logger.info("Waiting...")
        time.sleep(60)


if __name__ == "__main__":
    main()
