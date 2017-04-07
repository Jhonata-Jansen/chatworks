# Base code to integrate with Telegram
import requests
import sys

class Telegram():
    def __init__(self, webhook_url):
        self.webhook_url = webhook_url

    def _send_request(self, action_tapi, payload):
        # Check how the request need to be sent

    
