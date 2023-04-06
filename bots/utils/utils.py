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
