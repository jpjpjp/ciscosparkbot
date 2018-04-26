# -*- coding: utf-8 -*-
"""
Sample webex teams bot using the cicsosparkapi python sdk
"""

import os
from ciscosparkbot import SparkBot

# Retrieve required details from environment variables
bot_email = os.getenv("SPARK_BOT_EMAIL")
spark_token = os.getenv("SPARK_BOT_TOKEN")
bot_url = os.getenv("SPARK_BOT_URL")
bot_app_name = os.getenv("SPARK_BOT_APP_NAME")

# Create a new bot
# Let's check if the user wants us to talk to a specific
# Spark API endpoint.  This can be useful if testing with an emulator
if os.getenv("SPARK_API_URL"):
    bot = SparkBot(bot_app_name, spark_bot_token=spark_token,
                   spark_api_url=os.getenv("SPARK_API_URL"),
                   spark_bot_url=bot_url, spark_bot_email=bot_email, debug=True)
else:
    bot = SparkBot(bot_app_name, spark_bot_token=spark_token,
                   spark_bot_url=bot_url, spark_bot_email=bot_email, debug=True)

# Define the commands
# (note that /help is created automatically in the SparkBot framework)

def hello(incoming_msg, the_bot):
    """
    Respond to a /hello message
    :param incoming_msg: The incoming message object from Spark
    :param the_bot: The bot which includes our spark api instance
    :return: A text or markdown based reply, and the format to send it in
    """
    # lets get the info about who sent this message
    sender = the_bot.spark.people.get(incoming_msg.personId)
    response = "{}, you said hello to me!".format(sender.displayName)
    return response, "text"

def whoami(incoming_msg, the_bot):
    """
    Respond to a /whoami message
    :param incoming_msg: The incoming message object from Spark
    :param the_botot: The bot which includes our spark api instance
    :return: A text or markdown based reply, and the format to send it in
    """
    # lets get the info about who sent this message
    sender = the_bot.spark.people.get(incoming_msg.personId)
    room = the_bot.spark.rooms.get(incoming_msg.roomId)
    response = f'{sender.displayName} here is some of your information: \n\n\n **Room:** you are in \"**{room.title}**\" \n\n\n **Room id:** *{incoming_msg.roomId}*'
    the_bot.spark.messages.create(roomId=room.id, markdown=response)
    response = f' **Email:** your email on file is *{incoming_msg.personEmail}*'
    return response, "markdown"

def send_echo(incoming_msg, the_bot):
    """
    :param incoming_msg: The incoming message object from Spark
    :param the_botot: The bot which includes our spark api instance
    :return: A text or markdown based reply, and the format to send it in
    """
    # Get sent message without the mention or the command
    message = incoming_msg.text[incoming_msg.text.find('/echo ')+6:]
    response = f"Ok, I'll say it: \"{message}\""
    return response, "text"

def leave(incoming_msg, the_bot):
    """
    Respond to a /leave message
    :param incoming_msg: The incoming message object from Spark
    :param the_botot: The bot which includes our spark api instance
    :return: A text or markdown based reply, and the format to send it in
    """
    # lets get the info about who sent this message
    memberships = the_bot.spark.memberships.list(roomId=incoming_msg.roomId)
    my_id = the_bot.spark.people.me().id
    my_membership = ''
    for m in memberships:
        if m.personId == my_id:
            my_membership = m.id
            break

    if my_membership:
        the_bot.spark.messages.create(roomId=incoming_msg.roomId, text="OK.  I know when I'm not wanted...")
        the_bot.spark.memberships.delete(my_membership)
    else:
        return "I don't know how to leave!", "text"

# Add new commands
bot.add_command('/hello', 'say hello to our bot', hello)
bot.add_command('/whoami', 'tell me who i am', whoami)
bot.add_command('/echo', 'repeat this back to me', send_echo)
bot.add_command('/leave', 'bot should leave the room', leave)

# Run Bot
bot.run(host='0.0.0.0', port=7000)
