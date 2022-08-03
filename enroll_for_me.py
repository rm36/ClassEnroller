# This script was based on the instructions at:
# https://developers.google.com/gmail/api/guides/push#python

import os
from concurrent.futures import TimeoutError
from google.cloud import pubsub_v1
from gmail_helpers import is_latest_email_a_trigger
from enroller import enroll

project_id = "CHANGE_ME"
subscription_id = "CHANGE_ME_TOO"
credential_path = "C:\\path\\to\\CHANGE_ME_ALSO.json"

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credential_path

subscriber = pubsub_v1.SubscriberClient()
# The `subscription_path` method creates a fully qualified identifier
# in the form `projects/{project_id}/subscriptions/{subscription_id}`
subscription_path = subscriber.subscription_path(project_id, subscription_id)

def callback(message: pubsub_v1.subscriber.message.Message) -> None:
    data = message.data.decode('UTF-8')
    print("Received ", data)
    if is_latest_email_a_trigger():
        print('Time to enroll! Enrolling...')
        enroll()
    else:
        print('Not time to enroll yet.')
    message.ack()

streaming_pull_future = subscriber.subscribe(subscription_path, callback=callback)
print(f"Listening for messages on {subscription_path}..\n")

# Wrap subscriber in a 'with' block to automatically call close() when done.
with subscriber:
    try:
        # When `timeout` is not set, result() will block indefinitely.
        streaming_pull_future.result()
    except TimeoutError:
        streaming_pull_future.cancel()  # Trigger the shutdown.
        streaming_pull_future.result()  # Block until the shutdown is complete.