#!/usr/bin/env python
# tweepy-bots/bots/mentionChecker.py

import time
import tweepy
import logging
from config import create_api, create_client, create_streaming_client
import json
import rules
from time import sleep
from urllib import request
import requests
from parse_tweet import parse_tweet
from utils.constants import expansions, media_fields, tweet_fields, user_fields

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

client = create_client()
streaming_client = create_streaming_client()
api = create_api()

def get_media_list(referenced_tweet_ids, tweet):
    response = client.get_tweets(
        referenced_tweet_ids,
        expansions=expansions,
        media_fields=media_fields,
        tweet_fields=tweet_fields,
        user_fields=user_fields,
    )
    media_list = parse_tweet(response)
    if media_list is None:
        return
    for media in media_list:
        if media.get("media_type") == "video":
            media.update({"requested_username": tweet.author_id})  # TODO self kaldırılacak yerine tweet id konulacak.
            logger.info(f"media : {media}")
            j_media = json.dumps(media)
            s_tweet_id = str(media.get("tweet_id"))
            myObj = {"title": s_tweet_id, "content": j_media, "slug": s_tweet_id, "status": "publish"}
            url = "https://kodlamayabasla.com/wp-json/wp/v2/tweets"
            login_id = "style93"
            login_pwd = "xeAX hBWC 5wwm umrw jQbq rcl3"
            logger.info(f"Download link is https://kodlamayabasla.com/tweets/{s_tweet_id}")
            try: 
                r = requests.get(url + "?_fields=slug", auth=(login_id, login_pwd))
                logger.info(f"r.status_code : {r.status_code}")
                if r.status_code == 200:
                    r_json = r.json()
                    for slug in r_json:
                        logger.info(f"slug : {slug['slug']}")
                        if slug["slug"] == s_tweet_id:
                            response = client.create_tweet(
                                text=f"Download link is https://kodlamayabasla.com/tweets/{s_tweet_id}",
                                in_reply_to_tweet_id=tweet.id,
                                exclude_reply_user_ids=[1617475758951112704],
                            )
                            logger.info(response)
                            return
            except Exception as e:
                # TODO error exception
                logger.info(f"exeption on get tweets request : {e}")
                return

            try:
                r = requests.post(url, json=myObj, auth=(login_id, login_pwd))
                logger.info(f"r.ok : {r.ok}")
                if r.ok == True:
                    # reply tweet
                    response = client.create_tweet(
                        text=f"Download link is https://kodlamayabasla.com/tweets/{s_tweet_id}",
                        in_reply_to_tweet_id=tweet.id,
                        exclude_reply_user_ids=[1617475758951112704],
                    )
                    logger.info(response)
            except Exception as e:
                # TODO error exception
                logger.info(f"exeption on create tweet request : {e}")
                return
            # request.urlretrieve(media.get("url"),f'/home/halil/Projects/twitter_bots/depo/medias/python1.mp4') #download link


def check_mentions(api, keywords, last_mention_id):
    try:
        logger.info("Retrieving mentions")
        # Get new tweets
        mentions = api.get_users_mentions(
            1617475758951112704,
            since_id=last_mention_id,
            expansions=expansions,
            media_fields=media_fields,
            tweet_fields=tweet_fields,
            user_fields=user_fields,
        )
        # Iterate through mentions and reply to each mention
        for mention in reversed(mentions[0]):
            if mention.id > last_mention_id:
                last_mention_id = max(mention.id, last_mention_id) ## Moved from bottom to top of loop. because of when server is unavailable drop in infine loop.
                logger.info("last mention id : " + str(last_mention_id))
                logger.info(f"mention.id : {mention.id}")
                if any(keyword in mention.text.lower() for keyword in keywords):
                    referenced_tweet_ids = []
                    for referenced_tweet in mention.referenced_tweets:
                        logger.info(referenced_tweet.id)
                        if referenced_tweet["type"] == "replied_to":
                            referenced_tweet_ids.append(referenced_tweet.id)
                    get_media_list(referenced_tweet_ids=referenced_tweet_ids, tweet=mention)
                    logger.info(f"Answering to {mention.author_id}")
                    print(mention.text)
                    
        return last_mention_id
    except:
        return last_mention_id


def main():
    bearer_token = streaming_client.bearer_token
    client = tweepy.Client(streaming_client.bearer_token)
    last_mention_id = 1

    mentions = client.get_users_mentions(
        1617475758951112704,
        since_id=last_mention_id,
        expansions=expansions,
        media_fields=media_fields,
        tweet_fields=tweet_fields,
        user_fields=user_fields,
    )
    print(mentions)

    for mention in mentions[0]:
        last_mention_id = max(mention.id, last_mention_id)

    keywords = ["download"]
    while True:
        last_mention_id = check_mentions(client, keywords, last_mention_id)
        logger.info("last mention id : " + str(last_mention_id))
        logger.info("Waiting...")
    
        time.sleep(60)
        


if __name__ == "__main__":
    main()
