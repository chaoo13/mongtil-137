# -*- coding:utf-8 -*-
from __future__ import print_function
import httplib2
import os
from apiclient import errors
from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/gmail-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/gmail.readonly'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Gmail API Python Quickstart'


def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'gmail-python-quickstart.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials


def get_subject(service, user_id, msg_id):
  try:
      results = service.users().messages().get(userId=user_id, id=msg_id).execute()
      payloads = results.get('payload')
      parts = payloads.get('headers')
      subject = parts.get('Subject')
      return subject
  except errors.HttpError, error:
    print('An error occurred: +%s' % error)
    return



def modify_message(service, user_id, msg_id, msg_labels):
  """Modify the Labels on the given Message.

  Args:
    service: Authorized Gmail API service instance.
    user_id: User's email address. The special value "me"
    can be used to indicate the authenticated user.
    msg_id: The id of the message required.
    msg_labels: The change in labels.

  Returns:
    Modified message, containing updated labelIds, id and threadId.
  """
  try:
    message = service.users().messages().modify(userId=user_id, id=msg_id, body=msg_labels).execute()
    label_ids = message['labelIds']
    print('Message ID: %s - With Label IDs %s' % (msg_id, label_ids))
    return message
  except errors.HttpError, error:
    print('An error occurred: %s' % error)


def unread_label():
  return {'removeLabelIds': ['UNREAD'], 'addLabelIds': []}


def mail_list_unread(keyword):
    return mail_list(keyword, False)


def mail_list_read(keyword):
    return mail_list(keyword, True)


def mail_list(keyword, isread):
    subjects = []
    i=0
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    if isread:
        query = keyword + " is:read"
    else :
        query = keyword + " is:unread"
    service = discovery.build('gmail', 'v1', http=http)
    results = service.users().messages().list(userId='me', labelIds=None, q=query, pageToken=None,
                                              maxResults=None, includeSpamTrash=None).execute()
    messages = results.get('messages')

    if messages:
        for message in messages:
            id = message.get('id')
            subject = get_subject(service, 'me',id)
            if subject:
                subjects.insert(i, subject)
                i=i+1
    else:
        return {'text': 'No mail searched'}

