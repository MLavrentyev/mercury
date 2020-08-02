import asyncio
import time
import websockets
from multiprocessing import Lock, Queue
from data.data import DataPoint
from utils.config import Config
from utils.logger import Logger, LogType

class Websocket:
    def __init__(self, config: Config, logger: Logger, dataQueue: Queue, dataQueueLock: Lock):
        self.config = config
        self.logger = logger
        self.dataQueue = dataQueue
        self.dataQueueLock = dataQueueLock

    def __enter__(self):
        async def websocketHandler(websocketServer: websockets.WebSocketServerProtocol, _: str):
            self.logger.log(f"Starting web socket on port {websocketServer.local_address[1]}", LogType.INFO)
            while True:
                with self.dataQueueLock:
                    data: DataPoint = self.dataQueue.get()
                    await websocketServer.send(data.toJson())

                updateTime: float = self.config.getSetting("dashboard.websocket.update-time")
                time.sleep(updateTime)

        websocketPort = self.config.getSetting("dashboard.websocket.port")
        return websockets.serve(websocketHandler, "localhost", websocketPort)


    def __exit__(self, exceptionType, exceptionValue, exceptionTraceback):
        if exceptionType is None:
            self.logger.log("Closing websocket with no errors", LogType.INFO)
        else:
            self.logger.log(f"Closing websocket with error {exceptionType}", LogType.ERROR)

        asyncio.get_event_loop().close()