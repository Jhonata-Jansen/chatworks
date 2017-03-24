from flask import Flask, request
import sys
from decouple import config
from platforms.facebook import *

page_access_token = config('page_access_token')
url = config('url_default')
setup = config('first_time', default=False, cast=bool)
dbg = config('debug_enabled', default=False, cast=bool)

if setup:
    a = set_greeting("Define your greeting here") # Define a greeting
    b = get_started_button("start_bot") # Define an id to be sent when Get Started button is pressed, so the bot can get started
    c = persistent_menu([("postback", "title1", "teste123")]) # Define a persistent menu for the chatbot

    set_list = [a,b,c]
    for item in set_list:
        thread_request_maker(item, page_access_token)

app = Flask(__name__)

@app.route(url, methods=["POST", "GET"])
def hello():
    if request.method == "GET":
        if request.get_json() == None:
            return "It work's"
        if request.values["verify_token"]:
            return request.values["hub.challenge"]
    else:
        if config("debug_enabled", default=False, cast=bool):
            print(request.get_json(), file=sys.stderr)
        request_parser(request.get_json(), page_access_token)
        return "It work's"




if __name__ == "__main__":
    app.run(debug=dbg)
