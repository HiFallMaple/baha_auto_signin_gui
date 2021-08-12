import requests
from bs4 import BeautifulSoup
import time
import json
import crawler
from accounts_system import Accounts_system
from log import Log

class Baha():
    def __init__(self, reqs = requests.Session(),  log_file_name = '.log', account = dict()) -> None:
        self.reqs = reqs
        self.log_file_name = log_file_name
        self.account = account
        self.MAIN_HEADERS = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36',
            'Referer': 'https://www.gamer.com.tw/'
        }
        self.MAIN_URL = "https://www.gamer.com.tw"
        self.USER_URL = "https://user.gamer.com.tw"
        return None

    def login(self) -> bool:
        if self.is_login() is True:
            return True
        login_page=self.reqs.get(self.USER_URL+"/login.php", headers=self.MAIN_HEADERS)
        soup = BeautifulSoup(login_page.text, 'html.parser')
        alternativeCaptcha=soup.find('input', {'name': 'alternativeCaptcha'}).get('value')
        login_payload = self.__set_login_payload(alternativeCaptcha)
        login = self.reqs.post(self.USER_URL+"/doLogin.php", headers=self.MAIN_HEADERS, data=login_payload)
        soup = BeautifulSoup(login.text, 'html.parser')
        if self.is_login() is True:
            return True
        else:
            return False

    def __set_login_payload(self, alternativeCaptcha) -> dict:
        payload={
            "alternativeCaptcha": alternativeCaptcha,
            "autoLogin": "T",
            "getFrom": self.MAIN_URL,
            "hasCheck": "0",
            "onlogin": "0",
            "passwdh": self.account["passwd"],
            "saveid": "T",
            "twoStepAuth": "",
            "uidh": self.account["uid"]
        }
        return payload

    def is_login(self) -> bool:
        response = self.reqs.get('https://home.gamer.com.tw/homeindex.php', headers = self.MAIN_HEADERS)
        soup = BeautifulSoup(response.text, 'html.parser')
        ul = soup.find("ul", class_="MSG-mydata1")
        if ul is not None:
            li = ul.find("li")
            web_account = li.find("span").text
            return self.account["uid"] == web_account
        else:
            return False

    def signin(self) -> dict:
        signin_status = self.get_signin_status()
        if signin_status["data"]["signin"] == 1:
            return signin_status
        else:
            time_code = int(time.time()*1000)
            csrf_token = self.reqs.get(self.MAIN_URL + "/ajax/get_csrf_token.php?_={}".format(time_code), headers = self.MAIN_HEADERS)
            signin_data = {
                "action": 1,
                "token": csrf_token.text
            }
            signin = self.reqs.post(self.MAIN_URL+"/ajax/signin.php", headers=self.MAIN_HEADERS, data=signin_data)
            signin_status = self.get_signin_status() 
            if signin_status["data"]["signin"] == 1:
                return signin_status
        return False

    def get_signin_status(self) -> dict:
        if self.is_login() is False:
            return False
        else:
            return json.loads(self.reqs.post(url = self.MAIN_URL+"/ajax/signin.php", headers=self.MAIN_HEADERS, data={"action": 2}).text)

    def is_signin(self) -> bool:
        status = self.get_signin_status()
        return status["data"]["signin"] == 1


class Baha_auto_signin(): # 巴哈自動登入
    def __init__(self) -> None:
        self.baha = Baha()
        self.crawler_session = crawler.Session()
        self.accounts_system = Accounts_system()
        self.DEFAULT_ACCOUNTS = [{"uid": "test123qwe","passwd": "test1qa2ws"}]
        pass

    def __renew_baha_session(self):
        self.baha.reqs = requests.Session()
        return None


    def run(self):
        tmp_accounts = self.accounts_system.get_accounts()
        if tmp_accounts == False: # 無帳號
            print("accounts.json doesn't exist\nLoad defaust accounts")
            tmp_accounts = [{"uid": "test123qwe","passwd": "test1qa2ws"}]
            self.accounts_system.save_accounts(tmp_accounts)
        self.accounts = tmp_accounts

        status_dict = dict()
        for account in self.accounts:
            self.baha.account = account
            tmp_session = self.crawler_session.load_session(account["uid"])

            if tmp_session is None: # 從未登入過
                print("{} session not exist".format(account["uid"]))
                tmp_session = requests.Session()
            else:
                print("{} session exist".format(account["uid"]))

            self.baha.reqs = tmp_session

            if self.baha.is_login() is False:
                print("{} is not login!".format(account["uid"]))
                login_status = self.baha.login()
                if login_status == True:
                    print("{} Login success!!".format(account["uid"]))
                else:
                    print("{} Login Failed! Skip this account".format(account["uid"]))
                    continue
            else:
                print("{} is login!".format(account["uid"]))

            status_dict[account["uid"]] = dict() # 建立狀態dict

            if self.baha.is_signin() is False:
                signin_status = self.baha.signin() # 簽到
                print("{} signin success".format(account["uid"]))
                status_dict[account["uid"]]["login"] = 1
                status_dict[account["uid"]]["status"] = signin_status["data"]
            else:
                print("{} has signed in today".format(account["uid"]))
                signin_status = self.baha.get_signin_status() # 簽到
                status_dict[account["uid"]]["login"] = 1
                status_dict[account["uid"]]["status"] = signin_status["data"]

            self.crawler_session.save_session(self.baha.reqs, account["uid"])
            print("Save session of {}".format(account["uid"]))
            print("Renew session")
            self.__renew_baha_session()
        self.accounts_system.save_accounts_status(status_dict)
        return None
