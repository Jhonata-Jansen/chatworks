# Facebook Api Integration
import requests
import sys

def set_greeting(greeting):
    return {
        "setting_type": "greeting",
        "greeting":{
            "text": greeting,
        }
    }

def unique_conversations_count(page_access_token):
    r = requests.get("https://graph.facebook.com/v2.8/me/insights/page_messages_feedback_by_action_unique&access_token={}".format(page_access_token))
    return r.text

def get_started_button(action):
    return {
      "setting_type": "call_to_actions",
      "thread_state": "new_thread",
      "call_to_actions":[
        {
          "payload": action
        }
      ]
    }

def persistent_menu(items):
    """
    :param items: tuple of (type, title, url* || payload*)
    :return: JSON object containing the menu
    """
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

    return menu_js



def default_json():
    """
    :return: creates the default json object
    """
    default_js = {
        "recipient": {
            "id": ""
        },
        "message": {},
        "notification_type": "REGULAR"
    }
    return default_js

def msg_action_json(action, mid, seq, receiver):
    """
    :param action: String {typing_on, typing_off, mark_seen}
    :param receiver: Receiver Facebook ID
    :return: This function sends to the receiver the msg text
    """
    msg_js = default_json()
    msg_js["recipient"]["id"] = str(receiver)
    msg_js["sender_action"] = str(action)
    msg_js["mids"] = [str(mid)]
    msg_js["seq"] = str(seq)
    return msg_js

def msg_json(msg, receiver):
    """
    :param msg: String
    :param receiver: Receiver Facebook ID
    :return: This function sends to the receiver the msg text
    """
    msg_js = default_json()
    msg_js["recipient"]["id"] = str(receiver)
    msg_js["message"]["text"] = str(msg)
    return msg_js

def msg_txtwbuttons(msg, possible_responses, receiver):
    """
    :param msg: String
    :param possible_responses: List of tuples w/ the format (type, url, title)
    :param receiver: Receiver Facebook ID
    :return: This function sends to the receiver the msg text
    """
    msg_js = default_json()
    msg_js["recipient"]["id"] = str(receiver)
    msg_js["message"]["attachment"] = {}
    msg_js["message"]["attachment"]["type"] = "template"
    msg_js["message"]["attachment"]["payload"] = {}
    msg_js["message"]["attachment"]["payload"]["text"] = str(msg)
    msg_js["message"]["attachment"]["payload"]["template_type"] = "button"
    msg_js["message"]["attachment"]["payload"]["buttons"] = []

    encoded_buttons = msg_js["message"]["attachment"]["payload"]["buttons"]
    for i in possible_responses:
        button = {}
        button["type"] = i[0]
        button["url"] = i[1]
        button["title"] = i[2]
        encoded_buttons.append(button)

    return msg_js


def msg_linkwbuttons(msg, possible_responses, receiver):
    """
    :param msg: String
    :param possible_responses: List of tuples w/ the format (type, url, )
    :param receiver: Receiver Facebook ID
    :return: This function sends to the receiver the msg text
    """
    msg_js = default_json()
    msg_js["recipient"]["id"] = str(receiver)
    msg_js["message"]["text"] = str(msg)
    return msg_js


def request_maker(request_payload, page_access_token):
    """
    :param request_payload:
    :return: Sends the requisition to FB and checks for reception
    """
    url = "https://graph.facebook.com/v2.6/me/messages?access_token={}".format(page_access_token)
    r = requests.post(url, json=request_payload)
    return r.text

def thread_request_maker(request_payload, page_access_token):
    """
    :param request_payload:
    :return: Sends the requisition to FB and checks for reception
    """
    url = "https://graph.facebook.com/v2.6/me/thread_settings?access_token={}".format(page_access_token)
    r = requests.post(url, json=request_payload)
    return r.text


def chat_actions(action, receiver, page_access_token):
    if action == action:
        request_maker(msg_json(str(action), receiver), page_access_token)
    return True

def check_payload(payload, contentdict):
    return contentdict[payload]

def request_parser(request, page_access_token):
    """
    :param request: Request sent from facebook (message || delivery || read)
    :return: type of request
    """

    contentdict = {
    "start_bot": "IZIIIII"
    }

    full_packet = request["entry"][0]
    msg_info = full_packet["messaging"][0]
    if "message" in msg_info:
        msg = msg_info["message"]
        sender = msg_info["sender"]["id"]
        msg_text = msg["text"]
        seen = msg_action_json("mark_seen", msg["mid"], msg["seq"], sender)
        msg = msg_json(msg_text, sender)
        for i in [seen, msg]:
            request_maker(i, page_access_token)
    if "postback" in msg_info:
        chat_actions(check_payload(msg_info["postback"]["payload"], contentdict), msg_info["sender"]["id"], page_access_token)
        pass
    else:
        pass

    return True
