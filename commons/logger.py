import logging
import datetime as dt
import os


class Logger:
    def __init__(self):
        pass

    @staticmethod
    def setup_logger():
        filename = Logger.request_loggin_file()
        logging.basicConfig(filename=filename, level=logging.DEBUG, format="%(asctime)s %(message)s")

        Logger.info("Article Categorizer Logger Started")

    @staticmethod
    def request_loggin_file(path="unknown"):
        # create file with current date in file name
        file_name = dt.datetime.now().strftime("%Y-%m-%d") + ".log"
        filepath = f'./logs/{path}/{file_name}'

        if not os.path.isfile(filepath):
            open(filepath, 'w').close()
        else:
            # check if file is biggner than 1MB
            if os.path.getsize(filepath) > 1000000:
                # rename file
                os.rename(filepath, filepath + ".old")
                # create new file
                open(filepath, 'w').close()
            else:
                open(filepath, 'a').close()

        return file_name

    @staticmethod
    def info(message):
        print(message)
        logging.info(message)

    @staticmethod
    def error(message):
        print(message)
        logging.error(message)

    @staticmethod
    def debug(message):
        print(message)
        logging.debug(message)

    @staticmethod
    def warning(message):
        print(message)
        logging.warning(message)

    @staticmethod
    def critical(message):
        print(message)
        logging.critical(message)
