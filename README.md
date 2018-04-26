# webex-bot-python
This is a fork of the [ciscosparkbot project](https://github.com/imapex/ciscosparkbot), which provided an example of how to create a (then) Cisco Spark bot using the ciscosparkapi sdk.   This fork is designed as a companion to the [webex-api-emulator](https://github.com/webex/webex-api-emulator) to provide an example of a python based bot that regression tests could be created for.

Please see the [bot-test-framework-example](https://github.com/jpjpjp/bot-test-framework-example) project to see a full example of how to create and run a regression test against this bot.   

## Coding steps to make a ciscosparkapi based bot work with the emulator
It must be possible to configure the bot to send Webex API requests to the emulator rather than the real Webex API endpoint.  To accomplish this we made to changes to the original project.

In the [main bot code](webex_bot.py), we check to see if the environment variable SPARK_API_URL is set.  If so, we pass it into the contructor for the SparkBot

  ```
  if os.getenv("SPARK_API_URL"):
      bot = SparkBot(bot_app_name, spark_bot_token=spark_token,
                    spark_api_url=os.getenv("SPARK_API_URL"),
                    spark_bot_url=bot_url, spark_bot_email=bot_email, debug=True)
  else:
      bot = SparkBot(bot_app_name, spark_bot_token=spark_token,
                    spark_bot_url=bot_url, spark_bot_email=bot_email, debug=True)
  ```

Similarly, in the [ciscosparkbot implementation](ciscosparkbot/Spark.py) we pass this on to the CiscoSparkAPI sdk constructor if set:

  ```
        if (spark_api_url):
            self.spark = CiscoSparkAPI(access_token=spark_bot_token, base_url=spark_api_url)
        else:
            self.spark = CiscoSparkAPI(access_token=spark_bot_token)
  ```

## Running the bot in emulator mode

First setup your virtualenv: 
```
virtualenv venv
source venv/bin/activate
pip install ciscosparkbot
```

To run this bot so that it will work in conjunction with the bot-test-framework-example](https://github.com/jpjpjp/bot-test-framework-example), ensure that the webex-api-emulator is running as described there.

This sample reads its configuration from the environment, ie:
  ```
  # Retrieve required details from environment variables
  bot_email = os.getenv("SPARK_BOT_EMAIL")
  spark_token = os.getenv("SPARK_BOT_TOKEN")
  bot_url = os.getenv("SPARK_BOT_URL")
  bot_app_name = os.getenv("SPARK_BOT_APP_NAME")
  ```

To set these so they work with the webex-api-emulator as follows: 
   ```
   SPARK_BOT_EMAIL="bot@sparkbot.io" SPARK_BOT_TOKEN="ZYXWVUTSRQPONMLKJIHGFEDCBA9876543210" SPARK_BOT_URL="http://localhost:7000" SPARK_BOT_APP_NAME="webex-bot-python" SPARK_API_URL="http://localhost:3210/" python webex_bot.py
  ```

Once the bot is up and running you can proceed with the step-by-step instructions in the bot-test-framework-example README.

What follows is the readme from the original project.

# ciscosparkbot

[![Build Status](https://travis-ci.org/imapex/ciscosparkbot.svg?branch=master)](https://travis-ci.org/imapex/ciscosparkbot)
[![Coverage Status](https://coveralls.io/repos/github/imapex/ciscosparkbot/badge.svg?branch=master)](https://coveralls.io/github/imapex/ciscosparkbot?branch=master)


A flask based Bot for Cisco spark

# Prerequisites

If you don't already have a Cisco Spark account, go ahead and register for one.  They are free.
You'll need to start by adding your bot to the Cisco Spark website.

[https://developer.ciscospark.com/add-app.html](https://developer.ciscospark.com/add-app.html)

![add-app](images/newapp.png)

1. Click create bot

![add-bot](images/newbot.png)

2. Fill out all the details about your bot, including a publicly hosted avatar image.  A sample avatar is available at [http://cs.co/devnetlogosq](http://cs.co/devnetlogosq).

![enter-details](images/enterdetails.png)

3. Click "Add Bot", make sure to copy your access token, you will need this in a second

![copy-token](images/copytoken.png)

# Installation

Create a virtualenv and install the module

```
virtualenv venv
source venv/bin/activate
pip install ciscosparkbot
```

# Usage

The easiest way to use this module is to set a few environment variables

```
export SPARK_BOT_URL=https://mypublicsite.io
export SPARK_BOT_TOKEN=<your bots token>
export SPARK_BOT_EMAIL=<your bots email?
export SPARK_BOT_APP_NAME=<your bots name>
```

A [sample script](sample.py) is also provided for your convenience

```
# -*- coding: utf-8 -*-
"""
Sample code for using ciscosparkbot
"""

import os
from ciscosparkbot import SparkBot

__author__ = "imapex"
__author_email__ = "CiscoSparkBot@imapex.io"
__copyright__ = "Copyright (c) 2016 Cisco Systems, Inc."
__license__ = "Apache 2.0"

# Retrieve required details from environment variables
bot_email = os.getenv("SPARK_BOT_EMAIL")
spark_token = os.getenv("SPARK_BOT_TOKEN")
bot_url = os.getenv("SPARK_BOT_URL")
bot_app_name = os.getenv("SPARK_BOT_APP_NAME")

def do_something(incoming_msg):
    """
    Sample function to do some action.
    :param incoming_msg: The incoming message object from Spark
    :return: A text or markdown based reply
    """
    return "i did what you said - {}".format(incoming_msg.text)

# Create a new bot
bot = SparkBot(bot_app_name, spark_bot_token=spark_token,
               spark_bot_url=bot_url, spark_bot_email=bot_email, debug=True)

# Add new command
bot.add_command('/dosomething', 'help for do something', do_something)

# Run Bot
bot.run(host='0.0.0.0', port=5000)
```

# ngrok

ngrok will make easy for you to develop your code with a live bot.

You can find installation instructions here: https://ngrok.com/download

After you've installed ngrok, in another window start the service


`ngrok http 5000`


You should see a screen that looks like this:

```
ngrok by @inconshreveable                                                                                                                                 (Ctrl+C to quit)

Session Status                online
Version                       2.2.4
Region                        United States (us)
Web Interface                 http://127.0.0.1:4040
Forwarding                    http://this.is.the.url.you.need -> localhost:5000
Forwarding                    https://this.is.the.url.you.need -> localhost:5000

Connections                   ttl     opn     rt1     rt5     p50     p90
                              2       0       0.00    0.00    0.77    1.16

HTTP Requests
-------------

POST /                         200 OK
```

Make sure and update your environment with this url:

```
export SPARK_BOT_URL=https://this.is.the.url.you.need

```

Now launch your bot!!


```
python sample.py
```



## Local Development

If you have an idea for a feature you would like to see, we gladly accept pull requests.  To get started developing, simply run the following..

```
git clone https://github.com/imapex/ciscosparkbot
cd virlutils
pip install -r test-requirements.txt
python setup.py develop
```

### Linting

We use flake 8 to lint our code. Please keep the repository clean by running:

```
flake8
```

### Testing

Tests are located in the [tests](./tests) directory.

To run the tests in the `tests` folder, you can run the following command
from the project root.

```
coverage run --source=ciscosparkbot setup.py test
coverage html
```

This will generate a code coverage report in a directory called `htmlcov`
