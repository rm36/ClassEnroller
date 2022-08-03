# This script was based on the instructions at:
# https://developers.google.com/gmail/api/guides/push#python

# Gmail API at:
# https://developers.google.com/resources/api-libraries/documentation/gmail/v1/python/latest/index.html
import os.path
from datetime import datetime

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# The email address that sends the notification to enroll.
SENDER = 'your_email@illinois.edu'

# Used to check if subject is a trigger to enroll.
TRIGGER_SUBSTRING = 'Section Enrollment' # like "Section Enrollment Status Update from Course Explorer"

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']


def get_creds():
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return creds


def get_latest_email_subjects_from(gmail, who):
    results = gmail.users().messages().list(userId='me', q='from:' + who).execute()
    messages = results['messages']
    subjects = []
    for message in messages:
        email = gmail.users().messages().get(userId='me', id=message['id']).execute()
        subject = ''
        date = ''
        for header in email['payload']['headers']:
            if header['name'] == 'Subject':
                subject = header['value']
            if header['name'] == 'Date':
                date = header['value']
        # Example format: 'Tue, 2 Aug 2022 11:39:08 -0700'
        time = datetime.strptime(date, '%a, %d %b %Y %H:%M:%S %z')
        subjects.append({'subject': subject, 'time': time})
    subjects.sort(key=lambda s: s['time'], reverse=True)
    return subjects


def is_subject_a_trigger(subject):
    return (TRIGGER_SUBSTRING in subject)


def is_latest_email_a_trigger():
    creds = get_creds()
    try:
        gmail = build('gmail', 'v1', credentials=creds)

        subjects = get_latest_email_subjects_from(gmail, who=SENDER)

        # Uncomment to list the latest subjects.
        # print('Messages in reverse chronological order:')
        # for s in subjects:
        #     print(s['subject'], ' -- Sent at -- ', s['time'].strftime("%A, %d %B %Y %I:%M%p"))
        
        return is_subject_a_trigger(subjects[0]['subject'])

    except HttpError as error:
        print(f'An error occurred: {error}')


if __name__ == '__main__':
    if is_latest_email_a_trigger():
        print('Time to enroll!')
    else:
        print('Latest email is not a trigger to enroll')