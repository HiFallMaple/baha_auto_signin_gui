import socket
from accounts_system import Accounts_system
from service_data import Service_data

class Data_processor(Accounts_system, Service_data):
    def __init__(self) -> None:
        super().__init__()
        super(Accounts_system, self).__init__()
        super(Service_data, self).__init__()
        pass

    def is_port_in_use(self) -> bool:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            port = self.get_port()
            return s.connect_ex(('localhost', port)) == 0
    
    def get_setting_data(self):
        setting_json = dict()
        setting_json["time"] = self.get_time()
        setting_json["accounts"] = self.get_accounts()
        return setting_json