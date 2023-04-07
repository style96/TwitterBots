FROM python:3.10.6-alpine3.16

COPY bots/config.py /bots/
COPY bots/mentionChecker.py /bots/
COPY bots/rules.py /bots/
COPY bots/parse_tweet.py /bots/
COPY bots/utils/constants.py /bots/utils/
COPY bots/utils/credentials.py /bots/utils/

COPY requirements.txt /tmp
RUN pip3 install -r /tmp/requirements.txt

WORKDIR /bots
CMD ["python3", "mentionChecker.py"]