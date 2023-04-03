import json
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


def parse_tweet(tweet):
    try:
        logger.info(f"tweet {tweet}")
        # j_data = json.loads(tweet)
        # medias = tweet["includes"]["media"]
        includes = tweet.includes
        tweet_infos = tweet.data
        tweet_id = tweet_infos[0].get("id")
        users = includes.get("users")
        tweet_username = users[0].get("username")
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
            media_infos = {"media_type": media_type, "content_type": content_type, "url": url, "tweet_id": tweet_id, "author_username" : tweet_username}
            media_list.append(media_infos)
            urls.add(url)
            return media_list
    except (KeyError, AttributeError):
        return None
