import csv
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2 import service_account

SERVICE_ACCOUNT_FILE = 'utils/keys.json'
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SAMPLE_SPREADSHEET_ID = '1PMJTW5ldyErVzXYUumlb6oOxQY_aKHHQDMMZPUgh35Q'

credentials = None
credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)


def read_csv(csv_file):
    with open(csv_file, encoding="utf-8") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=",")
        result = []
        for row in csv_reader:
            result.append(row)
        return result


def export_to_google_sheet(csv_file):
    try:
        data = read_csv(csv_file)
        service = build('sheets', 'v4', credentials=credentials)
        sheet = service.spreadsheets()
        request = sheet.values().update(spreadsheetId=SAMPLE_SPREADSHEET_ID, range="B2",
                                        valueInputOption='USER_ENTERED', body={"values": data})
        try:
            response = request.execute()
            print(response)
        except Exception as e:
            print(e)
    except HttpError as err:
        print(err)


if __name__ == "__main__":
    export_to_google_sheet("../output/output.csv")
