import codecs

class Log:
    def __init__(self) -> None:
        pass

    def write_log(self, file_name, string, mode):
        with codecs.open(file_name, mode, 'utf-8') as log:
            log.write(string+'\n')
        return True