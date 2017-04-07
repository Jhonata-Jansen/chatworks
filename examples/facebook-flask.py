from chatworks import facebook
from flask import Flask

app = Flask("__app__")

@app.route("/")
def request_receiver():
    return "<h1>This is the return endpoint</h1>"

if __app__ == "__main__":
    app.run(host="0.0.0.0")
