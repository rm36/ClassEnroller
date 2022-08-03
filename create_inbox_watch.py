# Creates a watch
# This script was based on the instructions at:
# https://developers.google.com/gmail/api/guides/push#python

from gmail_helpers import get_creds

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

TOPIC_NAME = 'projects/CHANGE_ME/topics/CHANGE_ME_TOO'

# Subscribes to watch changes to the topic.
def main():
    creds = get_creds()
    try:
        # Call the Gmail API
        service = build('gmail', 'v1', credentials=creds)

        # Subscribe to watch
        request = {
          'labelIds': ['INBOX'],
          'topicName': TOPIC_NAME
        }
        results = service.users().watch(userId='me', body=request).execute()
        print('Called to subscribe to topic. Result: ', results)

    except HttpError as error:
        # TODO(developer) - Handle errors from gmail API.
        print(f'An error occurred: {error}')


if __name__ == '__main__':
    main()