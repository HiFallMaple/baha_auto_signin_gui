import json
import codecs
import os
from pathlib import Path


class Accounts_system:
    def __init__(self) -> None:
        self.ACCOUNTS_JSON_FILE_NAME = "accounts.json"
        self.STATUS_JSON_FILE_NAME = "status.json"
        self.ENCODING = 'utf-8'
        pass

    def get_accounts(self) -> list or False:
        if Path(self.ACCOUNTS_JSON_FILE_NAME).is_file() is True:
            return json.load(open(self.ACCOUNTS_JSON_FILE_NAME,))
        else: 
            return False

    def get_status(self) -> list or False:
        if Path(self.STATUS_JSON_FILE_NAME).is_file() is True:
            return json.load(open(self.STATUS_JSON_FILE_NAME,))
        else: 
            return False

    def save_accounts(self, accounts) -> None:
        json.dump(accounts, codecs.open(self.ACCOUNTS_JSON_FILE_NAME, 'w',
            self.ENCODING), ensure_ascii=False, indent=4, sort_keys=False)
        return None
    
    def save_accounts_status(self, status) -> None:
        json.dump(status, codecs.open(self.STATUS_JSON_FILE_NAME, 'w',
                  'utf-8'), ensure_ascii=False, indent=4, sort_keys=False)
        return None