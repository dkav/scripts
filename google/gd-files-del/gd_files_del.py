"""Simple script to delete files from Google Drive."""

from __future__ import print_function
import pickle
import os.path

import httplib2

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request


SCOPES = ["https://www.googleapis.com/auth/drive"]

MY_QUERY = "name contains 'test'"


def get_credentials():
    """Get Google credentials."""
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists("fetch_token.pickle"):
        with open("fetch_token.pickle", "rb") as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json", SCOPES
            )
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open("fetch_token.pickle", "wb") as token:
            pickle.dump(creds, token)

    return creds


def callback(_request_id, _response, exception):
    """Check callback for exception."""
    if exception:
        print("Exception:", exception)


def delete_files(service, batch, items):
    """Batch delete files."""
    for item in items:
        print(u"Deleting {0} ({1})".format(item["name"], item["id"]))
        batch.add(service.files().delete(fileId=item["id"]))

    batch.execute()


def get_files(service, token):
    """Get list of files."""
    results = (
        service.files()
        .list(
            q=MY_QUERY,
            spaces="drive",
            fields="nextPageToken, files(id, name)",
            pageToken=token,
            pageSize=100,
        )
        .execute()
    )
    items = results.get("files", [])
    token = results.get("nextPageToken", None)
    return items, token


def main():
    """Get files and delete them."""
    cred = get_credentials()
    service = build("drive", "v3", credentials=cred)
    batch = service.new_batch_http_request(callback=callback)
    token = None

    while True:
        files, token = get_files(service, token)
        print(files)
        if not files:
            print("No file exists to delete. Exiting...")
            break
        delete_files(service, batch, files)
        if token is None:
            print("No more files are found")
            break


if __name__ == "__main__":
    main()
