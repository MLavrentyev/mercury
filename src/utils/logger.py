import os
from datetime import datetime
from enum import Enum
from multiprocessing import Queue
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
        self.storedLogs: Queue = Queue()

    def log(self, message: str, logType: LogType):
        datetimeBlock = datetime.now().strftime("%d %b %H:%M:%S")
        logtypeBlock = f"[{logType.name.center(7)}]"

        self.storedLogs.put(f"{logtypeBlock} {datetimeBlock}> {message}")

        if self.stdoutLevel and logType.value <= self.stdoutLevel.value:
            print(f"{Logger.colors[logType]}{logtypeBlock}{colorama.Style.RESET_ALL} {datetimeBlock}> {message}")

    def flush(self, logFlushingEvent=False):
        if logFlushingEvent:
            self.log(f"Flushing logs to {os.path.basename(self.logFile)}", LogType.INFO)

        with open(self.logFile, "a") as stream:
            while not self.storedLogs.empty():
                stream.write(self.storedLogs.get_nowait() + "\n")
