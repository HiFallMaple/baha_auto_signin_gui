import datetime
import pytz
from data_processor import Data_processor
import time

class Baha_auto_signin_timer:
    def __init__(self, data_processor :Data_processor) ->None:
        self.TIMEZONE = pytz.timezone('Asia/Taipei')
        self.data_processor = data_processor
        self.time_list = list()
        self.__init_time_list()
        print(self.TIMEZONE)
        self.time_over = 1
        pass

    def countdown_until_time_over(self):
        while True:
            if self.data_processor.time_is_changed():
                self.__init_time_list()
            self.time_list = [self.__set_time_to_tomorrow(_time) if self.__time_is_smaller_than_now_for_a_period_of_time(_time) else _time for _time in self.time_list]
            for _time in self.time_list:
                if self.now() >= _time:
                    return None
            time.sleep(0.9)

    def now(self) -> datetime.datetime:
        return datetime.datetime.now().astimezone(self.TIMEZONE)

    def __init_time_list(self) -> None:
        tmp = self.data_processor.get_time()
        self.data_processor.save_time_status(False)
        self.time_list = [self.__time_converse(_time) for _time in tmp]
        return None

    def __time_converse(self, time :str) -> datetime.datetime:
        tmp = [int(i) for i in time.split(':')]
        conv_time = self.now().replace(
            hour=tmp[0], minute=tmp[1], second=tmp[2], microsecond=0)
        return conv_time

    def __time_is_smaller_than_now_for_a_period_of_time(self, time) -> bool:
        return time + datetime.timedelta(0, self.time_over) < self.now()

    def __set_time_to_tomorrow(self, time) -> datetime.datetime:
        conv_time = time + datetime.timedelta(days=1)
        return conv_time
