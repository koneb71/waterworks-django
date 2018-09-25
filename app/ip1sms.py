import json

import base64
import requests

from app.models import Client
from waterworks import settings


class SMSGateway(object):
    def __init__(self, from_name="iP.1"):
        self.from_name = from_name
        self.url = "https://"+settings.IP1SMS_API_URL+settings.IP1SMS_ENDPOINT

    def sendMessage(self, to_number, content):
        if to_number[0] == "0" and not to_number[0] == "+":
            to_number = "+63" + to_number[1:]
        print(to_number)
        message = json.dumps({
            "Numbers": [to_number],
            "From": self.from_name,
            "Message": content
        })
        headers = {
            'Content-Type': "application/json",
            "Authorization": "Basic " + base64.b64encode("%s:%s" % (settings.IP1SMS_ACCOUNT, settings.IP1SMS_PASSWORD)),
            "Content-Length": str(len(str(message)))
        }
        send = requests.post(self.url, data=message, headers=headers)
        print(send)

    def sendAll(self, message):
        clients = Client.objects.all()
        for client in clients:
            self.sendMessage(client.phone, message)


# sms = SMSGateway()
# sms.sendMessage('09357184430', "test")