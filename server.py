from os import environ
from flask import Flask
import bots.dedicated.mentionChecker_stream

app = Flask(__name__)

@app.route("/")
def home():
    mentionChecker_stream.main()
    return "Tweeting weather and a quote..."

app.run(host='0.0.0.0', port=environ.get('PORT'))
