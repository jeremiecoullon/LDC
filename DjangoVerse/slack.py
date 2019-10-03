import os
from slack import WebClient
import os

SLACK_TOKEN = os.environ["SLACK_TOKEN"]
slack_client = WebClient(SLACK_TOKEN)



def send_slack_message(message):
	response = slack_client.chat_postMessage(
        channel='#djangoverse',
        text=message)
