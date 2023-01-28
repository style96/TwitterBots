#!/usr/bin/env python
# tweepy-bots/bots/mentionChecker.py

import tweepy
import logging
from config import create_api, create_client, create_streaming_client
import json
import rules
from time import sleep
from urllib import request

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

client = create_client()
streaming_client = create_streaming_client()
api = create_api()


class MentionTweetListener(tweepy.StreamingClient):

    # This function gets called when the stream is working
    def on_connect(self):
        logger.info("Connected")
        self.me_id = client.get_me().data.id
        self.me_username = client.get_me().data.username
        logger.info(self.me_id)

    def on_data(self, raw_data):
        try:
            logger.info(f"raw data {raw_data}")
            j_data = json.loads(raw_data)
            medias = j_data["includes"]["media"]
            urls = set()
            media_list = []
            media_infos = dict()
            for media in medias:
                media_type = media.get("type")
                content_type = None
                if "variants" in media:
                    variants = media.get("variants")
                    # get first and highest quality variant
                    url = variants[0]["url"] if variants else None
                    content_type = variants[0]["content_type"] if variants else None
                else:
                    url = media.get("url")
                media_infos = {"media_type": media_type, "content_type": content_type, "url": url}
                media_list.append(media_infos)
                urls.add(url)
                logger.info(urls)
        except (KeyError, AttributeError):
            pass
        return super().on_data(raw_data)

    def on_tweet(self, tweet):
        logger.info(f"Processing tweet id {tweet.id}")
        logger.info(f"Processing tweet properties {tweet}")
        if tweet.author_id == self.me_id:
            logger.info("botun attiği tweet")
            return
        if tweet.referenced_tweets == None:
            return
        if isMentionedMe(tweet, self.me_username) is not True:
            logger.info("tweet did not mention me.")
            return
        logger.info(tweet.referenced_tweets)
        referenced_tweet_ids = []
        for referenced_tweet in tweet.referenced_tweets:
            logger.info(referenced_tweet.id)
            referenced_tweet_ids.append(referenced_tweet.id)
        response = client.get_tweets(
            referenced_tweet_ids,
            expansions=["attachments.media_keys", "author_id"],
            media_fields=[
                "media_key",
                "type",
                "duration_ms",
                "public_metrics",
                "width",
                "height",
                "preview_image_url",
                "alt_text",
                "url",
                "variants",
            ],
            tweet_fields=["created_at"],
        )
        media_list = parse_tweet(response)
        logger.debug(media_list)
        for media in media_list:
            if(media.get("media_type") == 'video'):
                request.urlretrieve(media.get("url"),f'/home/halil/Projects/twitter_bots/depo/medias/python1.mp4')
        
        #isUrlExist(tweet=tweet)  # kaldırılacak , calısmıyor
        # reply tweet
        # response = client.create_tweet(
        #     text="Thanks for mentioning me!", in_reply_to_tweet_id=tweet.id, exclude_reply_user_ids=[self.me_id]
        # )
        # logger.info(response)

        sleep(0.2)

    def on_error(self, status):
        logger.error(status)


#parse tweet
def parse_tweet(tweet):
    try:
        logger.info(f"tweet {tweet}")
        #j_data = json.loads(tweet)
        #medias = tweet["includes"]["media"]
        includes = tweet.includes
        medias = includes.get("media")
        urls = set()
        media_list = []
        media_infos = dict()
        for media in medias:
            media_type = media.get("type")
            content_type = None
            if "variants" in media:
                variants = media.get("variants")
                # get first and highest quality variant
                url = variants[0]["url"] if variants else None
                content_type = variants[0]["content_type"] if variants else None
            else:
                url = media.get("url")
            media_infos = {"media_type": media_type, "content_type": content_type, "url": url}
            media_list.append(media_infos)
            urls.add(url)
            return media_list
    except (KeyError, AttributeError):
        return None
# check
def isUrlExist(tweet):
    try:
        logger.info(f"entities tweet properties {tweet.entities}")
        urls = tweet.entities.get("urls")
        medias = []
        for url in urls:
            medias.append(url.get("expanded_url"))
        logger.info(medias)
    except AttributeError:
        return False
    return True


# check whether mentioned or not
def isMentionedMe(tweet, username):
    if tweet.entities is not None:
        logger.info(f"entities tweet properties {tweet.entities}")
        mentions = tweet.entities.get("mentions")
        mentioned_usernames = []
        if mentions is None:
            return None
        for mention in mentions:
            mentioned_usernames.append(mention.get("username"))
        logger.info(mentioned_usernames)
        if username not in mentioned_usernames:
            return False
        return True


# get rules
def get_rules():
    rules = streaming_client.get_rules()
    logger.info(f"Stream rules: {rules} ")
    return rules.data


# delete rules
def delete_rules(rules):
    if rules is None:
        return None

    # I don´t know why it works, but it works
    # If you know a better way for tuple unpacking here let me know on github
    # [StreamRule(value='radix OR #radix -is:retweet -is:quote', tag='radix', id='1555500321245462528'), ...
    for a, b, c in rules:
        response = streaming_client.delete_rules(ids=c)
        logger.info(f"{response} Name: {a}")


# set rules
def set_rules():
    rule_value = rules.search_rules[rules.rule_number]["value"]
    rule_tag = rules.search_rules[rules.rule_number]["tag"]
    search_rules = tweepy.StreamRule(value=rule_value, tag=rule_tag)
    response = streaming_client.add_rules(search_rules)
    logger.info(f"Set rule: {response}")


def main():
    stream = MentionTweetListener(streaming_client.bearer_token)
    rules = get_rules()
    delete_rules(rules)
    set_rules()
    # Starting stream
    stream.filter(
        expansions=["attachments.media_keys", "author_id"],
        media_fields=[
            "media_key",
            "type",
            "duration_ms",
            "public_metrics",
            "width",
            "height",
            "preview_image_url",
            "alt_text",
            "url",
            "variants",
        ],
        tweet_fields=["referenced_tweets", "entities"],
    )


if __name__ == "__main__":
    main()
