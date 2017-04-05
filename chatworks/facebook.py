import sys
import requests

class FacebookMessenger():

    def __init__(self, page_access_token):
        self.page_access_token = page_access_token
        self.actions = ["mark_seen", "typing_on", "typing_off"]

    def _simple_request_maker(self, payload):
        url = "https://graph.facebook.com/v2.6/me/messages?access_token={}".format(self.page_access_token)
        r = requests.post(url, json=payload)
        return r.text

    def _thread_request_maker(self, payload):
        url = "https://graph.facebook.com/v2.6/me/thread_settings?access_token={}".format(page_access_token)
        r = requests.post(url, json=request_payload)
        return r.text

    def _default_json(self, recipient):
        default_js = {
            "recipient": {
                "id": recipient
            }
        }
        return default_js

    def set_greeting(self, greeting):
        greeting = {
            "setting_type": "greeting",
            "greeting":{
                "text": greeting,
            }
        }
        self._simple_request_maker(greeting)
        return True

    def set_get_started(self, action):
        get_started_js = {
          "setting_type": "call_to_actions",
          "thread_state": "new_thread",
          "call_to_actions":[
            {
              "payload": action
            }
          ]
        }
        self._simple_request_maker(get_started_js)
        return True

    def set_persistent_menu(items):
        menu_js = {}
        menu_js["locale"] = "default"
        menu_js["composer_input_disabled"] = "true"
        menu_js["call_to_actions"] = []

        for item in items:
            dic_item = {}
            dic_item["type"] = item[0] # Mandatory
            dic_item["title"] = item[1] # Mandatory
            if item[0] == "web_url":
                dic_item["url"] = item[2]
            else:
                dic_item["payload"] = item[2]
            menu_js["call_to_actions"].append(dic_item)

        self._thread_request_maker(menu_js)
        return True

    def _message(self, recipient):
        base = self._default_json(recipient)
        base["message"] = {}
        base["notification_type"] = "REGULAR"
        return base

    def message_simple(self, recipient, message):
        msg = self._message(recipient)
        msg["message"]["text"] = str(message)
        self._simple_request_maker(msg)
        return msg

    def message_wbuttons(self, recipient, responses):
        msg = self._message(recipient)
        msg["message"]["attachment"] = {}
        msg["message"]["attachment"]["type"] = "template"
        msg["message"]["attachment"]["payload"] = {}
        msg["message"]["attachment"]["payload"]["text"] = str(msg)
        msg["message"]["attachment"]["payload"]["template_type"] = "button"
        msg["message"]["attachment"]["payload"]["buttons"] = []

        encoded_buttons = msg["message"]["attachment"]["payload"]["buttons"]
        for i in responses:
            button = {}
            button["type"] = i[0]
            button["url"] = i[1]
            button["title"] = i[2]
            encoded_buttons.append(button)

        self._simple_request_maker(msg)
        return True

    def set_chat_action(self, action, recipient):
        if action in self.actions:
            req = self._default_json(recipient)
            req["sender_action"] = str(action)
            self._simple_request_maker(req)
            return True
        return False
