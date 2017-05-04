# Base code to integrate with RocketChat
import os
import sys
import requests

class WebHookNotifier():
    def __init__(self, channel_hook_url):
        self.channel_webhook = channel_hook_url

    def _message(self):
        return {"text":""}

    def _send_request(self, payload):
        requests.post(self.channel_webhook, payload)

    def send_message(self, text):
        msg = self._message()
        msg["text"] = text
        self._send_request(msg)
