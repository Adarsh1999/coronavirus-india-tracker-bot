from auth import DEFAULT_SLACK_WEBHOOK
import requests
import json
import logging

# this is used as the slack webhooks only except json headers
HEADERS={
    'Content-type':'application/json'
}

# this is a function under functions and it returns a functions
def slacker(webhook_url=DEFAULT_SLACK_WEBHOOK):
    def slackit(msg):
        logging.info('sending {msg} to slack'.format(msg=msg))
        payload={'text':msg}
        return requests.post(webhook_url,headers=HEADERS,data=json.dumps([payload]))
    return slackit