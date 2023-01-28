FROM python:3.10.6-alpine3.16

COPY bots/config.py /bots/
COPY bots/mentionChecker_stream.py /bots/
COPY bots/rules.py /bots/
COPY requirements.txt /tmp
RUN pip3 install -r /tmp/requirements.txt

WORKDIR /bots
CMD ["python3", "mentionChecker_stream.py"]