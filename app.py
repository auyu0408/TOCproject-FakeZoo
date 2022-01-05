import os
import sys

from flask import Flask, jsonify, request, abort, send_file, render_template
from dotenv import load_dotenv
from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

from fsm import TocMachine
from urllib.parse import urlparse
from utils import send_text_message
import redis

load_dotenv()

machine = TocMachine(
    states=["demo", "welcome", "place", "zoo", "marine", "picture", "rule1", "rule2", "rule3", "rule4", "rule5",
    "rule6", "rule7", "rule8"],
    transitions=[
        {
            "trigger": "advance",
            "source": "welcome",
            "dest": "place",
            "conditions": "check_place",
        },
        {
            "trigger": "demo",
            "source": "welcome",
            "dest": "demo",
            "conditions": "demo",
        },
        {
            "trigger": "advance",
            "source": ["place", "marine"],
            "dest": "zoo",
            "conditions": "check_zoo",
        },
        {
            "trigger": "advance",
            "source": ["place", "marine"],
            "dest": "marine",
            "conditions": "check_marine",
        },
        {
            "trigger": "advance",
            "source": "zoo",
            "dest": "rule1",
            "conditions": "go_rule1",
        },
        {
            "trigger": "advance",
            "source": "zoo",
            "dest": "rule2",
            "conditions": "go_rule2"
        },
        {
            "trigger": "advance",
            "source": "zoo",
            "dest": "rule3",
            "conditions": "go_rule3"
        },
        {
            "trigger": "advance",
            "source": "zoo",
            "dest": "rule4",
            "conditions": "go_rule4"
        },
        {
            "trigger": "advance",
            "source": "zoo",
            "dest": "rule5",
            "conditions": "go_rule5"
        },
        {
            "trigger": "advance",
            "source": "zoo",
            "dest": "rule6",
            "conditions": "go_rule6"
        },
        {
            "trigger": "advance",
            "source": "zoo",
            "dest": "rule7",
            "conditions": "go_rule7"
        },
        {
            "trigger": "advance",
            "source": "zoo",
            "dest": "rule8",
            "conditions": "go_rule8"
        },
        {
            "trigger": "advance",
            "source": ["marine", "rule1", "rule3", "rule7", "rule8"],
            "dest": "picture",
            "conditions": "go_picture",
        },
        {
            "trigger": "advance",
            "source": ["demo", "rule1", "rule2", "rule3", "rule4", "rule5", "rule6", "rule7", "rule8", "picture"], 
            "dest": "zoo",
            "conditions": "check_zoo"
        },
        {
            "trigger": "advance",
            "source": ["demo", "welcome", "place", "zoo", "marine", "rule1", "rule2", "rule3", "rule4", "rule5", "rule6", "rule7", "rule8", "picture"], 
            "dest": "welcome",
            "conditions": "back_start"
        },
    ],
    initial="welcome",
    auto_transitions=False,
    show_conditions=True,
)

app = Flask(__name__, static_url_path="")


# get channel_secret and channel_access_token from your environment variable
channel_secret = os.getenv("LINE_CHANNEL_SECRET", None)
channel_access_token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN", None)
host=os.environ.get("REDIS_TLS_URL")
password=os.getenv("REDIS_PASSWORD")
url = urlparse(os.environ.get("REDIS_TLS_URL"))
db = redis.Redis(host=url.hostname, port=url.port, username=url.username, password=url.password, ssl=True, ssl_cert_reqs=None)
if channel_secret is None:
    print("Specify LINE_CHANNEL_SECRET as environment variable.")
    sys.exit(1)
if channel_access_token is None:
    print("Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.")
    sys.exit(1)

line_bot_api = LineBotApi(channel_access_token)
parser = WebhookParser(channel_secret)

@app.route("/callback", methods=["POST"])
def callback():
    signature = request.headers["X-Line-Signature"]
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # parse webhook body
    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        abort(400)

    # if event is MessageEvent and message is TextMessage, then echo text
    for event in events:
        if not isinstance(event, MessageEvent):
            continue
        if not isinstance(event.message, TextMessage):
            continue
        if not isinstance(event.message.text, str):
            continue
        user_id = event.source.user_id
        if(db.exists(user_id)==False):
            machine.state = "welcome"
        else:
            machine.state = db.get(user_id).decode("UTF-8")
        print(f"\nFSM STATE: {machine.state}")
        print(f"REQUEST BODY: \n{body}")
        response = machine.advance(event)
        db.set(user_id, machine.state)
        if response == False:
            send_text_message(event.reply_token, "請重新輸入!")

    return "OK"

@app.route("/webhook", methods=["POST"])
def webhook_handler():
    signature = request.headers["X-Line-Signature"]
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info(f"Request body: {body}")

    # parse webhook body
    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        abort(400)

    # if event is MessageEvent and message is TextMessage, then echo text
    for event in events:
        if not isinstance(event, MessageEvent):
            continue
        if not isinstance(event.message, TextMessage):
            continue
        if not isinstance(event.message.text, str):
            continue
        user_id = event.source.user_id
        if(db.exists(user_id)==False):
            machine.state = 'welcome'
        else:
            machine.state = db.get(user_id)
        print(f"\nFSM STATE: {machine.state}")
        print(f"REQUEST BODY: \n{body}")
        response = machine.advance(event)
        db.set(user_id, f"{machine.state}")
        if response == False:
            send_text_message(event.reply_token, "請重新輸入!")

    return "OK"


@app.route("/show-fsm", methods=["GET"])
def show_fsm():
    machine.get_graph().draw("fsm.png", prog="dot", format="png")
    return send_file("fsm.png", mimetype="image/png")


if __name__ == "__main__":
    port = os.environ.get("PORT", 8000)
    app.run(host="0.0.0.0", port=port, debug=True)