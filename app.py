#!/usr/bin/python
import random
import resources
import pickle
import os
from datetime import date
from twilio.rest import TwilioRestClient


ACCOUNT_SID = resources.ACCOUNT_SID
AUTH_TOKEN = resources.AUTH_TOKEN
MY_NUMBER = resources.MY_NUMBER
MY_TWILIO_NUMBER = resources.MY_TWILIO_NUMBER
contacts = resources.contacts
base_directory = os.path.dirname(os.path.realpath(__file__))
calls_tracker_location = os.path.join(base_directory, 'last_call.p')
call_date = date.today()

try:
    calls_tracker_list = pickle.load(open(calls_tracker_location, 'rb'))

except IOError:
    calls_tracker_list = []

found = False
while not found:
    to_call = random.sample(contacts.keys(), 1)[0]
    if len(calls_tracker_list) == 0 or calls_tracker_list[-1][0] != to_call:
        found = True
        calls_tracker_list.append((to_call, call_date))

body = 'Today you should call ' + to_call + '\n at' + contacts[to_call]

client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN)

client.messages.create(
    to=MY_NUMBER,
    from_=MY_TWILIO_NUMBER,
    body=body,
)

pickle.dump(calls_tracker_list, open(calls_tracker_location, 'wb'))
