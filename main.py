# from https://github.com/slackapi/bolt-python/blob/main/examples/heroku/main.py

import logging

import App

logging.basicConfig(level=logging.DEBUG)
app = App()


@app.command("/hello-bolt-python-heroku")
def hello(body, ack):
    user_id = body["user_id"]
    ack(f"Hi <@{user_id}>!")


from flask import Flask, request
from slack_bolt.adapter.flask import SlackRequestHandler

flask_app = Flask(__name__)
handler = SlackRequestHandler(app)


@flask_app.route("/slack/events", methods=["POST"])
def slack_events():
    return handler.handle(request)