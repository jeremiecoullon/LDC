import os
from slack import WebClient
import os

SLACK_TOKEN = os.environ["SLACK_TOKEN"]
slack_client = WebClient(SLACK_TOKEN)



# def list_channels():
#     channels_call = slack_client.api_call("channels.list")
#     if channels_call['ok']:
#         return channels_call['channels']
#     return None

def send_slack_message(message):
	response = slack_client.chat_postMessage(
        channel='#djangoverse',
        text=message)

# def send_slack_message(channel_id, message):
#     slack_client.api_call(
#         "chat.postMessage",
#         channel=channel_id,
#         text=message,
#         username='djangoverse_additions',
#         icon_emoji=':robot_face:'
#     )

# def send_feedback_to_slack(message='bige', channel_name='djangoverse'):
#     channels = list_channels()
#     for channel in channels:
#         if channel['name'] == channel_name:
#             send_slack_message(channel_id=channel['id'], message=message)