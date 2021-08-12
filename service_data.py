import json
import codecs
import os

class Service_data:
    def __init__(self) -> None:
        self.TIME_JSON_FILE_NAME = "time.json"
        self.PORT_FILE_NAME = "port"
        self.RESTART_STATUS_FILE_NAME = "restart_status"
        self.TIME_IS_CHANGED_FILE_NAME = "time_is_changed"
        self.ENCODING = 'utf-8'
        pass

    def get_port(self) -> int or False:
        if os.path.isfile(self.PORT_FILE_NAME) is True:
            with open(self.PORT_FILE_NAME, encoding=self.ENCODING) as f:
                port = int(f.readline())
            return port
        else: 
            return False

    def get_time(self) -> list or False:
        if os.path.isfile(self.TIME_JSON_FILE_NAME) is True:
            return json.load(open(self.TIME_JSON_FILE_NAME,))
        else: 
            return False

    def set_restart_status(self, status) -> None:
        with codecs.open(self.RESTART_STATUS_FILE_NAME, 'w',self.ENCODING) as f:
            f.write(str(status))
        return None

    def save_port(self, port) -> None:
        with codecs.open(self.PORT_FILE_NAME, 'w',self.ENCODING) as f:
            f.write(str(port))
        return None

    def save_time(self, time_dict) -> None:
        json.dump(time_dict, codecs.open(self.TIME_JSON_FILE_NAME, 'w',
            self.ENCODING), ensure_ascii=False, indent=4, sort_keys=False)
        self.save_time_status(True)
        return None

    def save_time_status(self, bool):
        with codecs.open(self.TIME_IS_CHANGED_FILE_NAME, 'w',self.ENCODING) as f:
            f.write(str(bool))

    def time_is_changed(self) -> bool:
        with open(self.TIME_IS_CHANGED_FILE_NAME, encoding=self.ENCODING) as f:
            return f.readline() == "True"


    
