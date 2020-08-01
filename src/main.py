import time
from multiprocessing import Process, Queue, Lock
from abc import ABC, abstractmethod
from utils.config import Config
from utils.logger import Logger, LogType
from data.data import DataPoint
from data.receiver import DataReceiver, SerialDataReceiver, StubDataReceiver
from web.server import app, turnOffFlaskLogging, websocket, sendData


class Runner(ABC):
    connection: Queue = Queue()
    lock: Lock = Lock()

    def __init__(self, config: Config, logger: Logger, *runnerArgs):
        self.config = config
        self.logger = logger
        self.process = Process(target=self.execute, args=(Runner.connection, Runner.lock) + runnerArgs)

    @abstractmethod
    def execute(self, queueConn: Queue, lock: Lock, *args):
        pass

    def start(self):
        self.process.start()
        self.logger.log(f"Started {type(self).__name__} process", LogType.INFO)

    def waitUntilFinished(self):
        self.process.join()

    def close(self):
        self.process.kill()
        self.process.close()
        self.logger.log(f"Stopped {type(self).__name__} process", LogType.INFO)


class WebServerRunner(Runner):
    def execute(self, queueConn: Queue, lock: Lock, *args):
        turnOffFlaskLogging()
        websocket.run(app,
                      port=self.config.getSetting("dashboard.display.port"),
                      debug=self.config.getSetting("dashboard.display.debug"),
                      use_reloader=False)


class WebSocketRunner(Runner):
    def execute(self, queueConn: Queue, lock: Lock, *args):
        while True:
            with lock:
                data: DataPoint = queueConn.get(block=True)
                sendData(websocket, data)


class DataReceiverRunner(Runner):
    def execute(self, queueConn: Queue, lock: Lock, *args):
        assert len(args) == 1
        receiver: DataReceiver = args[0]

        while True:
            if receiver.isNewDataAvailable():
                latestData: DataPoint = receiver.getData()

                with lock:
                    while not queueConn.empty():
                        queueConn.get_nowait()

                    assert queueConn.empty()
                    queueConn.put_nowait(latestData)


class LoggerFlusherRunner(Runner):
    def execute(self, queueConn: Queue, lock: Lock, *args):
        flushFrequency = self.config.getSetting("dashboard.logger.flush-frequency")
        logFlushing = self.config.getSetting("dashboard.logger.log-flushing")

        while True:
            time.sleep(flushFrequency)
            self.logger.flush(logFlushingEvent=logFlushing)


if __name__=="__main__":
    config = Config("config.yaml")
    logger = Logger(logDirectory="logs/", stdoutLevel=LogType[config.getSetting("dashboard.logger.level")])

    webServerRunner = WebServerRunner(config, logger)
    webSocketRunner = WebSocketRunner(config, logger)
    dataReceiverRunner = DataReceiverRunner(config, logger, StubDataReceiver(config))
    loggerFlusherRunner = LoggerFlusherRunner(config, logger)

    webServerRunner.start()
    webSocketRunner.start()
    dataReceiverRunner.start()
    loggerFlusherRunner.start()

    dataReceiverRunner.waitUntilFinished()
