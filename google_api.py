import gspread
import pandas as pd
import json
from oauth2client.service_account import ServiceAccountCredentials

json_constants_file = open("constants.json")
json_constants = json.load(json_constants_file)


class SheetsAPI:
    def __init__(self):
        print("Connecting to RCTS Google Sheets API\n...")
        self.creds = ServiceAccountCredentials.from_json_keyfile_name(json_constants["google_api"]["google_api_json"],
                                                                      json_constants["google_api"]["scope"])

        self.client = gspread.authorize(self.creds)
        self.sheet = self.client.open(json_constants["google_api"]["google_sheet_filename"])

        self._log = self.sheet.get_worksheet(0)
        self._filter = self.sheet.get_worksheet(1)
        self._accounts = self.sheet.get_worksheet(2)
        self._version = self.sheet.get_worksheet(3)
        self._test_accounts = self.sheet.get_worksheet(4)

        self._log = self._log.get_all_values()
        self._filter = self._filter.get_all_values()
        self._accounts = self._accounts.get_all_values()
        self._version = self._version.get_all_values()
        self._test_accounts = self._test_accounts.get_all_values()

        self.log_df = pd.DataFrame(self._log)
        self.filter_df = pd.DataFrame(self._filter)
        self.accounts_df = pd.DataFrame(self._accounts).iloc[1:, 0].values.tolist()
        self.test_accounts_df = pd.DataFrame(self._test_accounts).iloc[1:, 0].values.tolist()
        self.version_df = pd.DataFrame(self._version)
        print("Connected!")

    def insert_rows(self, sheet_index, df_to_insert):
        sheet_to_insert = self.sheet.get_worksheet(sheet_index)
        sheet_to_insert.append_rows(df_to_insert)

