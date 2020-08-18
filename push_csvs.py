from __future__ import print_function
from argparse import ArgumentParser
import os
import pickle

from googleapiclient.errors import HttpError
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# https://developers.google.com/sheets/api/quickstart/python

# This scope allows read/write access to user's sheets and their properties
# (https://developers.google.com/sheets/api/guides/authorizing)
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

# The ID of the sheet you want to add the CSVs into
SPREADSHEET_ID = "1NpFD-sxSNzCfOWoyMiEC_a1xnw24TdjnUkIqLFcVSqs"

# https://stackoverflow.com/questions/42362702/how-to-import-a-csv-file-using-google-sheets-api-v4
def find_sheet_id_by_name(API, spreadsheet_id, sheet_name):
    sheets_with_properties = (
        API.spreadsheets()
        .get(spreadsheetId=spreadsheet_id, fields="sheets.properties")
        .execute()
        .get("sheets")
    )

    for sheet in sheets_with_properties:
        if "title" in sheet["properties"].keys():
            if sheet["properties"]["title"] == sheet_name:
                return sheet["properties"]["sheetId"]


def push_csv_to_gsheet(API, spreadsheet_id, csv_path, sheet_id):
    with open(csv_path, "r") as csv_file:
        csvContents = csv_file.read()
    body = {
        "requests": [
            {
                "pasteData": {
                    "coordinate": {
                        "sheetId": sheet_id,
                        "rowIndex": "0",  # adapt this if you need different positioning
                        "columnIndex": "0",  # adapt this if you need different positioning
                    },
                    "data": csvContents,
                    "type": "PASTE_NORMAL",
                    "delimiter": ",",
                }
            }
        ]
    }
    request = API.spreadsheets().batchUpdate(spreadsheetId=spreadsheet_id, body=body)
    response = request.execute()
    return response


def write_csvs(spreadsheet_id, csv_dir):
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists("token.pickle"):
        with open("token.pickle", "rb") as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open("token.pickle", "wb") as token:
            pickle.dump(creds, token)

    service = build("sheets", "v4", credentials=creds)

    for file in os.listdir(csv_dir):
        if file.endswith(".csv"):
            body = {
                "requests": [
                    {
                        "addSheet": {
                            "properties": {
                                # By default names the sheet the name of the csv without the csv extension ("bert.csv" would become "bert" in Google sheets)
                                "title": file[:-4]
                            }
                        }
                    }
                ]
            }
            # Attemps to create a new sheet with this name
            try:
                # https://stackoverflow.com/questions/41445723/how-can-i-add-a-new-tab-to-an-existing-sheet-via-the-google-sheets-api\
                result = (
                    service.spreadsheets()
                    .batchUpdate(spreadsheetId=spreadsheet_id, body=body)
                    .execute()
                )
                sheet_id = result["replies"][0]["addSheet"]["properties"]["sheetId"]
            except HttpError:
                # A sheet with this name already exists, so just finds the ID of the sheet. Will overwrite whatever is currently in this sheet.
                sheet_id = find_sheet_id_by_name(service, spreadsheet_id, file[:-4])
            push_csv_to_gsheet(
                service,
                spreadsheet_id,
                csv_path=os.path.join(csv_dir, file),
                sheet_id=sheet_id,
            )


if __name__ == "__main__":
    argp = ArgumentParser()
    argp.add_argument("spreadsheet_id")
    argp.add_argument("csv_dir")
    args = argp.parse_args()
    write_csvs(args.spreadsheet_id, args.csv_dir)
