import os
from datetime import datetime
from enum import Enum
import colorama


class LogType(Enum):
    ERROR = 0
    WARNING = 1
    INFO = 2
    DEBUG = 3


class Logger:
    colors = {
        LogType.ERROR: colorama.Fore.RED,
        LogType.WARNING: colorama.Fore.YELLOW,
        LogType.INFO: colorama.Fore.BLUE,
        LogType.DEBUG: colorama.Fore.CYAN,
    }

    def __init__(self, logDirectory="logs/", stdoutLevel: LogType=None):
        self.stdoutLevel: LogType = stdoutLevel
        if self.stdoutLevel:
            colorama.init()

        self.logFile = os.path.join(logDirectory,
                                    datetime.now().strftime("%Y_%m_%d"),
                                    datetime.now().strftime("%H_%M_%S.log"))
        os.makedirs(os.path.dirname(self.logFile), exist_ok=True)
        self.storedLogs = []

    def log(self, message: str, logType: LogType):
        datetimeBlock = datetime.now().strftime("%d %b %H:%M:%S")
        logtypeBlock = f"[{logType.name.center(7)}]"

        self.storedLogs.append(f"{logtypeBlock} {datetimeBlock}> {message}\n")

        if self.stdoutLevel and logType.value <= self.stdoutLevel.value:
            print(f"{Logger.colors[logType]}{logtypeBlock}{colorama.Style.RESET_ALL} {datetimeBlock}> {message}")

    def flush(self):
        with open(self.logFile, "a") as stream:
            stream.writelines(self.storedLogs)
            self.storedLogs = []
