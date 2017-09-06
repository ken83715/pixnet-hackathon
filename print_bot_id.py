import os
from slackclient import SlackClient

BOT_NAME = 'ICE'

slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))


if __name__ == "__main__":
    api_call = slack_client.api_call("users.list")
    print(os.environ.get('SLACK_BOT_TOKEN'))
    # if api_call.get('ok'):
    #     # retrieve all users so we can find our bot
    #     users = api_call.get('members')
    #     for user in users:
    #         print(user.get('name'))               
    # else:
    #     print("could not find bot user with the name " + BOT_NAME)