import sys
import logging
import time
from core.env import get_env
from termcolor import colored


class ColoredFormatter(logging.Formatter):
    def __init__(self):
        logging.Formatter.__init__(self)

    def format(self, record):
        name = colored(record.name, "yellow")
        message = colored(record.msg, "blue")
        trace = colored(
            "{}:{}".format(record.filename, record.lineno), attrs=["dark"]
        )

        strtime = time.strftime("%H:%M:%S", time.localtime(record.created))
        timestamp = colored(
            "{}.{}".format(strtime, int(record.msecs)), attrs=["dark"]
        )

        level = colored(record.levelname, "white", attrs=["bold"])
        if record.levelname == "WARNING":
            level = colored(
                record.levelname, "white", "on_yellow", attrs=["bold"]
            )
        if record.levelname == "ERROR":
            level = colored(
                record.levelname, "white", "on_red", attrs=["bold"]
            )

        print_format = "{} {} {} {} {}".format(
            timestamp, level, name, message, trace
        )
        return print_format


def get_console_handler():
    console_handler = logging.StreamHandler(sys.stdout)
    colored_formatter = ColoredFormatter()
    console_handler.setFormatter(colored_formatter)
    return console_handler


def get_logger(logger_name):
    logger = logging.getLogger(logger_name)

    if get_env("ENV") == "production":
        logger.setLevel(logging.INFO)
    else:
        logger.setLevel(logging.DEBUG)

    logger.addHandler(get_console_handler())

    logger.propagate = False
    return logger
