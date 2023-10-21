#!/usr/bin/python

import http.client
import httplib2
import os
import random
import sys
import time

from apiclient.discovery import build
from apiclient.errors import HttpError
from apiclient.http import MediaFileUpload
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import argparser, run_flow

CATEGORY = {
    "Film et animation": "1",
    "Automobiles et véhicules": "2",
    "Musique": "10",
    "Animaux": "15",
    "Sports": "17",
    "Voyage et événements": "19",
    "Gaming": "20",
    "People et blogs": "22",
    "Comédie": "23",
    "Divertissement": "24",
    "Actualités et politique": "25",
    "Howto et style": "26",
    "Éducation": "27",
    "Science et technologie": "28",
    "Non lucratif et activisme": "29",
    "Films": "30",
    "Animation": "31",
    "Action et aventure": "32",
    "Classiques": "33",
    "Comédie": "34",
    "Documentaire": "35",
    "Drame": "36",
    "Famille": "37",
    "Étranger": "38",
    "Horreur": "39",
    "Science-fiction et fantastique": "40",
    "Courts métrages": "41",
    "Thriller": "42",
    "Shorts": "43",
    "Spectacles": "44",
    "Bandes-annonces": "45"
}

# Explicitly tell the underlying HTTP transport library not to retry, since
# we are handling retry logic ourselves.
httplib2.RETRIES = 1

# Maximum number of times to retry before giving up.
MAX_RETRIES = 10

# Always retry when these exceptions are raised.
RETRIABLE_EXCEPTIONS = (httplib2.HttpLib2Error, IOError, http.client.NotConnected,
  http.client.IncompleteRead, http.client.ImproperConnectionState,
  http.client.CannotSendRequest, http.client.CannotSendHeader,
  http.client.ResponseNotReady, http.client.BadStatusLine)

# Always retry when an apiclient.errors.HttpError with one of these status
# codes is raised.
RETRIABLE_STATUS_CODES = [500, 502, 503, 504]

# The CLIENT_SECRETS_FILE variable specifies the name of a file that contains
# the OAuth 2.0 information for this application, including its client_id and
# client_secret. You can acquire an OAuth 2.0 client ID and client secret from
# the Google API Console at
# https://console.developers.google.com/.
# Please ensure that you have enabled the YouTube Data API for your project.
# For more information about using OAuth2 to access the YouTube Data API, see:
#   https://developers.google.com/youtube/v3/guides/authentication
# For more information about the client_secrets.json file format, see:
#   https://developers.google.com/api-client-library/python/guide/aaa_client_secrets
CLIENT_SECRETS_FILE = "client_secrets.json"

# This OAuth 2.0 access scope allows an application to upload files to the
# authenticated user's YouTube channel, but doesn't allow other types of access.
YOUTUBE_UPLOAD_SCOPE = "https://www.googleapis.com/auth/youtube.upload"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

# This variable defines a message to display if the CLIENT_SECRETS_FILE is
# missing.
MISSING_CLIENT_SECRETS_MESSAGE = """
WARNING: Please configure OAuth 2.0

To make this sample run you will need to populate the client_secrets.json file
found at:

   %s

with information from the API Console
https://console.developers.google.com/

For more information about the client_secrets.json file format, please visit:
https://developers.google.com/api-client-library/python/guide/aaa_client_secrets

wesh ta oublié le fichier client_secrets.json pour te connecter
""" % os.path.abspath(os.path.join(os.path.dirname(__file__),
                                   CLIENT_SECRETS_FILE))

VALID_PRIVACY_STATUSES = ("public", "private", "unlisted")


def get_authenticated_service(args):
  flow = flow_from_clientsecrets(CLIENT_SECRETS_FILE,
    scope=YOUTUBE_UPLOAD_SCOPE,
    message=MISSING_CLIENT_SECRETS_MESSAGE)

  storage = Storage("%s-oauth2.json" % sys.argv[0])
  credentials = storage.get()

  if credentials is None or credentials.invalid:
    credentials = run_flow(flow, storage, args)

  return build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
    http=credentials.authorize(httplib2.Http()))

def initialize_upload(youtube, options):
  tags = None
  if 'keywords' in options and isinstance(options['keywords'], str):
      tags = options['keywords'].split(",")

  body = {
      "snippet": {
          "title": options['title'],
          "description": options['description'],
          "tags": tags,
          "categoryId": options['category'],
          "scheduledStartTime": options['date']
      },
      "status": {
          "privacyStatus": options['privacyStatus'],
          "selfDeclaredMadeForKids": options['ForKids'],
          "notifySubscribers": options['notify']
      }
  }

  # Call the API's videos.insert method to create and upload the video.
  insert_request = youtube.videos().insert(
      part=",".join(body.keys()),
      body=body,
      media_body=MediaFileUpload(options['file'], chunksize=-1, resumable=True)
  )

  ID = resumable_upload(insert_request)
  if ID is not None and 'miniature' in options and options['miniature'] != "":
      youtube.thumbnails().set(
          videoId=ID,
          media_body=MediaFileUpload(options['miniature'])
      ).execute()


# This method implements an exponential backoff strategy to resume a
# failed upload.
def resumable_upload(insert_request):
  response = None
  error = None
  retry = 0
  while response is None:
    try:
      print ("Uploading file...")
      status, response = insert_request.next_chunk()
      if response is not None:
        if 'id' in response:
          print ("Video id '%s' was successfully uploaded." % response['id'])
          return response['id']
        else:
          exit("The upload failed with an unexpected response: %s" % response)
    except HttpError as e:
      if e.resp.status in RETRIABLE_STATUS_CODES:
        error = "A retriable HTTP error %d occurred:\n%s" % (e.resp.status,
                                                             e.content)
      else:
        raise
    except RETRIABLE_EXCEPTIONS as e:
      error = "A retriable error occurred: %s" % e

    if error is not None:
      print (error)
      retry += 1
      if retry > MAX_RETRIES:
        exit("No longer attempting to retry.")

      max_sleep = 2 ** retry
      sleep_seconds = random.random() * max_sleep
      print ("Sleeping %f seconds and then retrying..." % sleep_seconds)
      time.sleep(sleep_seconds)

def upload(videopath='render.mp4', title="Test Title", description="Test Description", category="22", keywords="", n_privacy_statuses=1, miniature_path="", kids=False, notif=True, date=None):
  youtube = get_authenticated_service(args=None)  # Nous n'avons pas besoin de passer d'arguments de ligne de commande

  # Créez un dictionnaire contenant les valeurs à passer à initialize_upload()
  upload_args = {
      "file": videopath,
      "title": title,
      "description": description,
      "category": category,
      "keywords": keywords,
      "privacyStatus": VALID_PRIVACY_STATUSES[n_privacy_statuses],
      "miniature": miniature_path,
      "ForKids": kids,
      "notify": notif,
      "date": date
  }

  if not os.path.exists(upload_args['file']):
      exit("Please specify a valid file using the --file= parameter.")

  try:
      initialize_upload(youtube, upload_args)
  except HttpError as e:
      print("An HTTP error %d occurred:\n%s" % (e.resp.status, e.content))


if __name__ == '__main__':
	upload()
