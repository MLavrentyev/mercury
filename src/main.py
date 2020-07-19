from multiprocessing import Process, Queue, Lock
from abc import ABC, abstractmethod
from flask_socketio import SocketIO
from utils.config import Config
from utils.logger import Logger, LogType
from data.data import DataPoint
from data.receiver import DataReceiver, SerialDataReceiver, StubDataReceiver
from web.server import app, websocket, sendData


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

    def close(self):
        self.process.kill()
        self.process.close()


class WebServerRunner(Runner):
    def execute(self, queueConn, lock, *args):
        assert len(args) == 1
        socket: SocketIO = args[0]

        socket.run(app)


class WebSocketRunner(Runner):
    def execute(self, queueConn, lock, *args):
        assert len(args) == 1
        socket: SocketIO = args[0]

        while True:
            data: DataPoint = queueConn.get(block=True)
            sendData(socket, data)


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

                    queueConn.put_nowait(latestData)


if __name__=="__main__":
    config = Config("config.yaml")
    logger = Logger(logDirectory="logs/", stdoutLevel=LogType.DEBUG)

    webServerRunner = WebServerRunner(config, logger, websocket)
    webSocketRunner = WebSocketRunner(config, logger, websocket)
    dataReceiverRunner = DataReceiverRunner(config, logger, StubDataReceiver(config))