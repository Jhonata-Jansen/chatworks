# ChatWorks

ChatWorks is a chatbot creation framework which is based on Facebook, Telegram and Slack(last two are coming soon).
ChatWorks require a web requests processor such as Flask, Django or any other software supporting http requests.
Here, we will use Flask as a requests processor.

## Requirements

To install the necessary tools to work on chatworks:

```
python -m pip install -r requirements.txt
```

## Examples

This is an example of a Facebook bot on Flask:
```python
from flask import Flask, request
from chatworks.platform.facebook import *

app = Flask(__app__)

@app.route("/", methods=["GET", "POST"]) # We need to be able to process both of the requests
def main():
      if request.method == "GET":
        if request.get_json() == None:
            return "It work's"
        if request.values["verify_token"]:
            return request.values["hub.challenge"] # Here we define the facebook webhook challenge response
    else:
        if config("debug_enabled", default=False, cast=bool):
            print(request.get_json(), file=sys.stderr)
        request_parser(request.get_json(), page_access_token) # here we process the requests
        return "It work's"

